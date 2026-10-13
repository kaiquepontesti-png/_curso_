import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

app=tk.Tk()
app.title("Jogo da bolinha")
largura, altura= campo_pil.size
app.geometry(f"{largura}x{altura}")
canvas=tk.Canvas(app, width=largura, height=altura)
canvas.pack()
campo_pil = Image.open("campo.jpg")
campo_tk = ImageTk.PhotoImage(campo_pil)


canvas.create_image(400, 300, image=campo_tk)
canvas.imagem = campo_tk 




app.mainloop()