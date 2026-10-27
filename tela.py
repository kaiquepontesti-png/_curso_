import tkinter as tk
from tkinter import messagebox, ttk
from banco import salvar_contato, listar_nomes, excluir_nome, salvar_telefone

def cadastrar():
    nome = entry_nome.get().strip()
    telefone = entry_telefone.get().strip()

    if not nome:
        messagebox.showwarning("Aviso", "Por favor, digite um nome!")
        return

    if not telefone:
        messagebox.showwarning("Aviso", "Por favor, digite um número!")
        return

    try:
        salvar_contato(nome, telefone)
        messagebox.showinfo("Sucesso", "Contato salvo com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")

def excluir():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um nome na tabela para excluir!")
        return

    item = tree.item(selecionado[0])
    registro_id = item["values"][0]
    registro_nome = item["values"][1]

    if messagebox.askyesno("Confirmar", f"Deseja realmente excluir '{registro_nome}' (ID: {registro_id})?"):
        try:
            excluir_nome(registro_id)
            messagebox.showinfo("Sucesso", "Nome excluído com sucesso!")
            atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {e}")

def pesquisar():
    termo = entry_pesquisa.get().strip()
    atualizar_tabela(termo)

def limpar_pesquisa():
    entry_pesquisa.delete(0, tk.END)
    atualizar_tabela()

def atualizar_tabela(pesquisa=""):
    for item in tree.get_children():
        tree.delete(item)
    registros= listar_nomes(pesquisa)
    for reg in registros:
        tree.insert("", tk.END, values=(reg.id, reg.nome, reg.telefone))

janela= tk.Tk()
janela.title("Cadastro Simples")
janela.geometry("500x600")

label_instrucao= tk.Label(janela, text= "Digite o nome: ")
label_instrucao.pack(pady=(25,5))

entry_nome= tk.Entry(janela, width=28)
entry_nome.pack(pady=5)

label_instrucao2= tk.Label(janela, text= "Digite o numero: ")
label_instrucao2.pack(pady=(35,5))

entry_telefone= tk.Entry(janela, width=28)
entry_telefone.pack(pady=10)

btn_salvar= tk.Button(janela, text="Salvar", width=12, command=cadastrar)
btn_salvar.pack(pady=20)

frame_pesquisa= tk.Frame(janela)
frame_pesquisa.pack(pady=10)

entry_pesquisa= tk.Entry(frame_pesquisa, width=18)
entry_pesquisa.pack(side= "left", padx=2)

btn_todos= tk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar)
btn_todos.pack(side="left", padx=2)

btn_limpar = tk.Button(frame_pesquisa, text="Limpar", command=limpar_pesquisa)
btn_limpar.pack(side="left", padx=2)

colunas= ("id", "nome", "telefone")
tree= ttk.Treeview(janela, columns=colunas, show="headings", height=8)
tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.heading("telefone", text="telefone")
tree.column("id", width=50, anchor="center")
tree.column("nome", width=200)
tree.column("telefone", width=200)

tree.pack(padx=20, pady=5, fill="both", expand=True)

btn_excluir = tk.Button(janela, text="Excluir Selecionado", bg="#ec1111", command=excluir)
btn_excluir.pack(pady=10)

try:
    atualizar_tabela()
except Exception as e:
    print(f"Erro ao carregar dados: {e}")

janela.mainloop()