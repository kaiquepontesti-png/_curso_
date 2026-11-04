const existente = document.getElementById("manga-tradutor-overlay");
if (existente) existente.remove();

let imagemDeFundoUrl = "";
let idiomaAtual = "kor"; 

chrome.runtime.onMessage.addListener((request) => {
  if (request.acao === "iniciarSelecao") {
    imagemDeFundoUrl = request.imagemUrl;
    idiomaAtual = request.idioma; 
    iniciarFerramentaDeRecorte();
  }
});

function iniciarFerramentaDeRecorte() {
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
    overlay.style.pointerEvents = "none"; 
    overlay.style.background = "rgba(0,0,0,0.6)"; 
    
    const rect = selecao.getBoundingClientRect();
    if (rect.width > 10 && rect.height > 10) {
      processarRecorte(rect, overlay);
    } else {
      overlay.remove(); 
    }
  });
}

function processarRecorte(rect, overlay) {
  const canvas = document.createElement("canvas");
  canvas.width = rect.width;
  canvas.height = rect.height;
  const ctx = canvas.getContext("2d");

  const img = new Image();
  img.src = imagemDeFundoUrl;
  
  img.onload = () => {
    ctx.drawImage(img, rect.left, rect.top, rect.width, rect.height, 0, 0, rect.width, rect.height);
    const imagemRecortadaBase64 = canvas.toDataURL("image/png");
    
    executarOCR(imagemRecortadaBase64, overlay);
  };
}

function executarOCR(imagem64, overlay) {
  overlay.innerHTML = `<div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); background:white; padding:20px; border-radius:8px; color:black; font-family:sans-serif; text-align:center; min-width:300px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); pointer-events:auto;">
    <h3 style="margin-top:0;">Lendo a imagem...</h3>
    <p>Baixando pacotes ou extraindo texto. Aguarde...</p>
  </div>`;
  const container = overlay.querySelector('div');

  const script = document.createElement('script');
  script.src = "https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js";
  document.head.appendChild(script);

  script.onload = () => {
    Tesseract.recognize(imagem64, idiomaAtual)
      .then(resultado => {
        const textoExtraido = resultado.data.text.trim();
        if (textoExtraido.length < 1) {
          container.innerHTML = `<h3>Erro</h3><p>Nenhum texto legível encontrado.</p><button id="fecharOvl" style="padding:10px; width:100%; background:#2196F3; color:white; border:none; border-radius:4px; cursor:pointer;">Fechar</button>`;
          document.getElementById('fecharOvl').onclick = () => overlay.remove();
          return;
        }

        container.innerHTML = `<h3>Traduzindo...</h3><p>${textoExtraido}</p>`;
        
        const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=pt&dt=t&q=${encodeURI(textoExtraido)}`;
        
        fetch(url)
          .then(res => res.json())
          .then(data => {
            const textoTraduzido = data[0].map(p => p[0]).join("");
            container.innerHTML = `
              <h3 style="margin-top:0;">Resultado:</h3>
              <textarea style="width:100%; height:60px; margin-bottom:10px; resize:none;">${textoExtraido}</textarea>
              <textarea style="width:100%; height:60px; margin-bottom:10px; background:#f5f5f5; resize:none;">${textoTraduzido}</textarea>
              <button id="fecharOvl" style="padding:10px; width:100%; background:#2196F3; color:white; border:none; border-radius:4px; cursor:pointer;">Fechar</button>
            `;
            document.getElementById('fecharOvl').onclick = () => overlay.remove();
          })
          .catch(erro => {
            container.innerHTML = `<h3>Erro no Google Tradutor</h3><p>${erro.message}</p><button id="fecharOvl" style="padding:10px; width:100%; background:#2196F3; color:white; border:none; border-radius:4px; cursor:pointer;">Fechar</button>`;
            document.getElementById('fecharOvl').onclick = () => overlay.remove();
          });
      })
      .catch(erro => {
        container.innerHTML = `<h3>Erro no Leitor (OCR)</h3><p>Falha na leitura ou bloqueio de rede: ${erro}</p><button id="fecharOvl" style="padding:10px; width:100%; background:#2196F3; color:white; border:none; border-radius:4px; cursor:pointer;">Fechar</button>`;
        document.getElementById('fecharOvl').onclick = () => overlay.remove();
      });
  };
  
  script.onerror = () => {
    container.innerHTML = `<h3>Erro de Segurança (CSP)</h3><p>O site impede que scripts externos sejam rodados. O motor Tesseract não pôde ser carregado.</p><button id="fecharOvl" style="padding:10px; width:100%; background:#2196F3; color:white; border:none; border-radius:4px; cursor:pointer;">Fechar</button>`;
    document.getElementById('fecharOvl').onclick = () => overlay.remove();
  };
}