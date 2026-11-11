import os
import json
import pytest

from mobile_app.models import (
    ItemProduto,
    ListaDeCompras,
    CompraFinalizada,
    formatar_moeda_brl,
)
from mobile_app.storage import ArmazenamentoLocal
from mobile_app.ui_builder import gerar_html_mobile


def test_gerar_html_android_e_ios():
    bg = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "bg-doodle.jpg"))
    html_android = gerar_html_mobile(bg, plataforma="android", modo_pwa=False)
    assert "const IS_IOS_PLATFORM = false;" in html_android
    assert "manifest.webmanifest" not in html_android

    html_ios_pwa = gerar_html_mobile(bg, plataforma="ios", modo_pwa=True)
    assert "const IS_IOS_PLATFORM = true;" in html_ios_pwa
    assert "const IS_PWA_MODE = true;" in html_ios_pwa
    assert 'name="apple-mobile-web-app-capable"' in html_ios_pwa
    assert 'rel="manifest" href="manifest.webmanifest"' in html_ios_pwa
    assert "ios-topbar-back-btn" in html_ios_pwa
    assert "window.__IOS_PRELOADED_DATA__" in html_ios_pwa
    assert "transfer-modal" in html_ios_pwa
    assert "receberArquivoImportadoBase64" in html_ios_pwa
    assert "AndroidBridge" in html_android

    html_ios_wk = gerar_html_mobile(bg, plataforma="ios", modo_pwa=False)
    assert "const IS_IOS_PLATFORM = true;" in html_ios_wk
    assert "const IS_PWA_MODE = false;" in html_ios_wk
    assert "manifest.webmanifest" not in html_ios_wk
    assert "iosShare" in html_ios_wk
    assert "iosImportFile" in html_ios_wk


def test_item_produto_calculo_subtotal():
    item = ItemProduto(nome="Arroz 5kg", quantidade="2", preco="28,90")
    assert item.preco_numerico() == 28.90
    assert item.quantidade_numerica() == 2.0
    assert item.calcular_subtotal() == 57.80
    assert item.comprado is False

    item.alternar_comprado()
    assert item.comprado is True


def test_lista_de_compras_operacoes():
    lista = ListaDeCompras(titulo="Churrasco", descricao="Final de semana")
    item1 = lista.adicionar_item("Picanha", "2", "79,90")
    item2 = lista.adicionar_item("Carvão", "1", "25,00")

    assert lista.contar_itens() == 2
    assert lista.calcular_total_estimado() == round(2 * 79.90 + 25.00, 2)

    assert lista.alternar_item_comprado(item1.id) is True
    assert lista.calcular_total_comprado() == round(2 * 79.90, 2)

    editado = lista.editar_item(item2.id, "Carvão Ecológico", "2", "30,00")
    assert editado is not None
    assert editado.nome == "Carvão Ecológico"
    assert editado.calcular_subtotal() == 60.00

    assert lista.remover_item(item2.id) is True
    assert lista.contar_itens() == 1


def test_editar_item_armazenamento_local(tmp_path):
    arquivo = tmp_path / "dados_edit.json"
    storage = ArmazenamentoLocal(caminho_arquivo=str(arquivo), inicializar_exemplo=False)
    lista = storage.criar_lista("Feira")
    item = storage.adicionar_item_na_lista(lista.id, "Maçã", "3", "4,00")
    assert item is not None

    atualizado = storage.editar_item_da_lista(lista.id, item.id, "Maçã Gala", "5", "5,50")
    assert atualizado is not None
    assert atualizado.nome == "Maçã Gala"

    recarregado = ArmazenamentoLocal(caminho_arquivo=str(arquivo), inicializar_exemplo=False)
    item_salvo = recarregado.obter_listas()[0].itens[0]
    assert item_salvo.nome == "Maçã Gala"
    assert item_salvo.quantidade == "5"
    assert item_salvo.preco == "5,50"


