from classe_conta import Conta
class ContaCor(Conta):
    def __init__(self, nome, saldo, limite):
        super().__init__(nome, saldo)
        self.limite=limite
        
    def extrato(self):
        self.saldo += self.limite
        print(f'Saldo: {self.saldo}')
    