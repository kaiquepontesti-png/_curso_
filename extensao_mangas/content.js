// Remove a camada anterior, se existir
const existente = document.getElementById("manga-tradutor-overlay");
if (existente) existente.remove();

let imagemDeFundoUrl = "";

// Escuta a imagem capturada pelo background
chrome.runtime.onMessage.addListener((request) => {
  if (request.acao === "iniciarSelecao") {
    imagemDeFundoUrl = request.imagemUrl;
    iniciarFerramentaDeRecorte();
  }
});

function iniciarFerramentaDeRecorte() {
  // Cria uma camada transparente em cima da página
  const overlay = document.createElement("div");
  overlay.id = "manga-tradutor-overlay";
  overlay.style.position = "fixed";
  overlay.style.top = "0";
  overlay.style.left = "0";
  overlay.style.width = "100vw";
  overlay.style.height = "100vh";
  overlay.style.background = "rgba(0,0,0,0.3)";
  overlay.style.cursor = "crosshair";
  overlay.style.zIndex = "999999";
  document.body.appendChild(overlay);

  // Cria o quadrado visual da seleção
  const selecao = document.createElement("div");
  selecao.style.position = "absolute";
  selecao.style.border = "2px dashed red";
  selecao.style.background = "rgba(255,255,255,0.2)";
  selecao.style.pointerEvents = "none";
  overlay.appendChild(selecao);

  let inicioX, inicioY, fimX, fimY;
  let arrastando = false;

  overlay.addEventListener("mousedown", (e) => {
    arrastando = true;
    inicioX = e.clientX;
    inicioY = e.clientY;
    selecao.style.left = inicioX + "px";
    selecao.style.top = inicioY + "px";
    selecao.style.width = "0px";
    selecao.style.height = "0px";
  });

  overlay.addEventListener("mousemove", (e) => {
    if (!arrastando) return;
    fimX = e.clientX;
    fimY = e.clientY;
    
    // Permite desenhar o quadrado para qualquer direção
    const atualX = Math.min(inicioX, fimX);
    const atualY = Math.min(inicioY, fimY);
    const largura = Math.abs(inicioX - fimX);
    const altura = Math.abs(inicioY - fimY);

    selecao.style.left = atualX + "px";
    selecao.style.top = atualY + "px";
    selecao.style.width = largura + "px";
    selecao.style.height = altura + "px";
  });

  overlay.addEventListener("mouseup", () => {
    arrastando = false;
    overlay.style.pointerEvents = "none"; // Trava a tela
    overlay.style.background = "rgba(0,0,0,0.6)"; // Escurece mais para indicar carregamento
    
    // Obtém as coordenadas finais da caixa
    const rect = selecao.getBoundingClientRect();
    if (rect.width > 10 && rect.height > 10) {
      processarRecorte(rect, overlay);
    } else {
      overlay.remove(); // Se o clique foi muito pequeno, cancela
    }
  });
}

function processarRecorte(rect, overlay) {
  // Cria um canvas invisível para cortar a imagem da tela
  const canvas = document.createElement("canvas");
  canvas.width = rect.width;
  canvas.height = rect.height;
  const ctx = canvas.getContext("2d");

  const img = new Image();
  img.src = imagemDeFundoUrl;
  
  img.onload = () => {
    // Desenha no canvas apenas a área que o usuário selecionou
    ctx.drawImage(img, rect.left, rect.top, rect.width, rect.height, 0, 0, rect.width, rect.height);
    const imagemRecortadaBase64 = canvas.toDataURL("image/png");
    
    executarOCR(imagemRecortadaBase64, overlay);
  };
}

function executarOCR(imagem64, overlay) {
  // Exibe um balão flutuante para mostrar o resultado, substituindo o popup fechado
  overlay.innerHTML = `<div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); background:white; padding:20px; border-radius:8px; color:black; font-family:sans-serif; text-align:center; min-width:300px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); pointer-events:auto;">
    <h3 style="margin-top:0;">Lendo a imagem...</h3>
    <p>Aguarde, extraindo texto.</p>
  </div>`;
  const container = overlay.querySelector('div');

  // Carrega o Tesseract temporariamente na página
  const script = document.createElement('script');
  script.src = "https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js";
  document.head.appendChild(script);

  script.onload = () => {
    // Altere 'kor' para 'jpn' se for ler Mangá em japonês
    Tesseract.recognize(imagem64, 'kor')
      .then(resultado => {
        const textoExtraido = resultado.data.text.trim();
        if (textoExtraido.length < 1) {
          container.innerHTML = `<h3>Erro</h3><p>Nenhum texto encontrado.</p><button id="fecharOvl">Fechar</button>`;
          document.getElementById('fecharOvl').onclick = () => overlay.remove();
          return;
        }

        container.innerHTML = `<h3>Traduzindo...</h3><p>${textoExtraido}</p>`;
        
        // Manda o texto para a API do Google Translate
        const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=pt&dt=t&q=${encodeURI(textoExtraido)}`;
        
        fetch(url)
          .then(res => res.json())
          .then(data => {
            const textoTraduzido = data[0].map(p => p[0]).join("");
            container.innerHTML = `
              <h3 style="margin-top:0;">Resultado:</h3>
              <textarea style="width:100%; height:60px; margin-bottom:10px;">${textoExtraido}</textarea>
              <textarea style="width:100%; height:60px; margin-bottom:10px; background:#f5f5f5;">${textoTraduzido}</textarea>
              <button id="fecharOvl" style="padding:10px; width:100%; background:#2196F3; color:white; border:none; border-radius:4px; cursor:pointer;">Fechar e Continuar Lendo</button>
            `;
            document.getElementById('fecharOvl').onclick = () => overlay.remove();
          });
      });
  };
}