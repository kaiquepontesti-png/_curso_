chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.acao === "capturarTela") {
    executarCaptura(request.idioma);
  }
});

chrome.commands.onCommand.addListener((command) => {
  if (command === "ativar_recorte_invisivel") {
    chrome.storage.local.get(["idiomaSalvo"], (result) => {
      const idioma = result.idiomaSalvo || "kor";
      executarCaptura(idioma);
    });
  }
});

function executarCaptura(idioma) {
  chrome.tabs.captureVisibleTab(null, { format: "png" }, (imagemDataUrl) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        files: ["content.js"]
      }, () => {
        chrome.tabs.sendMessage(tabs[0].id, { 
          acao: "iniciarSelecao", 
          imagemUrl: imagemDataUrl,
          idioma: idioma
        });
      });
    });
  });
}