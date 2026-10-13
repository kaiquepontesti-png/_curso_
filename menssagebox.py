import tkinter as tk
from tkinter import messagebox

app=tk.Tk()
app.title("Exemplo Menssagebox")
app.geometry("250x100")

def mostrar_mensagem():
    resp=messagebox.askquestion("Aviso", "Operação realizada!")
    most_resp.config(text=resp)

btn=tk.Button(app, text="Clique Aqui", command=mostrar_mensagem)
btn.pack(pady=20)
most_resp=tk.Label(app, text="resp")
most_resp.pack(pady=30)

app.mainloop()