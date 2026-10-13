from classe_conta import Conta

class ContaPP(Conta):
    def __init__(self, nome, saldo, taxa_j):
        super().__init__(nome, saldo)
        self.taxa_j = taxa_j

    def render_juros(self):
        self.saldo += self.saldo * self.taxa_j 
        return self.saldo

