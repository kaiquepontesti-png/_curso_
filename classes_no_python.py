class Pessoa:
    def __init__(self,nome,idade):
        self.nome=nome
        self.idade=idade

    def apresentar(self):
        return f"Olá, sou {self.nome}"

p1= Pessoa("Dimi Neutron", 15)
p2= Pessoa("Cleitinho", 18)
p3= Pessoa("Vampeta", 56)
p4= Pessoa("Neto", 40)
print(p4.apresentar())