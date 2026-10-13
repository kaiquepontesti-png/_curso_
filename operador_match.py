bool=True
while True:
    num=int(input("Escreva um numero entre 1 e 3\n       "))
    match num:
        case 1:
            print("Iniciando jogo...")
        case 2:
           print("Carregando configurações")
        case 3:
            print("Saindo do programa. Até logo!")
            break
        case _:
            print("Opção invalida")
