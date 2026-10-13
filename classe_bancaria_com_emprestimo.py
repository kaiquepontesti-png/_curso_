class ContaBancaria:
    def __init__(self, saldo_inicial):
        self._valor_empConcedido=0
        self.__taxaJuros=0.08
        self.quatidadeParcelas=0
        self.__saldo=saldo_inicial
        self.__saldoDevedor=0
        self.valor_parcela=0


    def depositar(self, valor):
        if valor>0:
            self.__saldo+=valor
    def get_saldo(self):
        return self.__saldo
    
    def emprestimo(self,emprestimo, quantParcelas):
        self._valor_empConcedido=emprestimo*(1+self.__taxaJuros)
        self.valor_parcela=self._valor_empConcedido/quantParcelas
        self.__saldo+=emprestimo
        self.__saldoDevedor+=self._valor_empConcedido


