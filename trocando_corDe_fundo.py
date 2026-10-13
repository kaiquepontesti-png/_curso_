import tkinter as tk

janela=tk.Tk()
janela.title("Fundo Personalizado")

janela.configure(bg='#0F172A')

label= tk.Label(janela,
    text= "Tela Roxa!",
    bg='#0F172A',
    fg='#38BDF8',
    font=("Times New Roman", 14, "bold")
    )
label.pack(pady=30)

janela.mainloop()

