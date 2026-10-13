from classe_locadora import Locadora
from classe_veiculo import Veiculo

locadora = Locadora()

cliente = locadora.cadastro_cliente("Ana", 25)

carro1 = Veiculo("Civic", "ABC-1234", 150)
carro2 = Veiculo("Corolla", "DEF-5678", 180)
carro3 = Veiculo("Onix", "GHI-9012", 100)

locadora.cadastro_carro(carro1)
locadora.cadastro_carro(carro2)
locadora.cadastro_carro(carro3)
print(f"Total de carros cadastrados: {len(locadora.car)}")
for carro in locadora.car:
    print(f"Modelo: {carro.modelo}, Placa: {carro.placa}, Valor da diária: R${carro.valor_diaria}")
modelo_ou_placa = input("Qual carro deseja alugar? Digite o modelo ou a placa:\n")

locadora.alugar_car(cliente, modelo_ou_placa)
locadora.devolver_car(modelo_ou_placa)
locadora.historico_cliente(cliente)
