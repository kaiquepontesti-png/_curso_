# 📱 NumEsquece Lista · Mobile (100% Local e Orientado a Objetos)

Esta pasta contém a versão exclusivamente mobile do aplicativo **NumEsquece Lista**, sem qualquer dependência de servidor web, login, Flask, MySQL ou banco de dados externo.

Todas as informações são gerenciadas por **Classes Orientadas a Objetos** e salvas diretamente na **memória local do dispositivo**.

---

## 🧱 Arquitetura Baseada em Classes (100% Memória Local)

Tanto o código-fonte em Python quanto o aplicativo Android empacotado utilizam as mesmas classes estruturadas:

1. **`ItemProduto`** ([`models.py`](mobile_app/models.py)):
   - Representa cada produto de uma lista (`id`, `nome`, `quantidade`, `preco`, `comprado`).
   - Possui métodos próprios de cálculo de subtotal (`calcular_subtotal()`) e conversão para dicionário/JSON.
2. **`ListaDeCompras`** ([`models.py`](mobile_app/models.py)):
   - Encapsula uma lista completa com métodos para `adicionar_item()`, `remover_item()`, `alternar_item_comprado()` e cálculo de totais.
3. **`CompraFinalizada`** ([`models.py`](mobile_app/models.py)):
   - Representa um registro histórico imutável de compras finalizadas com data, valor total e itens adquiridos.
4. **`ArmazenamentoLocal`** ([`storage.py`](mobile_app/storage.py)):
   - Gerencia listas e compras na memória local (RAM + arquivo JSON `dados_dispositivo.json` no Python; `localStorage` + `IndexedDB` + memória RAM no Android APK).

---

## 📁 Estrutura Limpa (Somente Mobile)

```text
app mobile/
├── NumEsqueceLista.apk      <- Aplicativo Android compilado, alinhado e assinado (Android 8 a 15)
├── main.py                  <- Executável Python nativo (abre janela mobile Tkinter local sem navegador)
├── mobile_app/
│   ├── __init__.py
│   ├── models.py            <- Classes ItemProduto, ListaDeCompras e CompraFinalizada
│   ├── storage.py           <- Classe ArmazenamentoLocal (persistência sem banco de dados externo)
│   ├── ui_desktop.py        <- Interface gráfica mobile nativa em Python (Tkinter)
│   └── ui_builder.py        <- Gerador da interface Android empacotada no APK
├── assets/                  <- Recursos visuais mobile (doodle de fundo e ícones)
├── tests/                   <- Testes automatizados validando as classes e armazenamento local
├── requirements.txt         <- Sem dependências web/MySQL (apenas pytest para testes)
└── README.md                <- Este guia
```

---

## 📲 Como Usar

### No Celular Android (APK)
1. Transfira [`NumEsqueceLista.apk`](NumEsqueceLista.apk) para o celular.
2. Toque para instalar. Se o Play Protect exibir aviso no Android 15, toque em **Mais detalhes ➔ Instalar assim mesmo**.
3. Ao criar uma lista e tocar em **Salvar Lista**, o aplicativo cria uma instância de `ListaDeCompras`, salva na memória local do celular e leva você diretamente para a tela de **Adicionar Produtos**.

### No Computador em Python Puro (Simulador Mobile Nativo)
Sem precisar de navegador ou servidor web:
```powershell
python main.py
```
Abrirá a interface móvel com armazenamento automático no arquivo local `dados_dispositivo.json`.

### Rodar Testes Automatizados das Classes
```powershell
python -m pytest tests
```
