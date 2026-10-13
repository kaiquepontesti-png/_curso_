import tkinter as tk

def calcular(operacao):
    try:
        num1 = float(entrada1.get())
        num2 = float(entrada2.get())
        if operacao == "+":
            resultado = num1 + num2
        elif operacao == "-":
            resultado = num1 - num2
        elif operacao == "*":
            resultado = num1 * num2
        elif operacao == "/":
            resultado = num1 / num2
        label_resultado.config(text=f"Resultado: {resultado}")
    except ValueError:
        label_resultado.config(text="Por favor, insira números válidos.")

    
app=tk.Tk()
app.title("Calculadora")
app.geometry("1000x300")


entrada1=tk.Entry(app, width=20)
entrada1.pack(pady=10)
entrada2=tk.Entry(app, width=20)
entrada2.pack(pady=10)

botao=tk.Button(app, text="Somar", command=lambda: calcular("+"))
botao.place(x=200, y=110)

botao1=tk.Button(app, text="Subtrair", command=lambda: calcular("-"))
botao1.place(x=400, y=110)

botao2=tk.Button(app, text="Multiplicar", command=lambda: calcular("*"))
botao2.place(x=600, y=110)

botao3=tk.Button(app, text="Dividir", command=lambda: calcular("/"))
botao3.place(x=800, y=110)

label_resultado=tk.Label(app, text="Resultado: ")
label_resultado.pack(pady=10)

app.mainloop()