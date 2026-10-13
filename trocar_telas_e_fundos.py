import tkinter as tk


def mostrar_tela2():
    frame_tela1.pack_forget()
    frame_tela2.pack(fill="both", expand=True)
def mostrar_tela1():
    frame_tela2.pack_forget()
    frame_tela1.pack(fill="both", expand=True)
def mudar_cor():
    cor_atual=frame_tela2.cget("bg")
    if cor_atual == "#4F7BE4":
        frame_tela2.configure(bg="#DB0000")
    else:
        frame_tela2.configure(bg="#4F7BE4") 

app= tk.Tk()
app.title("Aplicação Multi-Telas"); app.geometry("300x200")

frame_tela1= tk.Frame(app)
label1=tk.Label(frame_tela1, text="Tela 1", bg='#0F172A', fg='#38BDF8', font=("Arial", 14)).pack(pady=20)
but1=tk.Button(frame_tela1, text="Ir para Tela 2", command=mostrar_tela2).pack(pady=10)


frame_tela2= tk.Frame(app, bg="#DF0808",)
tk.Label(frame_tela2,  text="Tela 2", font=("Arial", 14)).pack(pady=20)
but2=tk.Button(frame_tela2, text="mudar cor", command=mudar_cor).pack(pady=10)
but3=tk.Button(frame_tela2, text="Ir para Tela 1", command=mostrar_tela1).pack(pady=20)



frame_tela1.pack(fill="both", expand=True)
app.mainloop()