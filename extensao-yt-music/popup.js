document.getElementById('btn-listar').addEventListener('click', async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab.url.includes("music.youtube.com")) {
        document.getElementById('lista-texto').value = "Por favor, abra uma página do YouTube Music.";
        return;
    }

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: varrerPaginaYT
    }, (resultados) => {
        // Agora usamos 2 quebras de linha para separar melhor cada música
        const textoExtraido = resultados[0].result.join('\n\n');
        document.getElementById('lista-texto').value = textoExtraido;
        
        if (textoExtraido.length > 0 && !textoExtraido.includes("Nenhuma música")) {
            document.getElementById('btn-copiar').style.display = 'block';
        }
    });
});

document.getElementById('btn-copiar').addEventListener('click', () => {
    const texto = document.getElementById('lista-texto').value;
    navigator.clipboard.writeText(texto).then(() => {
        const btn = document.getElementById('btn-copiar');
        btn.innerText = "Copiado com sucesso!";
        setTimeout(() => { btn.innerText = "Copiar Tudo"; }, 2000);
    });
});

// A função atualizada que roda dentro da página do YT Music
function varrerPaginaYT() {
    let lista = [];
    
    let linhas = document.querySelectorAll('ytmusic-responsive-list-item-renderer');
    
    if(linhas.length > 0) {
        linhas.forEach(linha => {
            let colunas = linha.querySelectorAll('.flex-columns .yt-formatted-string');
            if(colunas.length > 1) {
                let titulo = colunas[0].innerText;
                let artista = colunas[1].innerText;
                
                // Busca a tag <a> que contém o link da música
                let linkElemento = colunas[0].querySelector('a') || linha.querySelector('a');
                let link = linkElemento ? linkElemento.href : "Link não encontrado";
                
                // Limpa o link para remover dados de playlist (&list=...)
                if(link.includes('&list=')) {
                    link = link.split('&list=')[0];
                }
                
                // Formata o texto final: Título - Artista e o link embaixo
                lista.push(`${titulo} - ${artista}\n🔗 ${link}`);
            }
        });
    } else {
        // Se estiver apenas tocando uma música na barra inferior
        let tituloAtual = document.querySelector('yt-formatted-string.title')?.innerText;
        let artistaAtual = document.querySelector('.byline.ytmusic-player-bar')?.innerText;
        
        let linkElemento = document.querySelector('yt-formatted-string.title a');
        let linkAtual = linkElemento ? linkElemento.href : "Link não encontrado";
        
        if(tituloAtual) {
            lista.push(`${tituloAtual} - ${artistaAtual || ''}\n🔗 ${linkAtual}`);
        } else {
            lista.push("Nenhuma música listada encontrada na tela.");
        }
    }
    
    return lista;
}
// teste de atualizacao