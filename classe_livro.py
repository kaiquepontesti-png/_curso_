class Livro:
    def __init__(self, titulo):
        self.titulo = titulo
        self.__disponibilidade = True

    def esta_disponivel(self):
        return self.__disponibilidade

    def set_indisponivel(self):
        self.__disponibilidade = False

    def set_devolvido(self):
        self.__disponibilidade = True
