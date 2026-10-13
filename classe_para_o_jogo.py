from prototipo_de_jogo import frame_menu, frame_jogo, jogo, frame_tutorial
class Metodo_jogo:
    def __init__(self):
        pass
    

    def sair_jogo():
        jogo.destroy()

    def pausar_jogo():
        pass
    def retorn_menuJ():
        frame_jogo.pack_forget()
        frame_jogo.destroy()
        frame_menu.pack()
    def retorn_menuT():
        frame_tutorial.pack_forget()
        frame_tutorial.destroy()
        frame_tutorial.pack()
