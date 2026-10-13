from classe_biblioteca import Biblioteca
from classe_livro import Livro
from classe_aluno import Aluno


bib=Biblioteca()
a1=Aluno("Pedrim")
l1=Livro("Harry Potter")
l2=Livro("As vantagens de ser invisivel")
l3=Livro("Percy Jackson")
bib.cadastro_livro(l1)
bib.cadastro_livro(l2)
bib.cadastro_livro(l3)

voltar_menu=True

while voltar_menu:
    print("-------Bem vindo a biblioteca do senac----------")
    print(f"\nÓla, {a1.nome}")
    print("\nO que gostaria de fazer?")
    opcao=input("\n1- Consultar Livros do acervo\n2- Ver livros disponiveis para emprestimo\n3-Pegar um livro emprestado\n4- Devolver um livro\n5- Ver quais livros você tem por emprestimo\n")

    match opcao:
        case 1:
            bib.listar()
            op=input("\nDeseja realizar outra operação?\n[1]- Sim       [2]- Não  ")
            if op == 1:
                pass
            if op == 2:
                voltar_menu=False
            else:
                print("\nOpção não identificada")
        case 2:
            bib.livros()
            opc=input("Deseja emprestar um livro?\n[1]-Sim    [2]-Não")
            match opc:
                case 1:
                    l=input("Qual livro deseja deseja pegar emprestado?\n")
                    bib.emprestar(l)
                case 2:
                    pass
        case 3:
