chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.acao === "capturarTela") {
    // Captura a tela inteira em formato de imagem (data URL)
    chrome.tabs.captureVisibleTab(null, { format: "png" }, (imagemDataUrl) => {
      // Envia a imagem capturada para a aba ativa
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { acao: "iniciarSelecao", imagemUrl: imagemDataUrl });
      });
    });
  }
});