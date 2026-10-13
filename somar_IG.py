import tkinter as tk

app = tk.Tk()
app.title("Calculadora")
app.geometry("300x250")

tk.Label(app, text="Primeiro número:").pack(pady=(10, 0))
entry1 = tk.Entry(app)
entry1.pack(pady=5)

tk.Label(app, text="Segundo número:").pack()
entry2 = tk.Entry(app)
entry2.pack(pady=5)

frame_botoes = tk.Frame(app)
frame_botoes.pack(pady=10)

lbl_res = tk.Label(app, text="Resultado:")
lbl_res.pack(pady=10)

app.mainloop()
