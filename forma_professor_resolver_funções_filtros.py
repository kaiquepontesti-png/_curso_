def analisar_notas(notas):
    media = sum(notas) / len(notas)
    # Coleta as notas acima da média usando laço tradicional
    acima = []
    for n in notas:
        if n > media:
            acima.append(n)
    # Conta quantas notas são maiores ou iguais a 7.0
    aprovados = 0
    for n in notas:
        if n >= 7.0:
            aprovados += 1
    return media, acima, aprovados
# Teste da função
dados = [5.5, 8.0, 9.5, 6.0, 7.5, 4.0]
media, acima, aprovados = analisar_notas(dados)
print(f"Média: {media:.2f}")
print(f"Notas acima da média: {acima}")
print(f"Quantidade de aprovados: {aprovados}")