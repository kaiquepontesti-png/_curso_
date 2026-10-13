
continuar = "1"

while continuar == "1":
    n1 = float(input("Digite o primeiro número: "))
    n2 = float(input("Digite o segundo número: "))
    n3 = float(input("Digite o terceiro número: "))

    print("\nQual operação deseja realizar?")
    print("Soma (opção 1)")
    print("Subtração (opção 2)")
    print("Multiplicação (opção 3)")
    print("Divisão (opção 4)")
    opcao = input("Opção: ")

    resultado = None

    if opcao == "1":
        resultado = n1 + n2 + n3
        operacao = "soma"
    elif opcao == "2":
        resultado = n1 - n2 - n3
        operacao = "subtração"
    elif opcao == "3":
        resultado = n1 * n2 * n3
        operacao = "multiplicação"
    elif opcao == "4":
        if n2 == 0 or n3 == 0:
            print("Não é possível dividir por zero.")
        else:
            resultado = n1 / n2 / n3
            operacao = "divisão"
    else:
        print("Opção inválida.")

    if resultado is not None:
        print(f"O resultado da {operacao} dos seus números é {resultado:g}")

    continuar = input(
        "\nDeseja realizar outra operação?\n"
        "Digite 1 para sim ou 2 para não: "
    )