def test_armazenamento_local_persistencia(tmp_path):
    arquivo = tmp_path / "dados_teste.json"
    storage = ArmazenamentoLocal(caminho_arquivo=str(arquivo), inicializar_exemplo=False)

    # Criar lista
    nova_lista = storage.criar_lista("Compras Rápidas", "Padaria")
    assert nova_lista.titulo == "Compras Rápidas"
    assert os.path.exists(arquivo)

    # Adicionar itens
    item1 = storage.adicionar_item_na_lista(nova_lista.id, "Pão Francês", "6", "0,80")
    item2 = storage.adicionar_item_na_lista(nova_lista.id, "Queijo", "1", "18,50")
    assert item1 is not None and item2 is not None

    # Duplicar lista
    copia = storage.duplicar_lista(nova_lista.id)
    assert copia is not None
    assert copia.titulo == "Compras Rápidas (Cópia)"
    assert copia.contar_itens() == 2

    # Finalizar compra no modo supermercado
    compra = storage.finalizar_compra(nova_lista.id, ids_no_carrinho=[item1.id, item2.id])
    assert compra is not None
    assert compra.valor_total == round(6 * 0.80 + 18.50, 2)
    assert formatar_moeda_brl(compra.valor_total) == "R$ 23,30"

    # Recarregar em nova instância de ArmazenamentoLocal para provar persistência em arquivo local
    storage_recarregado = ArmazenamentoLocal(caminho_arquivo=str(arquivo), inicializar_exemplo=False)
    listas = storage_recarregado.obter_listas()
    historico = storage_recarregado.obter_historico()

    assert len(listas) == 2
    assert len(historico) == 1
    assert historico[0].titulo_lista == "Compras Rápidas"
    assert len(historico[0].itens_comprados) == 2


def test_excluir_lista(tmp_path):
    arquivo = tmp_path / "dados_del.json"
    storage = ArmazenamentoLocal(caminho_arquivo=str(arquivo), inicializar_exemplo=False)
    lista = storage.criar_lista("Temporária")
    assert len(storage.obter_listas()) == 1

    excluida = storage.excluir_lista(lista.id)
    assert excluida is True
    assert len(storage.obter_listas()) == 0


def test_exportar_e_importar_listas_json(tmp_path):
    origem_arquivo = tmp_path / "origem.json"
    destino_arquivo = tmp_path / "destino.json"

    origem = ArmazenamentoLocal(caminho_arquivo=str(origem_arquivo), inicializar_exemplo=False)
    lista = origem.criar_lista("Churrasco Bluetooth", "Recebido de outro aparelho")
    origem.adicionar_item_na_lista(lista.id, "Pão de Alho", "2", "12,50")
    origem.adicionar_item_na_lista(lista.id, "Carvão 5kg", "1", "24,00")

    pacote_json = origem.exportar_listas_json(lista.id)
    dados = json.loads(pacote_json)
    assert dados["app"] == "NumEsqueceLista"
    assert len(dados["listas"]) == 1
    assert dados["listas"][0]["titulo"] == "Churrasco Bluetooth"

    destino = ArmazenamentoLocal(caminho_arquivo=str(destino_arquivo), inicializar_exemplo=False)
    importadas = destino.importar_listas_json(pacote_json)
    assert len(importadas) == 1
    imp = importadas[0]
    assert imp.titulo == "Churrasco Bluetooth"
    assert imp.contar_itens() == 2

    # Verificar que a lista importada pode ser editada e salva localmente normalmente
    item_editado = destino.editar_item_da_lista(imp.id, imp.itens[0].id, "Pão de Alho Picante", "3", "14,00")
    assert item_editado is not None
    assert item_editado.nome == "Pão de Alho Picante"

    recarregado = ArmazenamentoLocal(caminho_arquivo=str(destino_arquivo), inicializar_exemplo=False)
    assert len(recarregado.obter_listas()) == 1
    assert recarregado.obter_listas()[0].itens[0].nome == "Pão de Alho Picante"
    assert recarregado.obter_listas()[0].itens[0].quantidade == "3"
