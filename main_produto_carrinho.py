from classe_produto_base import Produto
from classe_carrinho_resposta import Carrinho

p1= Produto("Creme crack", 6)
p2= Produto("Bolo", 15)
p3= Produto("Farrinha", 5)
p4= Produto("Ovo", 20)
p5= Produto("Refrigerante", 8)

c=Carrinho()
c.adicionar(p1)
c.adicionar(p2)

