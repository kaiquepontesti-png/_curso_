class Produto:
    def __init__(self, nome, preco):
        self.nome=nome
        self.preco=preco
        self.precoDesconto=0
        self.percentual=0.1

    def apl_desconto(self):
        self.precoDesconto = self.preco*self.percentual
        self.preco-=self.precoDesconto
        return f"Com o desconto custa R${self.preco:.2f}"

    def exibir_produtos(self):
        return f"Temos o produto {self.nome}, custando R${self.preco}"
    

