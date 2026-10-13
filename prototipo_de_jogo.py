import tkinter as tk
from PIL import Image, ImageTk

def game_start():
        frame_menu.pack_forget()
        frame_jogo.pack()

jogo=tk.Tk()
frame_menu=tk.Frame(jogo)
frame_jogo=tk.Frame(jogo)
frame_tutorial=tk.Frame(jogo)
frame_menu.pack()
jogo.title("Prototipo de jogo")
frame_menu.pack(fill='both', expand=True)
disco=ImageTk.PhotoImage(Image.open("disco.png"))
imagem=ImageTk.PhotoImage(Image.open("campo.jpg"))
backg_menu = tk.Label(frame_menu, image=imagem)
backg_menu.pack(fill='both', expand=True)
jogo.attributes('-fullscreen', True)
campo_jogo=tk.Label(frame_jogo, image=imagem)
campo_jogo.pack(fill='both', expand=True)
backg_tutorial = tk.Label(frame_tutorial, image=imagem)
backg_tutorial.pack(fill='both', expand=True)
backg_menu.image = imagem
campo_jogo.image = imagem
backg_tutorial.image = imagem

tut1=tk.Label(frame_tutorial, text=" Utilize as teclas  S e W do teclado para\nmover o skate do lado equerdo")
tut2=tk.Label(frame_tutorial, text=" Utilize as teclas  seta para cima e seta para baixo do teclado\npara mover o skate do lado direito")
tut3=tk.Label(frame_tutorial, text=" O jogo termina ao marcar 5 pontos")
tut4=tk.Label(frame_tutorial, text=" Você marca ponto quando a bola enconta no gol do adverario")
btn_start=tk.Button(jogo, text="Começar jogo", command=game_start)
btn_start.pack(pady=50)

jogo.mainloop()