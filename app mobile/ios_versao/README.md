# NumEsquece Lista · Versão iOS (iPhone / iPad)

Esta pasta contém a versão iOS completa do **NumEsquece Lista** (mesmas classes orientadas a objetos `ItemProduto`, `ListaDeCompras`, `CompraFinalizada`, `ArmazenamentoLocal` e `AplicativoNumEsquece`, mesmo visual Monocromático Clássico de Alto Contraste, edição de itens, modo mercado, histórico e navegação com retorno).

> **Importante sobre compilação `.ipa` no Windows:**  
> A Apple exige **macOS + Xcode** para compilar binários nativos iOS (`.ipa`) e exige assinatura digital ligada a um Apple ID para instalar fora da App Store. Por isso, esta pasta entrega **duas opções funcionais**:

---

## Opção 1: Instalação Imediata no iPhone (sem Mac / sem Xcode) — `app_pwa/`
Versão **PWA iOS** configurada com `apple-mobile-web-app-capable`, ícones `icon-180.png`/`icon-512.png`, ajuste de *Safe Areas* (Notch / Dynamic Island / barra inferior do iPhone), prevenção de zoom automático em inputs, gesto de deslizar da borda esquerda e botão `‹ Voltar` na barra superior.

### Como instalar no iPhone pela rede Wi-Fi:
1. No Windows, execute:
   ```powershell
   python servir_pwa_iphone.py
   ```
2. Conecte o iPhone na mesma rede Wi-Fi e abra no **Safari** o endereço exibido no terminal (ex.: `http://192.168.X.X:8080`).
3. Toque em **Compartilhar** (ícone de seta para cima) → **Adicionar à Tela de Início**.
4. Abra o app pelo ícone **NumEsquece** na Tela de Início (abre em tela cheia, sem barra do Safari).

> **Dica para funcionar 100% offline até em Modo Avião:**  
> O Safari iOS só ativa o Service Worker (`sw.js`) quando a página é aberta uma primeira vez via **HTTPS** (ex.: publicando a pasta `app_pwa/` gratuitamente no GitHub Pages, Cloudflare Pages ou Netlify). Depois de aberto uma vez em HTTPS e adicionado à Tela de Início, tudo fica em cache local no aparelho.

---

## Opção 2: App Nativo `.ipa` Offline (`projeto_nativo_ipa/`) via GitHub Actions + Sideloadly / AltStore
Se você quiser um arquivo **`.ipa` nativo instalável** (container SwiftUI + `WKWebView` carregando o HTML offline do bundle + gravação atômica de `dados_dispositivo.json` na pasta `Documents` do app):

1. Suba o projeto para um repositório no GitHub e dispare o workflow `.github/workflows/build-ios-ipa.yml` (executa em runner `macos-15` gratuitamente no GitHub Actions sem precisar ter um Mac).
2. Baixe o arquivo gerado `NumEsqueceLista-unsigned.ipa` nos *Artifacts* da execução.
3. No Windows, conecte o iPhone via cabo USB e instale o `.ipa` usando **Sideloadly** ou **AltStore** com seu Apple ID (iOS 15.0+).

---

## Exportação / Importação via Bluetooth / AirDrop e Arquivos
- **Envio (Exportar)**: Na tela **Minhas Listas** ou dentro de qualquer lista, toque em **📤 Via Bluetooth** / **📡** para gerar `.numesquece.json`. No app nativo (`.ipa`), abre o menu do iOS (`UIActivityViewController`) com **AirDrop (Bluetooth + Wi-Fi Direct)**, **Arquivos** e outros apps; na versão PWA Safari, usa o compartilhamento nativo (`navigator.share` / download).
- **Recebimento (Importar dos Ficheiros)**: Toque em **📥 Importar Arquivo** → **📂 Procurar Listas nos Ficheiros do Celular** para pedir acesso via seletor **Arquivos / iCloud / Downloads** (`UIDocumentPickerViewController` no app nativo ou seletor de arquivos do iOS no PWA), carregar a lista para `ArmazenamentoLocal`, editar itens e usar normalmente.

---

## Atualizar / Regenerar os arquivos iOS após editar o código Python
Sempre que alterar a lógica ou o layout em `mobile_app/ui_builder.py`, rode na raiz do projeto:
```powershell
python ios_versao/gerar_versao_ios.py
```
