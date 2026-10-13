class Conta:
    def __init__(self, nome, saldo):
        self.nome = nome
        self.saldo = saldo

    def extrato(self):
        print(f"Saldo: {self.saldo}")