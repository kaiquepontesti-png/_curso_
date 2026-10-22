import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Banco de dados fictício direto no Python
CARDAPIO = [
    {"nome": "Calabresa", "preco": 42.00, "ingredientes": "Molho de tomate, muçarela, calabresa fatiada e cebola."},
    {"nome": "Margherita", "preco": 45.00, "ingredientes": "Molho de tomate, muçarela, rodelas de tomate e manjericão fresco."},
    {"nome": "Frango com Catupiry", "preco": 48.00, "ingredientes": "Molho de tomate, frango desfiado e o legítimo Catupiry."},
    {"nome": "Quatro Queijos", "preco": 52.00, "ingredientes": "Muçarela, catupiry, provolone e gorgonzola."}
]

# Código HTML e JavaScript embutido para rodar como arquivo único
HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pizzaria Bella Itália - Teste Rápido</title>
    <style>
        :root { --primary: #e74c3c; --dark: #2c3e50; --light: #f8f9fa; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background-color: var(--light); color: var(--dark); }
        header { background-color: var(--dark); color: white; padding: 20px; text-align: center; border-bottom: 5px solid var(--primary); }
        .container { max-width: 1000px; margin: 20px auto; padding: 0 20px; }
        .pizza-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
        .pizza-card { background: white; border-radius: 8px; padding: 15px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .pizza-info h3 { margin-bottom: 8px; }
        .pizza-info p { font-size: 0.9rem; color: #666; margin-bottom: 15px; }
        .price { font-size: 1.2rem; font-weight: bold; color: var(--primary); margin-bottom: 10px; }
        button { background-color: var(--primary); color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.2s; }
        button:hover { background-color: #c0392b; }
        #cart { margin-top: 40px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .cart-item { display: flex; justify-content: space-between; margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #ddd; }
        .whatsapp-btn { background-color: #25d366; margin-top: 15px; }
        .whatsapp-btn:hover { background-color: #128c7e; }
    </style>
</head>
<body>

    <header>
        <h1>🍕 Pizzaria Bella Itália</h1>
        <p>Protótipo em arquivo único Python + Flask</p>
    </header>

    <div class="container">
        <h2>Nosso Cardápio</h2>
        
        <div class="pizza-grid">
            {% for pizza in pizzas %}
            <div class="pizza-card">
                <div class="pizza-info">
                    <h3>{{ pizza.nome }}</h3>
                    <p>{{ pizza.ingredientes }}</p>
                </div>
                <div>
                    <div class="price">R\$ {{ "%.2f"|format(pizza.preco) }}</div>
                    <button onclick="adicionarAoCarrinho('{{ pizza.nome }}', {{ pizza.preco }})">Adicionar</button>
                </div>
            </div>
            {% endfor %}
        </div>

        <div id="cart">
            <h2>Seu Pedido</h2>
            <div id="cart-items" style="margin-top: 15px;"><p>O carrinho está vazio.</p></div>
            <h3 id="cart-total" style="margin-top: 15px; text-align: right; display: none;">Total: R\$ 0,00</h3>
            <button class="whatsapp-btn" id="send-btn" style="display: none;" onclick="enviarWhatsApp()">Enviar Pedido pelo WhatsApp</button>
        </div>
    </div>

    <script>
        let carrinho = [];
        let total = 0;
        const NUMERO_WHATSAPP = "5511999999999"; // Substitua pelo seu WhatsApp comercial

        function adicionarAoCarrinho(nome, preco) {
            carrinho.push({ nome, preco });
            atualizarCarrinho();
        }

        function atualizarCarrinho() {
            const itensDiv = document.getElementById('cart-items');
            const totalH3 = document.getElementById('cart-total');
            const btnEnviar = document.getElementById('send-btn');
            
            if (carrinho.length === 0) {
                itensDiv.innerHTML = '<p>O carrinho está vazio.</p>';
                totalH3.style.display = 'none';
                btnEnviar.style.display = 'none';
                return;
            }

            itensDiv.innerHTML = '';
            total = 0;

            carrinho.forEach((item) => {
                total += item.preco;
                itensDiv.innerHTML += `<div class="cart-item"><span>${item.nome}</span><span>R$ ${item.preco.toFixed(2)}</span></div>`;
            });

            totalH3.innerText = `Total: R$ ${total.toFixed(2)}`;
            totalH3.style.display = 'block';
            btnEnviar.style.display = 'block';
        }

        function enviarWhatsApp() {
            let texto = "Olá! Gostaria de fazer o seguinte pedido:\\n\\n";
            carrinho.forEach(item => { texto += `• 1x Pizza de ${item.nome} - R$ ${item.preco.toFixed(2)}\\n`; });
            texto += `\\n*Total: R$ ${total.toFixed(2)}*`;
            window.open(`https://whatsapp.com{NUMERO_WHATSAPP}&text=${encodeURIComponent(texto)}`, '_blank');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    # Renderiza a string HTML injetando a lista de pizzas
    return render_template_string(HTML_PAGE, pizzas=CARDAPIO)

if __name__ == '__main__':
    print("\n🚀 Servidor Iniciado com Sucesso!")
    print("👉 Clique no link ou abra no navegador: http://127.0.0.1:5000 \n")
    app.run(debug=True, port=5000)
    