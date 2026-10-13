class Carrinho:
    def __init__(self):
        self.produtos=[]

    def adicionar(self, produto):
        self.produtos.append(produto)
    def remover(self, produto):
        if produto in self.produtos:
            self.produtos.remove(produto)
    def lista_produtos(self):
        for p in self.produtos:
            print("Produto:", p.nome, "/ Preço: R$:", p.preco)
    def calcular_total(self):
        total = 0
        for p in self.produtos:
            total = total+p.preco
            return total
