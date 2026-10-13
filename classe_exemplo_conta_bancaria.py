class ContaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular=titular
        self.saldo=saldo
    def depositar(self, valor):
        self.saldo+=valor
    def sacar(self, valor):
        if self.saldo>=valor:
            self.saldo -= valor

c1= ContaBancaria("Maria", 1000)
c1.depositar(500)
print(f"Saldo de {c1.titular}: r${c1.saldo}")
c1.sacar(200)
print(f"Saldo de {c1.titular}: r${c1.saldo}")
c1.sacar(100)
print(f"Saldo de {c1.titular}: r${c1.saldo}")