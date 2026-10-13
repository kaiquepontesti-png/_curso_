from classe_livro import Livro

class Biblioteca:
    def __init__(self):
        self.l_livros = []
        self.livros_aluno = []

    def cadastro_livro(self, livro):
        self.l_livros.append(livro)

    def listar(self):
        for p in self.l_livros:
            print(p.titulo)

    def listar_aluno(self):
        for p in self.livros_aluno:
            print(p.titulo)

    def livros(self):
        print("--- Livros Disponíveis para Empréstimo ---")
        for livro in self.l_livros:
            if livro.esta_disponivel():
                print(livro.titulo)

    def emprestar(self, nome_livro):
        for livro in self.l_livros:
            if livro.titulo==nome_livro:
                if livro.esta_disponivel():
                    livro.set_indisponivel()
                    self.livros_aluno.append(livro)
                    print(f"O livro '{livro.titulo}' foi emprestado com sucesso!")
                    return
                else:
                    print(f"O livro '{nome_livro}' já está emprestado.")
                    return
        
        print(f"O livro '{nome_livro}' não foi encontrado na biblioteca.")

    def devolver(self, nome_livro):
        for livro in self.l_livros:
            if livro.titulo == nome_livro:
                if not livro.esta_disponivel():
                    livro.set_devolvido()
                    # Remove da lista de livros do aluno se ele estiver lá
                    if livro in self.livros_aluno:
                        self.livros_aluno.remove(livro)
                    print(f"O livro '{nome_livro}' foi devolvido com sucesso!")
                    return
                else:
                    print(f"O livro '{nome_livro}' já está na biblioteca.")
                    return
                    
        print(f"O livro '{nome_livro}' não foi encontrado na biblioteca.")