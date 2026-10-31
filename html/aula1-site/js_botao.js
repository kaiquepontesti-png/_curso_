const botao = document.getElementById("botao");
const titulo = document.getElementById("inicio");

botao.addEventListener("click", function () {
    titulo.textContent = "Bem-vindo ao Senac";
    botao.classList.add("clicado");
});