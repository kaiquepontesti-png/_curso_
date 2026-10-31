const menu = document.getElementById('menu');

// 1 e 2. Abre/fecha o menu pelo botão e fecha ao clicar nos links
document.getElementById('btn-menu').onclick = () => menu.classList.toggle('aberto');
document.querySelectorAll('.menu a').forEach(link => link.onclick = () => menu.classList.remove('aberto'));

// 3. Ativa/desativa o tema escuro (Opcional)
document.getElementById('btn-tema').onclick = () => document.body.classList.toggle('escuro');

// 4. Validação do formulário com mensagem de erro
document.getElementById('form').onsubmit = (evento) => {
    evento.preventDefault();
    const valorNome = document.getElementById('nome').value.trim();
    document.getElementById('erro').innerText = valorNome === '' ? 'Erro: Nome obrigatório!' : '';
    if (valorNome !== '') alert('Enviado!');
};