n1=float(input("Digite a primeira nota\n"))
n2=float(input("Digite a segunda nota\n"))
n3=float(input("Digite a terceira nota\n"))
media=(n1+n2+n3)/3
print(f"\nSua nota final é {media:.2f}")
if media<=6:
    print("Você está reprovado")
elif media>=7:
    print("Você esta aprovado")
if n1<media:
    print(f"A nota {n1} ta abaixo da média")
elif n2<media:
    print(f"A nota {n2} ta abaixo da média")
elif n3<media:
    print(f"A nota {n1} ta abaixo da média")
else:
    print("Todas as notas estão acima da média")
