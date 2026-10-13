import tkinter as tk


janela = tk.Tk()
janela.title("Minha Calculadora")

janela.geometry("1200x1200")

label= tk.Label(janela, text="Olá, Mundo!")
label.place(y=350, x=600)

def ao_clicar():
    cal=10+10+10*2
    label.config(text=f"Botão clicado! {cal}")

botao = tk.Button(janela, text="Clique aqui", command=ao_clicar)
botao.place(y=400, x=600)


janela.mainloop()