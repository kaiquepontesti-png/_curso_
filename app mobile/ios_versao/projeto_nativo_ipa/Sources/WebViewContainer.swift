import Foundation
import SwiftUI
import UIKit
import UniformTypeIdentifiers
import WebKit

private final class LocalAppSchemeHandler: NSObject, WKURLSchemeHandler {
    func webView(_ webView: WKWebView, start urlSchemeTask: WKURLSchemeTask) {
        guard let htmlURL = Bundle.main.url(forResource: "index", withExtension: "html"),
              let data = try? Data(contentsOf: htmlURL) else {
            urlSchemeTask.didFailWithError(
                NSError(domain: "com.numesquece.lista", code: 404, userInfo: [NSLocalizedDescriptionKey: "index.html não encontrado"])
            )
            return
        }

        let responseURL = urlSchemeTask.request.url ?? URL(string: "numesquece://app/index.html")!
        let response = URLResponse(
            url: responseURL,
            mimeType: "text/html",
            expectedContentLength: data.count,
            textEncodingName: "utf-8"
        )
        urlSchemeTask.didReceive(response)
        urlSchemeTask.didReceive(data)
        urlSchemeTask.didFinish()
    }

    func webView(_ webView: WKWebView, stop urlSchemeTask: WKURLSchemeTask) {}
}

private final class WeakScriptMessageHandler: NSObject, WKScriptMessageHandler {
    private weak var delegate: WKScriptMessageHandler?

    init(delegate: WKScriptMessageHandler) {
        self.delegate = delegate
    }

    func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
        delegate?.userContentController(userContentController, didReceive: message)
    }
}

private final class ArmazenamentoArquivoIOS {
    private let arquivoURL: URL
    private let fila = DispatchQueue(label: "com.numesquece.ios.storage")
    private var dados: [String: String]

    init() {
        let docs = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first
            ?? FileManager.default.temporaryDirectory
        self.arquivoURL = docs.appendingPathComponent("dados_dispositivo.json")

        if let raw = try? Data(contentsOf: arquivoURL),
           let decoded = try? JSONSerialization.jsonObject(with: raw) as? [String: String] {
            self.dados = decoded
        } else {
            self.dados = [:]
        }
    }

    func scriptPreloadJS() -> String {
        guard let jsonData = try? JSONSerialization.data(withJSONObject: dados, options: []),
              let jsonStr = String(data: jsonData, encoding: .utf8) else {
            return "window.__IOS_PRELOADED_DATA__ = {};"
        }
        return "window.__IOS_PRELOADED_DATA__ = \(jsonStr);"
    }

    func salvar(chave: String, valor: String) {
        dados[chave] = valor
        let snapshot = dados
        let destino = arquivoURL
        fila.async {
            guard let data = try? JSONSerialization.data(withJSONObject: snapshot, options: [.prettyPrinted]) else {
                return
            }
            try? data.write(to: destino, options: .atomic)
        }
    }
}

