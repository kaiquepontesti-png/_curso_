import copy
import json
import os
from datetime import datetime
from typing import List, Optional

from .models import CompraFinalizada, ItemProduto, ListaDeCompras, gerar_id_unico


class ArmazenamentoLocal:
    """
    Classe responsável por gerenciar e salvar todas as informações
    diretamente na memória local do dispositivo (RAM + arquivo JSON local),
    sem necessidade de banco de dados externo (MySQL) ou internet.
    """

    def __init__(self, caminho_arquivo: Optional[str] = None, inicializar_exemplo: bool = True):
        if caminho_arquivo is None:
            pasta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            caminho_arquivo = os.path.join(pasta_base, "dados_dispositivo.json")

        self.caminho_arquivo: str = caminho_arquivo
        self.listas: List[ListaDeCompras] = []
        self.historico: List[CompraFinalizada] = []

        self.carregar_dados(inicializar_exemplo=inicializar_exemplo)

    def carregar_dados(self, inicializar_exemplo: bool = True) -> None:
        """Carrega os objetos ListaDeCompras e CompraFinalizada da memória local do aparelho."""
        if os.path.exists(self.caminho_arquivo):
            try:
                with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                self.listas = [
                    ListaDeCompras.from_dict(item) for item in dados.get("listas", [])
                ]
                self.historico = [
                    CompraFinalizada.from_dict(comp) for comp in dados.get("historico", [])
                ]
                return
            except (OSError, json.JSONDecodeError, ValueError):
                pass

        if inicializar_exemplo and not self.listas:
            lista_exemplo = ListaDeCompras(
                id=1,
                titulo="Compras do Mês",
                descricao="Itens essenciais para a despensa e limpeza",
                itens=[
                    ItemProduto(id=101, nome="Arroz 5kg", quantidade="2", preco="28,90"),
                    ItemProduto(id=102, nome="Feijão Carioca 1kg", quantidade="3", preco="7,49"),
                    ItemProduto(id=103, nome="Café Torrado 500g", quantidade="2", preco="16,50"),
                    ItemProduto(id=104, nome="Leite Integral 1L", quantidade="6", preco="4,69"),
                    ItemProduto(id=105, nome="Azeite de Oliva 500ml", quantidade="1", preco="34,90"),
                ],
            )
            self.listas = [lista_exemplo]
            self.historico = []
            self.salvar_dados()

    def salvar_dados(self) -> None:
        """Persiste todos os dados das classes na memória interna do dispositivo em formato JSON."""
        pasta = os.path.dirname(os.path.abspath(self.caminho_arquivo))
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)

        payload = {
            "listas": [lista.to_dict() for lista in self.listas],
            "historico": [compra.to_dict() for compra in self.historico],
            "atualizado_em": datetime.now().isoformat(),
        }
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def obter_listas(self) -> List[ListaDeCompras]:
        return list(self.listas)

    def buscar_lista(self, lista_id: int) -> Optional[ListaDeCompras]:
        for lista in self.listas:
            if lista.id == lista_id:
                return lista
        return None

    def criar_lista(self, titulo: str, descricao: str = "") -> ListaDeCompras:
        titulo_limpo = titulo.strip()
        if not titulo_limpo:
            raise ValueError("O título da lista não pode estar vazio.")

        nova_lista = ListaDeCompras(
            titulo=titulo_limpo,
            descricao=descricao.strip(),
        )
        self.listas.insert(0, nova_lista)
        self.salvar_dados()
        return nova_lista

    def editar_lista(
        self, lista_id: int, titulo: str, descricao: str = ""
    ) -> Optional[ListaDeCompras]:
        lista = self.buscar_lista(lista_id)
        if not lista:
            return None

        titulo_limpo = titulo.strip()
        if not titulo_limpo:
            raise ValueError("O título da lista não pode estar vazio.")

        lista.titulo = titulo_limpo
        lista.descricao = descricao.strip()
        lista.atualizado_em = datetime.now().isoformat()
        self.salvar_dados()
        return lista

    def duplicar_lista(self, lista_id: int) -> Optional[ListaDeCompras]:
        original = self.buscar_lista(lista_id)
        if not original:
            return None

        itens_copiados = []
        for idx, it in enumerate(original.itens):
            itens_copiados.append(
                ItemProduto(
                    id=gerar_id_unico() + idx + 1,
                    nome=it.nome,
                    quantidade=it.quantidade,
                    preco=it.preco,
                    comprado=False,
                )
            )

        nova_lista = ListaDeCompras(
            titulo=f"{original.titulo} (Cópia)",
            descricao=original.descricao,
            itens=itens_copiados,
        )
        self.listas.insert(0, nova_lista)
        self.salvar_dados()
        return nova_lista

    def excluir_lista(self, lista_id: int) -> bool:
        tamanho_antes = len(self.listas)
        self.listas = [l for l in self.listas if l.id != lista_id]
        if len(self.listas) < tamanho_antes:
            self.salvar_dados()
            return True
        return False

    def adicionar_item_na_lista(
        self,
        lista_id: int,
        nome: str,
        quantidade: str = "1",
        preco: str = "0,00",
        comprado: bool = False,
    ) -> Optional[ItemProduto]:
        lista = self.buscar_lista(lista_id)
        if not lista:
            return None
        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome do produto não pode estar vazio.")

        item = lista.adicionar_item(
            nome=nome_limpo,
            quantidade=quantidade,
            preco=preco,
            comprado=comprado,
        )
        self.salvar_dados()
        return item

    def editar_item_da_lista(
        self,
        lista_id: int,
        item_id: int,
        nome: str,
        quantidade: str = "1",
        preco: str = "0,00",
    ) -> Optional[ItemProduto]:
        lista = self.buscar_lista(lista_id)
        if not lista:
            return None
        item = lista.editar_item(item_id, nome=nome, quantidade=quantidade, preco=preco)
        if item:
            self.salvar_dados()
        return item

    def remover_item_da_lista(self, lista_id: int, item_id: int) -> bool:
        lista = self.buscar_lista(lista_id)
        if not lista:
            return False
        removido = lista.remover_item(item_id)
        if removido:
            self.salvar_dados()
        return removido

    def alternar_item_comprado(self, lista_id: int, item_id: int) -> bool:
        lista = self.buscar_lista(lista_id)
        if not lista:
            return False
        alterado = lista.alternar_item_comprado(item_id)
        if alterado:
            self.salvar_dados()
        return alterado

    def obter_historico(self) -> List[CompraFinalizada]:
        return list(self.historico)

    def finalizar_compra(
        self, lista_id: int, ids_no_carrinho: Optional[List[int]] = None
    ) -> Optional[CompraFinalizada]:
        lista = self.buscar_lista(lista_id)
        if not lista:
            return None

        if ids_no_carrinho is not None:
            selecionados = [it for it in lista.itens if it.id in ids_no_carrinho]
        else:
            selecionados = [it for it in lista.itens if it.comprado]

        total = round(sum(it.calcular_subtotal() for it in selecionados), 2)
        itens_copia = [copy.deepcopy(it) for it in selecionados]

        for it in selecionados:
            it.comprado = True

        compra = CompraFinalizada(
            titulo_lista=lista.titulo,
            valor_total=total,
            itens_comprados=itens_copia,
        )
        self.historico.insert(0, compra)
        self.salvar_dados()
        return compra

    def exportar_listas_json(self, lista_id: Optional[int] = None) -> str:
        """Exporta uma lista específica ou todas as listas no formato portátil JSON."""
        if lista_id is not None:
            alvo = self.buscar_lista(lista_id)
            listas_exportar = [alvo] if alvo else []
        else:
            listas_exportar = list(self.listas)

        pacote = {
            "app": "NumEsqueceLista",
            "versao": 1,
            "exportadoEm": datetime.now().isoformat(timespec="seconds"),
            "origem": "Desktop",
            "listas": [lst.to_dict() for lst in listas_exportar],
        }
        return json.dumps(pacote, ensure_ascii=False, indent=2)

    def importar_listas_json(self, conteudo_json: str) -> List[ListaDeCompras]:
        """
        Importa uma ou mais listas a partir de JSON recebido via Bluetooth/arquivo,
        criando objetos ListaDeCompras/ItemProduto com novos IDs locais únicos.
        """
        if not conteudo_json or not conteudo_json.strip():
            raise ValueError("Arquivo JSON vazio.")

        dados = json.loads(conteudo_json)
        if isinstance(dados, dict) and isinstance(dados.get("listas"), list):
            entradas = dados["listas"]
        elif isinstance(dados, list):
            entradas = dados
        elif isinstance(dados, dict) and (dados.get("titulo") or isinstance(dados.get("itens"), list)):
            entradas = [dados]
        else:
            raise ValueError("Formato de lista NumEsquece inválido.")

        importadas: List[ListaDeCompras] = []
        base_id = gerar_id_unico()
        for idx, bruta in enumerate(entradas):
            if not isinstance(bruta, dict):
                continue
            titulo = str(bruta.get("titulo") or "").strip()
            if not titulo:
                continue

            novo_id_lista = base_id + idx + 1
            itens_novos: List[ItemProduto] = []
            itens_brutos = bruta.get("itens") if isinstance(bruta.get("itens"), list) else []
            for item_idx, item_dict in enumerate(itens_brutos):
                if not isinstance(item_dict, dict):
                    continue
                nome_item = str(item_dict.get("nome") or "").strip()
                if not nome_item:
                    continue
                itens_novos.append(
                    ItemProduto(
                        id=gerar_id_unico() + item_idx + 1,
                        nome=nome_item,
                        quantidade=str(item_dict.get("quantidade") or "1"),
                        preco=str(item_dict.get("preco") or "0,00"),
                        comprado=bool(item_dict.get("comprado", item_dict.get("no_carrinho", False))),
                    )
                )

            nova_lista = ListaDeCompras(
                id=novo_id_lista,
                titulo=titulo,
                descricao=str(bruta.get("descricao") or bruta.get("subtitulo") or ""),
                itens=itens_novos,
            )
            self.listas.insert(0, nova_lista)
            importadas.append(nova_lista)

        if not importadas:
            raise ValueError("Nenhuma lista válida encontrada no arquivo selecionado.")

        self.salvar_dados()
        return importadas
