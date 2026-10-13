from classe_veiculo_heranca import Veiculo
class Carro(Veiculo):
    def __init__(self, marca, portas):
        super().__init__(marca)
        self.portas=portas
    def ligar(self):
        print(f'Carro {self.marca} está ligado.')