struct WebViewContainer: UIViewRepresentable {
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    func makeUIView(context: Context) -> WKWebView {
        let contentController = WKUserContentController()
        let preloadScript = WKUserScript(
            source: context.coordinator.storage.scriptPreloadJS(),
            injectionTime: .atDocumentStart,
            forMainFrameOnly: true
        )
        contentController.addUserScript(preloadScript)
        contentController.add(WeakScriptMessageHandler(delegate: context.coordinator), name: "iosStorage")
        contentController.add(WeakScriptMessageHandler(delegate: context.coordinator), name: "iosShare")
        contentController.add(WeakScriptMessageHandler(delegate: context.coordinator), name: "iosImportFile")

        let config = WKWebViewConfiguration()
        config.userContentController = contentController
        config.websiteDataStore = .default()
        config.setURLSchemeHandler(context.coordinator.schemeHandler, forURLScheme: "numesquece")

        let webView = WKWebView(frame: .zero, configuration: config)
        context.coordinator.webView = webView
        webView.backgroundColor = .white
        webView.scrollView.backgroundColor = .white
        webView.scrollView.contentInsetAdjustmentBehavior = .never
        webView.allowsBackForwardNavigationGestures = true
        webView.isOpaque = true

        if let url = URL(string: "numesquece://app/index.html") {
            webView.load(URLRequest(url: url))
        }
        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    final class Coordinator: NSObject, WKScriptMessageHandler, UIDocumentPickerDelegate {
        let schemeHandler = LocalAppSchemeHandler()
        let storage = ArmazenamentoArquivoIOS()
        weak var webView: WKWebView?

        func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
            if message.name == "iosStorage" {
                guard let body = message.body as? [String: Any],
                      let chave = body["chave"] as? String,
                      let valor = body["valor"] as? String else {
                    return
                }
                storage.salvar(chave: chave, valor: valor)
                return
            }

            if message.name == "iosShare" {
                guard let body = message.body as? [String: Any],
                      let jsonStr = body["json"] as? String else {
                    return
                }
                let rawName = (body["fileName"] as? String) ?? "lista.numesquece.json"
                let safeFileName = rawName
                    .replacingOccurrences(of: "/", with: "_")
                    .replacingOccurrences(of: "..", with: "_")
                compartilharArquivo(json: jsonStr, fileName: safeFileName)
                return
            }

            if message.name == "iosImportFile" {
                abrirSeletorArquivos()
            }
        }

        private func controladorApresentacao() -> UIViewController? {
            let scenes = UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }
            let window = scenes.flatMap { $0.windows }.first { $0.isKeyWindow } ?? scenes.flatMap { $0.windows }.first
            var topo = window?.rootViewController
            while let presented = topo?.presentedViewController {
                topo = presented
            }
            return topo
        }

        private func compartilharArquivo(json: String, fileName: String) {
            let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent(fileName)
            guard let data = json.data(using: .utf8) else { return }
            do {
                try data.write(to: tempURL, options: .atomic)
            } catch {
                return
            }

            DispatchQueue.main.async { [weak self] in
                guard let self, let presenter = self.controladorApresentacao() else { return }
                let activityVC = UIActivityViewController(activityItems: [tempURL], applicationActivities: nil)
                if let pop = activityVC.popoverPresentationController {
                    pop.sourceView = presenter.view
                    pop.sourceRect = CGRect(x: presenter.view.bounds.midX, y: presenter.view.bounds.midY, width: 1, height: 1)
                    pop.permittedArrowDirections = []
                }
                presenter.present(activityVC, animated: true)
            }
        }

        private func abrirSeletorArquivos() {
            DispatchQueue.main.async { [weak self] in
                guard let self, let presenter = self.controladorApresentacao() else { return }
                let tipos: [UTType] = [.json, .plainText, .data]
                let picker = UIDocumentPickerViewController(forOpeningContentTypes: tipos, asCopy: true)
                picker.delegate = self
                picker.allowsMultipleSelection = false
                picker.shouldShowFileExtensions = true
                presenter.present(picker, animated: true)
            }
        }

        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            guard let url = urls.first else { return }
            let precisaEncerrarAcesso = url.startAccessingSecurityScopedResource()
            defer {
                if precisaEncerrarAcesso {
                    url.stopAccessingSecurityScopedResource()
                }
            }
            guard let data = try? Data(contentsOf: url) else {
                notificarJS(js: "window.app && window.app.atualizarStatusTransferenciaNativa(false, 'Não foi possível abrir o arquivo selecionado.')")
                return
            }
            let b64 = data.base64EncodedString()
            let nomeEscapado = url.lastPathComponent
                .replacingOccurrences(of: "\\", with: "\\\\")
                .replacingOccurrences(of: "'", with: "\\'")
                .replacingOccurrences(of: "\n", with: " ")
            notificarJS(js: "window.app && window.app.receberArquivoImportadoBase64('\(b64)', '\(nomeEscapado)')")
        }

        func documentPickerWasCancelled(_ controller: UIDocumentPickerViewController) {
            notificarJS(js: "window.app && window.app.atualizarStatusTransferenciaNativa(false, 'Importação de arquivo cancelada.')")
        }

        private func notificarJS(js: String) {
            DispatchQueue.main.async { [weak self] in
                self?.webView?.evaluateJavaScript(js, completionHandler: nil)
            }
        }
    }
}
