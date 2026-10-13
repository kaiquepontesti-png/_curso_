import tkinter as tk
from PIL import Image, ImageTk

app= tk.Tk()
app.title("Exibindo imagem")
app.geometry("700x800")

img_pil= Image.open("nice.jpg")
img_pil=img_pil.resize((700, 700))

imagem_tk= ImageTk.PhotoImage(img_pil)

lbl_img= tk.Label(app, image =imagem_tk)
lbl_img.image=imagem_tk
lbl_img.pack(pady=20)

app.mainloop()