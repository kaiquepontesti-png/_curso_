from classe_produto_base import Produto

class Carrinho:
    def __init__(self):
        pass
    def adicionar_produtos(self, produto):
        produto_digitado=input("Digite o nome do produto\n")
        produto.nome.append(produto_digitado)
        
        preco_digitado=float(input("\nAgora digite o preço do produto\n"))
        produto.preco.append(preco_digitado)
    
    def remover_produtos(self, produto):
        nome=(input("Digite o nome do produto que deseja excluir\n"))
        produto.nome.remove(nome)
        preco=float(input("Digite o preço do produto que deseja excluir\n"))
        produto.preco.remove(preco)

    def lista_produto(self, produto):
        print(produto.nome)
        print(produto.preco)

    def calcular(self, produto):
        res=sum(produto.preco)
        print(f"Sua compra dew{res:.2f}")
