document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get(["idiomaSalvo"], (result) => {
    if (result.idiomaSalvo) {
      document.getElementById("idiomaOrigem").value = result.idiomaSalvo;
    }
  });
});

document.getElementById("idiomaOrigem").addEventListener("change", (e) => {
  chrome.storage.local.set({ idiomaSalvo: e.target.value });
});

document.getElementById("btnRecortar").addEventListener("click", async () => {
  const idioma = document.getElementById("idiomaOrigem").value;
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  window.close();
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content.js"]
  }, () => {
    chrome.runtime.sendMessage({ acao: "capturarTela", idioma: idioma });
  });
});