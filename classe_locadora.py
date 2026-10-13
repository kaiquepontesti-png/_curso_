from classe_veiculo import Veiculo
from classe_cliente import Cliente
class Locadora:
    def __init__(self):
        self.car = []
        self.__cliente = []
        self.alugados = []
         

    def cadastro_cliente(self, nome, idade):
        if type(nome) == str and type(idade) == int:
            novo_cliente = Cliente(nome, idade)
            self.__cliente.append(novo_cliente)
            print(f"Cliente {nome} cadastrado com sucesso!")
            return novo_cliente
        print("Cliente só pode receber caracteres e idade só pode receber números inteiros.")
        return None

    def cadastro_carro(self, carro):
        self.car.append(carro)

    def alugar_car(self, cliente, modelo_ou_placa):
        for carro in self.car:
            if carro.modelo == modelo_ou_placa or carro.placa == modelo_ou_placa:
                if carro.status == 1:
                    dias=int(input("Digite quantos dias de locação:\n"))
                    carro.dias_alugados = dias
                    carro.status = 0
                    self.alugados.append(carro)
                    cliente.historico.append({
                        "modelo": carro.modelo,
                        "placa": carro.placa,
                        "dias": dias,
                        "valor_diaria": carro.valor_diaria
                    })
                    print(f"O carro '{carro.modelo}' foi alugado com sucesso!")
                else:
                    print(f"O carro '{carro.modelo}' já está alugado.")
                return
        print(f"Carro '{modelo_ou_placa}' não encontrado.")

    def devolver_car(self, modelo_ou_placa):
        for carro in self.car:
            if (carro.modelo == modelo_ou_placa or carro.placa == modelo_ou_placa):
                if carro.status == 0:
                    carro.status = 1
                    self.alugados.remove(carro)
                    print(f"O carro '{carro.modelo}' foi devolvido com sucesso!")
                    print(f"\nValor total da locação:\nR${carro.dias_alugados * carro.valor_diaria}\nQual a forma de pagamento?")
                else:
                    print(f"O carro '{carro.modelo}' não está alugado.")
                return

        print(f"Carro '{modelo_ou_placa}' não encontrado.")

    def historico_cliente(self, cliente):
        if cliente in self.__cliente:
            print(f"Histórico de locações do cliente '{cliente.nome}':")
            for registro in cliente.historico:
                print(f"Modelo: {registro['modelo']}, Placa: {registro['placa']}, Dias: {registro['dias']}, Valor da diária: R${registro['valor_diaria']}")
        else:
            print(f"Cliente '{cliente.nome}' não encontrado.")