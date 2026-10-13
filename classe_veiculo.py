class Veiculo:
    def __init__(self, modelo, placa, valor_diaria):
        self.modelo=modelo
        self.placa=placa
        self.valor_diaria=valor_diaria
        self.status=1
        self.dias_alugados = 0
