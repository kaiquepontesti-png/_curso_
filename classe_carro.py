class Carro:
    def __init__(self, marca, modelo, ano):
        self.marca=marca
        self.modelo=modelo
        self.ano=ano

    def exibir_dados(self):
        return f"A marca do carro é {self.marca}, do modelo {self.modelo} do ano {self.ano}"

