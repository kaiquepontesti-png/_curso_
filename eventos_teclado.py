import tkinter as tk

def mudar_texto(event):
    label.config(text="Mensagem Alterada! 🎉")

janela=tk.Tk()
janela.title("evento Enter")
janela.geometry("500x500")
janela.configure(bg='#0F172A')

label=tk.Label(janela, text="Pressione enter",
               bg='#0f172A',
               fg='#38BDF8',
               font=("Arial", 12, "bold"))

label.pack(pady=50)

janela.bind('<Return>', mudar_texto)

janela.mainloop()
