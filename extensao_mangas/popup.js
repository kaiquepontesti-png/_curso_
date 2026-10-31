document.getElementById("btnRecortar").addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  // O popup fecha automaticamente para você poder recortar a tela
  window.close();

  // Injeta o código de seleção na página
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content.js"]
  }, () => {
    // Pede para o background capturar a imagem da tela atual
    chrome.runtime.sendMessage({ acao: "capturarTela" });
  });
});