import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

app= tk.Tk()
app.geometry("700x800")

img_pil = Image.open("nice.jpg").resize((300, 300))
dinossauro_pil = Image.open("dinofauro_.jpg").resize((300, 300))

icone_tk = ImageTk.PhotoImage(img_pil)
dinossauro_tk = ImageTk.PhotoImage(dinossauro_pil)

def mudar_imagem():
    nova_imagem = dinossauro_tk if btn.image == icone_tk else icone_tk
    btn.config(image=nova_imagem)
    btn.image = nova_imagem

btn = tk.Button(
    app,
    text="Aperte aqui",
    image=icone_tk,
    compound="left",
    command=mudar_imagem,
    bg="#2563EB",
    fg="#FFFFFF",
    activebackground="#8C17AF",
    activeforeground="#F8FAFC",
)

btn.image = icone_tk
btn.pack(pady=40)

app.mainloop()