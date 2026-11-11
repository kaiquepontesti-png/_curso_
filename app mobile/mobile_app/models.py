from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import time


def gerar_id_unico() -> int:
    """Gera um identificador único numérico baseado no timestamp em microssegundos."""
    return int(time.time() * 1_000_000)


def formatar_moeda_brl(valor: float) -> str:
    """Formata um valor float no padrão monetário brasileiro (ex: R$ 1.234,56)."""
    texto = f"{valor:,.2f}"
    # Converte formato americano 1,234.56 -> 1.234,56
    texto = texto.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {texto}"


def converter_preco_para_float(valor_str: str) -> float:
    """Converte string monetária brasileira (ex: '28,90') para float."""
    if not valor_str:
        return 0.0
    limpo = str(valor_str).replace("R$", "").strip().replace(".", "").replace(",", ".")
    try:
        return float(limpo)
    except ValueError:
        return 0.0


def converter_qtd_para_float(qtd_str: str) -> float:
    """Converte string de quantidade (ex: '2', '1.5', '1,5') para float."""
    if not qtd_str:
        return 1.0
    limpo = str(qtd_str).strip().replace(",", ".")
    try:
        val = float(limpo)
        return val if val > 0 else 1.0
    except ValueError:
        return 1.0


@dataclass
class ItemProduto:
    """Classe que representa um item/produto dentro de uma lista de compras."""

    nome: str
    quantidade: str = "1"
    preco: str = "0,00"
    comprado: bool = False
    id: int = field(default_factory=gerar_id_unico)

    def preco_numerico(self) -> float:
        return converter_preco_para_float(self.preco)

    def quantidade_numerica(self) -> float:
        return converter_qtd_para_float(self.quantidade)

    def calcular_subtotal(self) -> float:
        return round(self.preco_numerico() * self.quantidade_numerica(), 2)

    def alternar_comprado(self) -> bool:
        self.comprado = not self.comprado
        return self.comprado

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "preco": self.preco,
            "comprado": self.comprado,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ItemProduto":
        return cls(
            id=int(data.get("id", gerar_id_unico())),
            nome=str(data.get("nome", "")),
            quantidade=str(data.get("quantidade", "1")),
            preco=str(data.get("preco", "0,00")),
            comprado=bool(data.get("comprado", False)),
        )


@dataclass
class ListaDeCompras:
    """Classe que representa uma lista de compras armazenada localmente no dispositivo."""

    titulo: str
    descricao: str = ""
    itens: List[ItemProduto] = field(default_factory=list)
    atualizado_em: str = field(default_factory=lambda: datetime.now().isoformat())
    id: int = field(default_factory=gerar_id_unico)

    def adicionar_item(
        self, nome: str, quantidade: str = "1", preco: str = "0,00", comprado: bool = False
    ) -> ItemProduto:
        novo_item = ItemProduto(
            nome=nome.strip(),
            quantidade=quantidade.strip() or "1",
            preco=preco.strip() or "0,00",
            comprado=comprado,
        )
        self.itens.append(novo_item)
        self.atualizado_em = datetime.now().isoformat()
        return novo_item

    def buscar_item(self, item_id: int) -> Optional[ItemProduto]:
        for item in self.itens:
            if item.id == item_id:
                return item
        return None

    def editar_item(
        self, item_id: int, nome: str, quantidade: str = "1", preco: str = "0,00"
    ) -> Optional[ItemProduto]:
        item = self.buscar_item(item_id)
        if not item:
            return None
        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome do produto não pode estar vazio.")
        item.nome = nome_limpo
        item.quantidade = quantidade.strip() or "1"
        item.preco = preco.strip() or "0,00"
        self.atualizado_em = datetime.now().isoformat()
        return item

    def remover_item(self, item_id: int) -> bool:
        tamanho_antes = len(self.itens)
        self.itens = [it for it in self.itens if it.id != item_id]
        if len(self.itens) < tamanho_antes:
            self.atualizado_em = datetime.now().isoformat()
            return True
        return False

    def alternar_item_comprado(self, item_id: int) -> bool:
        item = self.buscar_item(item_id)
        if item:
            item.alternar_comprado()
            self.atualizado_em = datetime.now().isoformat()
            return True
        return False

    def calcular_total_estimado(self) -> float:
        return round(sum(it.calcular_subtotal() for it in self.itens), 2)

    def calcular_total_comprado(self) -> float:
        return round(sum(it.calcular_subtotal() for it in self.itens if it.comprado), 2)

    def contar_itens(self) -> int:
        return len(self.itens)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "atualizado_em": self.atualizado_em,
            "itens": [it.to_dict() for it in self.itens],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ListaDeCompras":
        itens_objs = [ItemProduto.from_dict(it) for it in data.get("itens", [])]
        return cls(
            id=int(data.get("id", gerar_id_unico())),
            titulo=str(data.get("titulo", "")),
            descricao=str(data.get("descricao", "")),
            atualizado_em=str(data.get("atualizado_em", datetime.now().isoformat())),
            itens=itens_objs,
        )


@dataclass
class CompraFinalizada:
    """Classe que representa o registro histórico de uma compra finalizada no dispositivo."""

    titulo_lista: str
    valor_total: float
    itens_comprados: List[ItemProduto] = field(default_factory=list)
    data_compra: str = field(default_factory=lambda: datetime.now().isoformat())
    id: int = field(default_factory=gerar_id_unico)

    def valor_formatado(self) -> str:
        return formatar_moeda_brl(self.valor_total)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "titulo_lista": self.titulo_lista,
            "valor_total": self.valor_total,
            "data_compra": self.data_compra,
            "itens_comprados": [it.to_dict() for it in self.itens_comprados],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompraFinalizada":
        itens_objs = [ItemProduto.from_dict(it) for it in data.get("itens_comprados", [])]
        return cls(
            id=int(data.get("id", gerar_id_unico())),
            titulo_lista=str(data.get("titulo_lista", "")),
            valor_total=float(data.get("valor_total", 0.0)),
            data_compra=str(data.get("data_compra", datetime.now().isoformat())),
            itens_comprados=itens_objs,
        )
