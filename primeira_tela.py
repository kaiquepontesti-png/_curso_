import tkinter as tk
from pathlib import Path
def ler():                   #ou with_name("Ferramentas -Python.text")
    caminho = Path(__file__).parent/"Ferramentas-Python.txt"
    try:
        print(caminho.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("Arquivo Ferramentas-Python.txt não encontrado.")


janela=tk.Tk()
janela.title("Minha Primeira Tela")
janela.geometry("400x300")
fala=tk.Label(janela, text="Olá, Mundo!", bg="#000000", fg="#1127F3", font=("Times New Roman", 20))
fala.pack(pady=10)
botao=tk.Button(janela, text="Clique aqui", command=ler, bg="#D10606", fg='#FFFFFF')
botao.pack(pady=30)
janela.mainloop()