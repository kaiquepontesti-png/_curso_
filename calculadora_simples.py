num1=float(input("Digite o primeiro numero\n"))
num2=float(input("Digite o segundo numero\n"))
soma= num1+num2
sub= num1-num2
mult= num1*num2
div= num1/num2
oper=int(input("Qual operação deseja executar?\n Soma[1] -- Subtração[2] -- Multiplicação[3] -- Divisão[4]\n"))
match oper:
    case 1:
        print(f"Seu resultado é {soma}")
    case 2:
        print(f"Seu resultado é {sub}")
    case 3:
        print(f"Seu resultado é {mult}")
    case 4:
        print(f"Seu resultado é {div}")
    case _:
        print("Opção invalida")