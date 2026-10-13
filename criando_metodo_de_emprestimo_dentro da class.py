class ContaBancaria:
    def __init__(self, saldo_inicial):
        self.valor_emprestimo=0
        self.valor_empConcedido=0
        self.__taxaJuros=0.08
        self.__quatidadeParcelas=0
        self.__saldo=saldo_inicial
        self.__sacarTudo= saldo_inicial-saldo_inicial


    def depositar(self, valor):
        if valor>0:
            self.__saldo+=valor
    def get_saldo(self):
        return self.__saldo
    def emprestimo(self,emprestimo, quantParcelas):
        emprestimo*(1+(1*self.__taxaJuros))=self.valor_empConcedido
        self.valor_empConcedido/quantParcelas=self.valor_emprestimo


        

conta= ContaBancaria(1000)
conta.depositar(500)
