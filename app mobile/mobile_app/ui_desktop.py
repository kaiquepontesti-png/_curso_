import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, Set

from .models import ListaDeCompras, formatar_moeda_brl
from .storage import ArmazenamentoLocal


class NumEsqueceMobileApp:
    """
    Interface gráfica nativa em Python (Tkinter) em formato mobile (Android / iOS),
    conectada diretamente às classes de memória local (ArmazenamentoLocal).
    Sem servidor web, sem Flask e sem banco de dados externo.
    """

    COR_FUNDO = "#FFFFFF"
    COR_PRETO = "#000000"
    COR_CINZA = "#757575"
    COR_CINZA_CLARO = "#F4F4F4"
    COR_VERMELHO = "#B91C1C"

    def __init__(self, armazenamento: Optional[ArmazenamentoLocal] = None):
        self.storage = armazenamento or ArmazenamentoLocal()
        self.lista_atual_id: Optional[int] = None
        self.itens_no_carrinho: Set[int] = set()

        self.root = tk.Tk()
        self.root.title("NumEsquece Lista · Mobile")
        self.root.geometry("412x760")
        self.root.configure(bg=self.COR_FUNDO)
        self.root.resizable(False, False)

        self._construir_chrome()
        self.mostrar_inicio()

    def _construir_chrome(self):
        # Topbar fixa Neo-Brutalist
        self.topbar = tk.Frame(
            self.root, bg=self.COR_FUNDO, height=58, highlightthickness=2, highlightbackground=self.COR_PRETO
        )
        self.topbar.pack(side=tk.TOP, fill=tk.X)
        self.topbar.pack_propagate(False)

        brand = tk.Label(
            self.topbar,
            text="📝 NumEsquece Lista",
            bg=self.COR_FUNDO,
            fg=self.COR_PRETO,
            font=("Segoe UI", 13, "bold"),
            cursor="hand2",
        )
        brand.pack(side=tk.LEFT, padx=14)
        brand.bind("<Button-1>", lambda e: self.mostrar_inicio())

        btn_nova = tk.Button(
            self.topbar,
            text="+ Nova Lista",
            bg=self.COR_PRETO,
            fg=self.COR_FUNDO,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.mostrar_criar_lista,
        )
        btn_nova.pack(side=tk.RIGHT, padx=12, pady=10)

        # Área principal rolável
        self.container_scroll = tk.Frame(self.root, bg=self.COR_FUNDO)
        self.container_scroll.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.container_scroll, bg=self.COR_FUNDO, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.container_scroll, orient="vertical", command=self.canvas.yview)
        self.frame_conteudo = tk.Frame(self.canvas, bg=self.COR_FUNDO, padx=14, pady=14)

        self.frame_conteudo.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_conteudo, anchor="nw", width=394)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Barra de Navegação Inferior Mobile
        self.bottom_nav = tk.Frame(
            self.root, bg=self.COR_FUNDO, height=62, highlightthickness=2, highlightbackground=self.COR_PRETO
        )
        self.bottom_nav.pack(side=tk.BOTTOM, fill=tk.X)
        self.bottom_nav.pack_propagate(False)

        abas = [
            ("🏠\nInício", self.mostrar_inicio, False),
            ("📋\nListas", self.mostrar_minhas_listas, False),
            ("➕\nNova", self.mostrar_criar_lista, True),
            ("📜\nHistórico", self.mostrar_historico, False),
        ]
        for texto, cmd, destaque in abas:
            btn = tk.Button(
                self.bottom_nav,
                text=texto,
                bg=self.COR_PRETO if destaque else self.COR_FUNDO,
                fg=self.COR_FUNDO if destaque else self.COR_PRETO,
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                cursor="hand2",
                command=cmd,
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=6)

    def _limpar_tela(self):
        for w in self.frame_conteudo.winfo_children():
            w.destroy()
        self.canvas.yview_moveto(0)

    def _criar_cabecalho(self, eyebrow: str, titulo: str, subtitulo: str):
        card = self._criar_card()
        tk.Label(
            card, text=eyebrow.upper(), bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")
        tk.Label(
            card,
            text=titulo,
            bg=self.COR_FUNDO,
            fg=self.COR_PRETO,
            font=("Segoe UI", 16, "bold"),
            wraplength=340,
            justify="left",
        ).pack(anchor="w")
        tk.Label(
            card,
            text=subtitulo,
            bg=self.COR_FUNDO,
            fg="#4A4A4A",
            font=("Segoe UI", 9),
            wraplength=340,
            justify="left",
        ).pack(anchor="w", pady=(2, 0))

    def _criar_card(self) -> tk.Frame:
        card = tk.Frame(
            self.frame_conteudo,
            bg=self.COR_FUNDO,
            highlightbackground=self.COR_PRETO,
            highlightthickness=2,
            padx=14,
            pady=14,
        )
        card.pack(fill=tk.X, pady=(0, 14))
        return card

    # --- TELAS ---

    def mostrar_inicio(self):
        self._limpar_tela()
        self._criar_cabecalho("Caderno Móvel", "Minhas Compras", "Armazenamento local por classes (100% offline).")

        card = self._criar_card()
        tk.Label(card, text="Acesso Rápido", bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 12, "bold")).pack(
            anchor="w", pady=(0, 10)
        )

        tk.Button(
            card,
            text="📋 Ver Minhas Listas",
            bg=self.COR_PRETO,
            fg=self.COR_FUNDO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            pady=10,
            cursor="hand2",
            command=self.mostrar_minhas_listas,
        ).pack(fill=tk.X, pady=(0, 8))

        tk.Button(
            card,
            text="➕ Criar Nova Lista",
            bg=self.COR_FUNDO,
            fg=self.COR_PRETO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.SOLID,
            bd=1,
            pady=10,
            cursor="hand2",
            command=self.mostrar_criar_lista,
        ).pack(fill=tk.X, pady=(0, 8))

        tk.Button(
            card,
            text="📜 Histórico de Gastos",
            bg=self.COR_FUNDO,
            fg=self.COR_PRETO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.SOLID,
            bd=1,
            pady=10,
            cursor="hand2",
            command=self.mostrar_historico,
        ).pack(fill=tk.X)

    def mostrar_minhas_listas(self):
        self._limpar_tela()
        self._criar_cabecalho("Organização", "Minhas Listas", "Toque para adicionar produtos, importar arquivos ou ir às compras.")

        barra_xfer = tk.Frame(self.frame_conteudo, bg=self.COR_FUNDO)
        barra_xfer.pack(fill=tk.X, pady=(0, 10))
        tk.Button(
            barra_xfer,
            text="📥 Importar Arquivo",
            bg=self.COR_FUNDO,
            fg=self.COR_PRETO,
            font=("Segoe UI", 9, "bold"),
            relief=tk.SOLID,
            bd=2,
            padx=8,
            pady=5,
            cursor="hand2",
            command=self._importar_arquivo_json,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        tk.Button(
            barra_xfer,
            text="📤 Exportar Listas",
            bg=self.COR_PRETO,
            fg=self.COR_FUNDO,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=8,
            pady=6,
            cursor="hand2",
            command=lambda: self._exportar_arquivo_json(None),
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        listas = self.storage.obter_listas()
        if not listas:
            card = self._criar_card()
            tk.Label(card, text="Nenhuma lista cadastrada ainda.", bg=self.COR_FUNDO, fg=self.COR_CINZA).pack(pady=10)
            tk.Button(
                card,
                text="+ Criar Primeira Lista",
                bg=self.COR_PRETO,
                fg=self.COR_FUNDO,
                font=("Segoe UI", 10, "bold"),
                relief=tk.FLAT,
                pady=8,
                command=self.mostrar_criar_lista,
            ).pack(fill=tk.X)
            return

        for lista in listas:
            card = self._criar_card()
            tk.Label(
                card,
                text=f"🛒 {lista.contar_itens()} itens",
                bg=self.COR_PRETO,
                fg=self.COR_FUNDO,
                font=("Segoe UI", 8, "bold"),
                padx=8,
                pady=2,
            ).pack(anchor="w", pady=(0, 6))

            tk.Label(
                card, text=lista.titulo, bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 12, "bold")
            ).pack(anchor="w")
            if lista.descricao:
                tk.Label(
                    card,
                    text=lista.descricao,
                    bg=self.COR_FUNDO,
                    fg=self.COR_CINZA,
                    font=("Segoe UI", 9),
                    wraplength=340,
                    justify="left",
                ).pack(anchor="w", pady=(2, 8))

            acoes = tk.Frame(card, bg=self.COR_FUNDO)
            acoes.pack(fill=tk.X, pady=(8, 0))

            tk.Button(
                acoes,
                text="📝 Ver / Add Itens",
                bg=self.COR_PRETO,
                fg=self.COR_FUNDO,
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                padx=10,
                pady=6,
                command=lambda lid=lista.id: self.mostrar_detalhe_lista(lid),
            ).pack(side=tk.LEFT, padx=(0, 6))

            tk.Button(
                acoes,
                text="🛒 Comprar",
                bg=self.COR_FUNDO,
                fg=self.COR_PRETO,
                font=("Segoe UI", 9, "bold"),
                relief=tk.SOLID,
                bd=1,
                padx=10,
                pady=5,
                command=lambda lid=lista.id: self.mostrar_modo_mercado(lid),
            ).pack(side=tk.LEFT, padx=(0, 6))

            tk.Button(
                acoes,
                text="📤",
                bg=self.COR_FUNDO,
                fg=self.COR_PRETO,
                font=("Segoe UI", 9, "bold"),
                relief=tk.SOLID,
                bd=1,
                padx=8,
                pady=5,
                command=lambda lid=lista.id: self._exportar_arquivo_json(lid),
            ).pack(side=tk.RIGHT, padx=(6, 0))

            tk.Button(
                acoes,
                text="🗑️",
                bg=self.COR_FUNDO,
                fg=self.COR_VERMELHO,
                font=("Segoe UI", 9, "bold"),
                relief=tk.SOLID,
                bd=1,
                padx=8,
                pady=5,
                command=lambda lid=lista.id: self._excluir_lista(lid),
            ).pack(side=tk.RIGHT)

    def _exportar_arquivo_json(self, lista_id: Optional[int]):
        try:
            payload = self.storage.exportar_listas_json(lista_id)
        except Exception as exc:
            messagebox.showerror("Erro ao Exportar", str(exc))
            return
        caminho = filedialog.asksaveasfilename(
            title="Salvar Lista para Envio / Bluetooth",
            defaultextension=".numesquece.json",
            initialfile="minha_lista.numesquece.json" if lista_id else "todas_listas.numesquece.json",
            filetypes=[("Arquivos NumEsquece JSON", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            return
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(payload)
            messagebox.showinfo("Exportação Concluída", f"Arquivo salvo em:\n{caminho}\nVocê pode enviá-lo via Bluetooth ou arquivos.")
        except OSError as exc:
            messagebox.showerror("Erro ao Salvar", str(exc))

    def _importar_arquivo_json(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar Lista nos Arquivos",
            filetypes=[("Arquivos JSON / NumEsquece", "*.json;*.txt"), ("Todos os arquivos", "*.*")],
        )
        if not caminho:
            return
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read()
            importadas = self.storage.importar_listas_json(conteudo)
            messagebox.showinfo(
                "Importação Concluída",
                f"{len(importadas)} lista(s) importada(s) e pronta(s) para uso/edição!",
            )
            self.mostrar_minhas_listas()
        except Exception as exc:
            messagebox.showerror("Erro ao Importar", f"Não foi possível importar o arquivo:\n{exc}")

    def _excluir_lista(self, lista_id: int):
        if messagebox.askyesno("Excluir Lista", "Deseja excluir esta lista de compras?"):
            self.storage.excluir_lista(lista_id)
            self.mostrar_minhas_listas()

    def mostrar_criar_lista(self):
        self._limpar_tela()
        self._criar_cabecalho("Formulário", "Criar Nova Lista", "Salve para avançar direto à adição de produtos.")

        card = self._criar_card()
        tk.Label(card, text="Nome da Lista", bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 9, "bold")).pack(
            anchor="w", pady=(0, 4)
        )
        entry_titulo = tk.Entry(
            card, bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 11), relief=tk.SOLID, bd=2
        )
        entry_titulo.pack(fill=tk.X, ipady=6, pady=(0, 10))
        entry_titulo.focus_set()

        tk.Label(
            card, text="Descrição (opcional)", bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(0, 4))
        entry_desc = tk.Entry(
            card, bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 10), relief=tk.SOLID, bd=2
        )
        entry_desc.pack(fill=tk.X, ipady=6, pady=(0, 14))

        def salvar():
            titulo = entry_titulo.get().strip()
            if not titulo:
                messagebox.showwarning("Aviso", "Informe o nome da lista.")
                return
            nova = self.storage.criar_lista(titulo=titulo, descricao=entry_desc.get().strip())
            self.mostrar_detalhe_lista(nova.id)

        tk.Button(
            card,
            text="Salvar Lista e Adicionar Itens",
            bg=self.COR_PRETO,
            fg=self.COR_FUNDO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            pady=10,
            cursor="hand2",
            command=salvar,
        ).pack(fill=tk.X)

    def mostrar_detalhe_lista(self, lista_id: int):
        lista = self.storage.buscar_lista(lista_id)
        if not lista:
            self.mostrar_minhas_listas()
            return
        self.lista_atual_id = lista_id
        self._limpar_tela()
        self._criar_cabecalho("Lista Selecionada", lista.titulo, lista.descricao or "Adicione e gerencie produtos.")

        top_btns = tk.Frame(self.frame_conteudo, bg=self.COR_FUNDO)
        top_btns.pack(fill=tk.X, pady=(0, 12))
        tk.Button(
            top_btns,
            text="🛒 Vamos Comprar?",
            bg=self.COR_PRETO,
            fg=self.COR_FUNDO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            pady=8,
            command=lambda: self.mostrar_modo_mercado(lista.id),
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        tk.Button(
            top_btns,
            text="Voltar",
            bg=self.COR_FUNDO,
            fg=self.COR_PRETO,
            font=("Segoe UI", 9, "bold"),
            relief=tk.SOLID,
            bd=1,
            padx=14,
            pady=7,
            command=self.mostrar_minhas_listas,
        ).pack(side=tk.RIGHT)

        # Formulário de adicionar produto
        card_add = self._criar_card()
        tk.Label(card_add, text="Adicionar Produto", bg=self.COR_FUNDO, font=("Segoe UI", 11, "bold")).pack(
            anchor="w", pady=(0, 8)
        )
        tk.Label(card_add, text="Nome do item", bg=self.COR_FUNDO, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_nome = tk.Entry(card_add, font=("Segoe UI", 10), relief=tk.SOLID, bd=2)
        ent_nome.pack(fill=tk.X, ipady=4, pady=(2, 8))

        row = tk.Frame(card_add, bg=self.COR_FUNDO)
        row.pack(fill=tk.X, pady=(0, 10))
        f_qtd = tk.Frame(row, bg=self.COR_FUNDO)
        f_qtd.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        tk.Label(f_qtd, text="Quantidade", bg=self.COR_FUNDO, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_qtd = tk.Entry(f_qtd, font=("Segoe UI", 10), relief=tk.SOLID, bd=2)
        ent_qtd.insert(0, "1")
        ent_qtd.pack(fill=tk.X, ipady=4)

        f_preco = tk.Frame(row, bg=self.COR_FUNDO)
        f_preco.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        tk.Label(f_preco, text="Preço (R$)", bg=self.COR_FUNDO, font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent_preco = tk.Entry(f_preco, font=("Segoe UI", 10), relief=tk.SOLID, bd=2)
        ent_preco.insert(0, "0,00")
        ent_preco.pack(fill=tk.X, ipady=4)

        def adicionar_item():
            nome = ent_nome.get().strip()
            if not nome:
                messagebox.showwarning("Aviso", "Informe o nome do produto.")
                return
            self.storage.adicionar_item_na_lista(
                lista.id, nome=nome, quantidade=ent_qtd.get().strip() or "1", preco=ent_preco.get().strip() or "0,00"
            )
            self.mostrar_detalhe_lista(lista.id)

        tk.Button(
            card_add,
            text="+ Adicionar à Lista",
            bg=self.COR_PRETO,
            fg=self.COR_FUNDO,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            pady=8,
            command=adicionar_item,
        ).pack(fill=tk.X)

        # Itens cadastrados
        card_itens = self._criar_card()
        tk.Label(
            card_itens, text=f"Itens Cadastrados ({lista.contar_itens()})", bg=self.COR_FUNDO, font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(0, 8))

        if not lista.itens:
            tk.Label(card_itens, text="Nenhum produto adicionado ainda.", bg=self.COR_FUNDO, fg=self.COR_CINZA).pack(
                pady=10
            )
        else:
            for item in lista.itens:
                item_row = tk.Frame(
                    card_itens,
                    bg=self.COR_CINZA_CLARO if item.comprado else self.COR_FUNDO,
                    highlightbackground=self.COR_PRETO,
                    highlightthickness=1,
                    padx=8,
                    pady=8,
                )
                item_row.pack(fill=tk.X, pady=(0, 6))

                tk.Label(
                    item_row,
                    text=f"{'✓ ' if item.comprado else ''}{item.nome}\nQtd: {item.quantidade} · R$ {item.preco}",
                    bg=item_row["bg"],
                    fg=self.COR_PRETO,
                    font=("Segoe UI", 9, "bold"),
                    justify="left",
                ).pack(side=tk.LEFT, anchor="w")

                tk.Button(
                    item_row,
                    text="🗑️",
                    bg=self.COR_FUNDO,
                    fg=self.COR_VERMELHO,
                    relief=tk.FLAT,
                    command=lambda iid=item.id: self._remover_item(lista.id, iid),
                ).pack(side=tk.RIGHT)

                tk.Button(
                    item_row,
                    text="✏️",
                    bg=self.COR_FUNDO,
                    fg=self.COR_PRETO,
                    relief=tk.FLAT,
                    command=lambda iid=item.id: self._editar_item(lista.id, iid),
                ).pack(side=tk.RIGHT, padx=(0, 4))

    def _editar_item(self, lista_id: int, item_id: int):
        lista = self.storage.buscar_lista(lista_id)
        if not lista:
            return
        item = lista.buscar_item(item_id)
        if not item:
            return

        modal = tk.Toplevel(self.root)
        modal.title("Editar Produto")
        modal.geometry("320x250")
        modal.configure(bg=self.COR_FUNDO)
        modal.transient(self.root)
        modal.grab_set()

        tk.Label(modal, text="Nome do produto", bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 9, "bold")).pack(
            anchor="w", padx=16, pady=(14, 2)
        )
        ent_nome = tk.Entry(modal, font=("Segoe UI", 10), relief=tk.SOLID, bd=2)
        ent_nome.insert(0, item.nome)
        ent_nome.pack(fill=tk.X, padx=16, ipady=4)

        tk.Label(modal, text="Quantidade", bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 9, "bold")).pack(
            anchor="w", padx=16, pady=(10, 2)
        )
        ent_qtd = tk.Entry(modal, font=("Segoe UI", 10), relief=tk.SOLID, bd=2)
        ent_qtd.insert(0, item.quantidade)
        ent_qtd.pack(fill=tk.X, padx=16, ipady=4)

        tk.Label(modal, text="Preço (R$)", bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 9, "bold")).pack(
            anchor="w", padx=16, pady=(10, 2)
        )
        ent_preco = tk.Entry(modal, font=("Segoe UI", 10), relief=tk.SOLID, bd=2)
        ent_preco.insert(0, item.preco)
        ent_preco.pack(fill=tk.X, padx=16, ipady=4)

        def salvar():
            nome = ent_nome.get().strip()
            if not nome:
                messagebox.showwarning("Aviso", "Informe o nome do produto.", parent=modal)
                return
            self.storage.editar_item_da_lista(
                lista_id,
                item_id,
                nome=nome,
                quantidade=ent_qtd.get().strip() or "1",
                preco=ent_preco.get().strip() or "0,00",
            )
            modal.destroy()
            self.mostrar_detalhe_lista(lista_id)

        btns = tk.Frame(modal, bg=self.COR_FUNDO)
        btns.pack(fill=tk.X, padx=16, pady=14)
        tk.Button(
            btns, text="Cancelar", bg=self.COR_FUNDO, fg=self.COR_PRETO, relief=tk.SOLID, bd=1, command=modal.destroy
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 6))
        tk.Button(
            btns,
            text="Salvar",
            bg=self.COR_PRETO,
            fg=self.COR_FUNDO,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            command=salvar,
        ).pack(side=tk.RIGHT, expand=True, fill=tk.X)

    def _remover_item(self, lista_id: int, item_id: int):
        self.storage.remover_item_da_lista(lista_id, item_id)
        self.mostrar_detalhe_lista(lista_id)

    def mostrar_modo_mercado(self, lista_id: int):
        lista = self.storage.buscar_lista(lista_id)
        if not lista:
            return
        self.lista_atual_id = lista_id
        self._limpar_tela()
        self._criar_cabecalho("Modo Supermercado", lista.titulo, "Toque nos itens para colocá-los no carrinho.")

        total_carrinho = sum(it.calcular_subtotal() for it in lista.itens if it.id in self.itens_no_carrinho)

        box_total = self._criar_card()
        tk.Label(box_total, text="VALOR NO CARRINHO", bg=self.COR_FUNDO, font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(
            box_total, text=formatar_moeda_brl(total_carrinho), bg=self.COR_FUNDO, font=("Consolas", 18, "bold")
        ).pack(side=tk.LEFT)

        tk.Button(
            box_total,
            text="Finalizar Compra",
            bg=self.COR_PRETO,
            fg=self.COR_FUNDO,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=10,
            pady=6,
            command=lambda: self._finalizar_compra_mercado(lista.id),
        ).pack(side=tk.RIGHT)

        card_prateleira = self._criar_card()
        tk.Label(card_prateleira, text="Produtos na Prateleira", bg=self.COR_FUNDO, font=("Segoe UI", 11, "bold")).pack(
            anchor="w", pady=(0, 8)
        )
        na_prateleira = [it for it in lista.itens if it.id not in self.itens_no_carrinho]
        if not na_prateleira:
            tk.Label(card_prateleira, text="Todos os itens estão no carrinho.", bg=self.COR_FUNDO, fg=self.COR_CINZA).pack(
                pady=6
            )
        for item in na_prateleira:
            r = tk.Frame(card_prateleira, bg=self.COR_FUNDO, highlightbackground=self.COR_PRETO, highlightthickness=1, padx=8, pady=6)
            r.pack(fill=tk.X, pady=(0, 6))
            tk.Label(r, text=f"{item.nome} (x{item.quantidade}) · R$ {item.preco}", bg=self.COR_FUNDO, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
            tk.Button(
                r, text="+ Carrinho", bg=self.COR_PRETO, fg=self.COR_FUNDO, font=("Segoe UI", 8, "bold"), relief=tk.FLAT,
                command=lambda iid=item.id: self._mover_para_carrinho(lista.id, iid)
            ).pack(side=tk.RIGHT)

        card_car = self._criar_card()
        tk.Label(card_car, text="Dentro do Carrinho 🛒", bg=self.COR_FUNDO, font=("Segoe UI", 11, "bold")).pack(
            anchor="w", pady=(0, 8)
        )
        no_carrinho = [it for it in lista.itens if it.id in self.itens_no_carrinho]
        for item in no_carrinho:
            r = tk.Frame(card_car, bg=self.COR_CINZA_CLARO, highlightbackground=self.COR_PRETO, highlightthickness=1, padx=8, pady=6)
            r.pack(fill=tk.X, pady=(0, 6))
            tk.Label(r, text=f"✓ {item.nome} (x{item.quantidade}) · {formatar_moeda_brl(item.calcular_subtotal())}", bg=self.COR_CINZA_CLARO, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
            tk.Button(
                r, text="Tirar", bg=self.COR_FUNDO, fg=self.COR_PRETO, font=("Segoe UI", 8, "bold"), relief=tk.SOLID, bd=1,
                command=lambda iid=item.id: self._tirar_do_carrinho(lista.id, iid)
            ).pack(side=tk.RIGHT)

    def _mover_para_carrinho(self, lista_id: int, item_id: int):
        self.itens_no_carrinho.add(item_id)
        self.mostrar_modo_mercado(lista_id)

    def _tirar_do_carrinho(self, lista_id: int, item_id: int):
        self.itens_no_carrinho.discard(item_id)
        self.mostrar_modo_mercado(lista_id)

    def _finalizar_compra_mercado(self, lista_id: int):
        compra = self.storage.finalizar_compra(lista_id, list(self.itens_no_carrinho))
        self.itens_no_carrinho.clear()
        if compra:
            messagebox.showinfo("Sucesso", f"Compra salva no histórico!\nTotal: {compra.valor_formatado()}")
        self.mostrar_historico()

    def mostrar_historico(self):
        self._limpar_tela()
        self._criar_cabecalho("Registro", "Histórico de Compras", "Compras salvas diretamente no aparelho.")

        historico = self.storage.obter_historico()
        if not historico:
            card = self._criar_card()
            tk.Label(card, text="Nenhuma compra finalizada ainda.", bg=self.COR_FUNDO, fg=self.COR_CINZA).pack(pady=10)
            return

        for compra in historico:
            card = self._criar_card()
            tk.Label(card, text=compra.titulo_lista, bg=self.COR_FUNDO, font=("Segoe UI", 12, "bold")).pack(anchor="w")
            tk.Label(
                card, text=f"Total Gasto: {compra.valor_formatado()}", bg=self.COR_FUNDO, font=("Consolas", 13, "bold")
            ).pack(anchor="w", pady=(4, 8))
            for it in compra.itens_comprados:
                tk.Label(
                    card,
                    text=f"• {it.nome} (x{it.quantidade}) — R$ {it.preco}",
                    bg=self.COR_FUNDO,
                    fg=self.COR_CINZA,
                    font=("Segoe UI", 9),
                ).pack(anchor="w")

    def iniciar(self):
        self.root.mainloop()
