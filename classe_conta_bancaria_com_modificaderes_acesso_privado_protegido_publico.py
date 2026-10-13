class ContaBancaria:
    def __init__(self, saldo_inicial):
        self.saldoPublico=saldo_inicial
        self._saldoProtegido=saldo_inicial
        self.__saldoPrivado=saldo_inicial
       

    def depositar(self, valor):
        if valor>0:
            self.__saldoPrivado+=valor
    
    def get_saldo(self):
        return self.__saldoPrivado

conta = ContaBancaria(1000)
conta.depositar(500)
pedrim= ContaBancaria(1000)
pedrim.depositar(500)
conta.__saldoPrivado=2000

print(conta.get_saldo())