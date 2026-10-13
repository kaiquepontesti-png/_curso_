def analisar_notas(lista_de_notas):
    media=sum(lista_de_notas)/len(lista_de_notas)
    filtro_de_notas=list(filter(lambda x: x>7, lista_de_notas))
    quantidade_aprovados = len(filtro_de_notas)
    print(f"As notas aprovadas são {filtro_de_notas}")
    print(f"\nA média é {media}")
    print(f"Os alunos aprovados são: {quantidade_aprovados}")
           
notas=[5.5, 8.0, 9.5, 6.0, 7.5, 4.0]

analisar_notas(notas)