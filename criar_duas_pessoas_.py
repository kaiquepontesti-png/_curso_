class Pessoa:
    def __init__(self, nome, idade):
          self.nome=nome
          self.idade=idade

    def apresentar(self):
        return f"Olá {self.nome}, você tem {self.idade} anos de idade"
