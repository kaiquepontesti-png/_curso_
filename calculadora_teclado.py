import tkinter as tk

def calcular(operacao):
    try:
        txt1 = entrada1.get().replace("+", "")
        txt2 = entrada2.get().replace("+", "")
        
        # 2. Atualiza as caixas de texto limpando o caractere '+' visualmente
        entrada1.delete(0, tk.END)
        entrada1.insert(0, txt1)
        entrada2.delete(0, tk.END)
        entrada2.insert(0, txt2)
        
        # 3. Faz o cálculo
        num1 = float(txt1)
        num2 = float(txt2)
        resultado = num1 + num2
        label_resultado.config(text=f"Resultado: {resultado}")
    except ValueError:
        label_resultado.config(text="Por favor, insira números válidos.")
    return "break" 
def subt(operacao):
    try:
        txt1 = entrada1.get().replace("-", "")
        txt2 = entrada2.get().replace("-", "")
        
        # 2. Atualiza as caixas de texto limpando o caractere '+' visualmente
        entrada1.delete(0, tk.END)
        entrada1.insert(0, txt1)
        entrada2.delete(0, tk.END)
        entrada2.insert(0, txt2)
        
        # 3. Faz o cálculo
        num1 = float(txt1)
        num2 = float(txt2)
        resultado = num1 - num2
        label_resultado.config(text=f"Resultado: {resultado}")
    except ValueError:
        label_resultado.config(text="Por favor, insira números válidos.")
    return "break" 
def mult(operacao):
    try:
        txt1 = entrada1.get().replace("*", "")
        txt2 = entrada2.get().replace("*", "")
        
        # 2. Atualiza as caixas de texto limpando o caractere '+' visualmente
        entrada1.delete(0, tk.END)
        entrada1.insert(0, txt1)
        entrada2.delete(0, tk.END)
        entrada2.insert(0, txt2)
        
        # 3. Faz o cálculo
        num1 = float(txt1)
        num2 = float(txt2)
        resultado = num1 * num2
        label_resultado.config(text=f"Resultado: {resultado}")
    except ValueError:
        label_resultado.config(text="Por favor, insira números válidos.")
    return "break" 
def div(operacao):
    try:
        txt1 = entrada1.get().replace("/", "")
        txt2 = entrada2.get().replace("/", "")
        
        # 2. Atualiza as caixas de texto limpando o caractere '+' visualmente
        entrada1.delete(0, tk.END)
        entrada1.insert(0, txt1)
        entrada2.delete(0, tk.END)
        entrada2.insert(0, txt2)
        
        # 3. Faz o cálculo
        num1 = float(txt1)
        num2 = float(txt2)
        resultado = num1 / num2
        label_resultado.config(text=f"Resultado: {resultado}")
    except ValueError:
        label_resultado.config(text="Por favor, insira números válidos.")
    return "break" 

app=tk.Tk()
app.title("Calculadora")
app.geometry("400x300")

entrada1=tk.Entry(app, width=20)
entrada1.pack(pady=10)
entrada2=tk.Entry(app, width=20)
entrada2.pack(pady=10)

label_resultado=tk.Label(app, text="Resultado: ")
label_resultado.pack(pady=10)
app.bind('<plus>', calcular)
app.bind('<minus>', subt)
app.bind('<asterisk>', mult)
app.bind('<slash>', div)

app.mainloop()