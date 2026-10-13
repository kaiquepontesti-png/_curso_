def calcular_desconto(preco, pct=0.1):
    """Calcular o valor final com desconto."""
    valor_desconto=preco*pct
    preco_final= preco-valor_desconto
    return preco_final

resultado=calcular_desconto(int(input("Qual o valor do item\n")))
print(f"Valor: R${resultado:.2f}")
