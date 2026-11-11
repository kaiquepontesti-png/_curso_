import base64
import os


def gerar_html_mobile(
    caminho_imagem_fundo: str,
    plataforma: str = "android",
    modo_pwa: bool = False,
) -> str:
    """
    Gera a interface mobile offline completa do aplicativo NumEsquece Lista
    com classes orientadas a objetos (ItemProduto, ListaDeCompras,
    CompraFinalizada, ArmazenamentoLocal e AplicativoNumEsquece) operando 100%
    na memória local do dispositivo, sem nenhuma dependência web.
    Suporta alvos 'android' e 'ios' (PWA Safari e projeto nativo WKWebView .ipa).
    """
    eh_ios = plataforma == "ios"
    extra_head_parts = []
    if eh_ios:
        extra_head_parts.extend([
            '  <meta name="apple-mobile-web-app-capable" content="yes" />',
            '  <meta name="apple-mobile-web-app-status-bar-style" content="default" />',
            '  <meta name="apple-mobile-web-app-title" content="NumEsquece Lista" />',
            '  <meta name="theme-color" content="#FFFFFF" />',
            '  <meta name="format-detection" content="telephone=no" />',
        ])
        if modo_pwa:
            extra_head_parts.extend([
                '  <link rel="manifest" href="manifest.webmanifest" />',
                '  <link rel="apple-touch-icon" sizes="180x180" href="icon-180.png" />',
                '  <link rel="icon" type="image/png" sizes="512x512" href="icon-512.png" />',
            ])
    extra_head = "\n".join(extra_head_parts)

    with open(caminho_imagem_fundo, "rb") as f:
        bg_b64 = base64.b64encode(f.read()).decode("ascii")

    bg_data_uri = f"url('data:image/jpeg;base64,{bg_b64}')"

    html = r'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>NumEsquece Lista</title>
__EXTRA_HEAD__
  <style>
    :root {
      --bg-base: #FFFFFF;
      --text-main: #000000;
      --text-muted: #757575;
      --border-black: 2px solid #000000;
      --shadow-dry-sm: 2px 2px 0px #000000;
      --shadow-dry-md: 3px 3px 0px #000000;
      --shadow-dry-lg: 4px 4px 0px #000000;
      --font-main: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --font-mono: "JetBrains Mono", SFMono-Regular, Consolas, Menlo, monospace;
      --topbar-height: 60px;
      --bottom-nav-height: 64px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      font-family: var(--font-main);
      background-color: #FFFFFF;
      background-image:
        linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
        __BG_IMAGE_URI__;
      background-repeat: repeat;
      background-size: 380px auto;
      background-position: center top;
      background-attachment: fixed;
      color: var(--text-main);
      min-height: 100vh;
      line-height: 1.5;
      padding-top: calc(var(--topbar-height) + env(safe-area-inset-top, 0px));
      padding-bottom: calc(var(--bottom-nav-height) + env(safe-area-inset-bottom, 0px) + 24px);
      user-select: none;
      -webkit-user-select: none;
      -webkit-touch-callout: none;
      -webkit-overflow-scrolling: touch;
      overscroll-behavior-y: contain;
    }

    @supports (-webkit-touch-callout: none) {
      body {
        background-attachment: scroll;
      }
    }

    input, textarea, select {
      user-select: text;
      -webkit-user-select: text;
    }

    /* Topbar Fixa */
    .app-topbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      height: calc(var(--topbar-height) + env(safe-area-inset-top, 0px));
      background: #FFFFFF;
      border-bottom: var(--border-black);
      box-shadow: 0 2px 0px #000000;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      padding-top: env(safe-area-inset-top, 0px);
      z-index: 1000;
    }

    .topbar-back-btn {
      background: #FFFFFF;
      color: #000000;
      border: 2px solid #000000;
      border-radius: 8px;
      padding: 5px 10px;
      font-weight: 800;
      font-size: 0.84rem;
      cursor: pointer;
      box-shadow: 2px 2px 0px #000000;
      display: none;
      align-items: center;
      gap: 4px;
      flex-shrink: 0;
    }

    .topbar-back-btn:active {
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0px #000000;
    }

    .topbar-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 1.15rem;
      color: #000000;
    }

    .brand-icon {
      width: 34px;
      height: 34px;
      background: #000000;
      color: #FFFFFF;
      border: 2px solid #000000;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
      box-shadow: 2px 2px 0px #000000;
    }

    .topbar-action-btn {
      background: #000000;
      color: #FFFFFF;
      border: 2px solid #000000;
      border-radius: 8px;
      padding: 6px 14px;
      font-weight: 700;
      font-size: 0.85rem;
      cursor: pointer;
      box-shadow: 2px 2px 0px #000000;
      transition: all 0.15s ease;
    }

    .topbar-action-btn:active {
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0px #000000;
    }

    /* Toast Mobile */
    .toast-banner {
      position: fixed;
      top: calc(var(--topbar-height) + env(safe-area-inset-top, 0px) + 12px);
      left: 50%;
      transform: translateX(-50%) translateY(-16px);
      background: #000000;
      color: #FFFFFF;
      border: 2px solid #000000;
      border-radius: 10px;
      padding: 10px 18px;
      font-size: 0.9rem;
      font-weight: 700;
      box-shadow: 4px 4px 0px rgba(0, 0, 0, 0.25);
      z-index: 3000;
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s ease;
      max-width: calc(100% - 32px);
      text-align: center;
    }

    .toast-banner.show {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }

    /* Barra de Navegação Inferior */
    .mobile-bottom-nav {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      height: calc(var(--bottom-nav-height) + env(safe-area-inset-bottom, 0px));
      background: #FFFFFF;
      border-top: var(--border-black);
      box-shadow: 0 -2px 0px #000000;
      display: flex;
      justify-content: space-around;
      align-items: center;
      padding: 0 8px;
      padding-bottom: env(safe-area-inset-bottom, 0px);
      z-index: 1000;
    }

    .nav-tab {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      color: var(--text-muted);
      font-size: 0.72rem;
      font-weight: 700;
      min-width: 60px;
      padding: 6px 4px;
      cursor: pointer;
      border: none;
      background: transparent;
      transition: all 0.15s ease;
    }

    .nav-tab .tab-icon {
      font-size: 1.3rem;
      line-height: 1;
    }

    .nav-tab.active {
      color: #000000;
    }

    .nav-tab.active .tab-icon {
      transform: translateY(-2px);
    }

    .nav-tab-accent {
      background: #000000;
      color: #FFFFFF !important;
      border-radius: 12px;
      padding: 6px 14px;
      box-shadow: 2px 2px 0px #000000;
    }

    .nav-tab-accent:active {
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0px #000000;
    }

    /* Container Principal */
    .main-container {
      width: min(600px, calc(100% - 24px));
      margin: 16px auto;
    }

    .view-section {
      display: none;
    }

    .view-section.active {
      display: block;
      animation: fadeIn 0.2s ease-in-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .page-header {
      background: #FFFFFF;
      border: var(--border-black);
      border-radius: 14px;
      padding: 16px 18px;
      box-shadow: var(--shadow-dry-lg);
      margin-bottom: 18px;
    }

    .eyebrow {
      font-size: 0.74rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #000000;
      margin-bottom: 4px;
      display: block;
    }

    .page-header h1 {
      font-size: 1.55rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.25;
      color: #000000;
      word-break: break-word;
    }

    .page-header p {
      font-size: 0.92rem;
      color: #4A4A4A;
      font-weight: 500;
      margin-top: 4px;
    }

    /* Cards Neo-Brutalist */
    .panel {
      background: #FFFFFF;
      border: var(--border-black);
      border-radius: 14px;
      padding: 20px;
      box-shadow: var(--shadow-dry-lg);
      margin-bottom: 18px;
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 2px solid #000000;
    }

    .panel-header h2 {
      font-size: 1.18rem;
      font-weight: 700;
      color: #000000;
    }

    /* Botões */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border-radius: 8px;
      padding: 12px 18px;
      font-size: 0.95rem;
      font-weight: 600;
      font-family: var(--font-main);
      cursor: pointer;
      transition: all 0.15s ease-in-out;
      text-align: center;
      min-height: 44px;
    }

    .btn-primary {
      background-color: #000000;
      color: #FFFFFF;
      border: 2px solid #000000;
      box-shadow: var(--shadow-dry-md);
    }

    .btn-primary:active {
      transform: translate(2px, 2px);
      box-shadow: 1px 1px 0px #000000;
    }

    .btn-secondary {
      background-color: #FFFFFF;
      color: #000000;
      border: 2px solid #000000;
      box-shadow: var(--shadow-dry-sm);
    }

    .btn-secondary:active {
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0px #000000;
    }

    .btn-danger {
      background-color: #FFFFFF;
      color: #B91C1C;
      border: 2px solid #000000;
      box-shadow: var(--shadow-dry-sm);
    }

    .btn-danger:active {
      background-color: #FEF2F2;
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0px #000000;
    }

    .btn-small {
      padding: 8px 12px;
      font-size: 0.85rem;
      min-height: 36px;
    }

    .btn-block {
      width: 100%;
    }

    /* Formulários */
    .form-group {
      margin-bottom: 14px;
    }

    .form-group label {
      display: block;
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 6px;
      color: #000000;
    }

    .input-field {
      width: 100%;
      background-color: #FFFFFF;
      color: #000000;
      border: 2px solid #000000;
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 1rem;
      font-family: var(--font-main);
      font-weight: 500;
      transition: all 0.15s ease;
    }

    .input-field:focus {
      outline: none;
      box-shadow: var(--shadow-dry-sm);
      transform: translate(-1px, -1px);
    }

    .input-field.input-error {
      border-color: #B91C1C;
      background-color: #FEF2F2;
    }

    .error-hint {
      color: #B91C1C;
      font-size: 0.82rem;
      font-weight: 700;
      margin-top: 5px;
      display: none;
    }

    .error-hint.visible {
      display: block;
    }

    .input-field::placeholder {
      color: var(--text-muted);
    }

    /* Cards de Lista */
    .record-item {
      background: #FFFFFF;
      border: var(--border-black);
      border-radius: 12px;
      padding: 16px;
      box-shadow: var(--shadow-dry-md);
      margin-bottom: 14px;
    }

    .list-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }

    .badge-pill {
      display: inline-block;
      background: #000000;
      color: #FFFFFF;
      padding: 3px 10px;
      border-radius: 99px;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .list-card-title {
      font-size: 1.2rem;
      font-weight: 800;
      color: #000000;
      margin-bottom: 4px;
    }

    .list-card-desc {
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-bottom: 14px;
    }

    .list-card-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding-top: 10px;
      border-top: 1.5px solid #000000;
    }

    /* Itens dentro da Lista */
    .shopping-item-card {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      background: #FFFFFF;
      border: var(--border-black);
      border-radius: 10px;
      box-shadow: var(--shadow-dry-sm);
      margin-bottom: 10px;
      transition: all 0.15s ease;
    }

    .shopping-item-card.is-bought {
      background: #F4F4F4;
      border-color: #757575;
      box-shadow: none;
      opacity: 0.85;
    }

    .shopping-item-card.is-bought .item-title {
      text-decoration: line-through;
      color: #757575;
    }

    .item-check-toggle {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      border: 2px solid #000000;
      background: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      flex-shrink: 0;
      font-weight: 900;
      color: #000000;
    }

    .shopping-item-card.is-bought .item-check-toggle {
      background: #000000;
      color: #FFFFFF;
    }

    .item-info {
      flex: 1;
      min-width: 0;
    }

    .item-title {
      font-weight: 700;
      font-size: 1.05rem;
      word-break: break-word;
      color: #000000;
    }

    .item-subtext {
      font-size: 0.84rem;
      color: var(--text-muted);
      margin-top: 2px;
      font-family: var(--font-mono);
      font-weight: 600;
    }

    /* Resumo Carrinho */
    .cart-summary-box {
      background: #FFFFFF;
      border: var(--border-black);
      border-radius: 12px;
      padding: 16px 20px;
      box-shadow: var(--shadow-dry-lg);
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .cart-summary-box .label {
      font-size: 0.8rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #000000;
    }

    .cart-summary-box .total {
      font-family: var(--font-mono);
      font-size: 2rem;
      font-weight: 800;
      color: #000000;
    }

    /* Modais */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.6);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      z-index: 2000;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-dialog {
      background: #FFFFFF;
      border: var(--border-black);
      border-radius: 14px;
      padding: 24px;
      width: min(440px, 100%);
      box-shadow: 6px 6px 0px #000000;
    }

    .modal-dialog h3 {
      font-size: 1.25rem;
      font-weight: 800;
      margin-bottom: 10px;
    }

    .modal-dialog p {
      font-size: 0.95rem;
      color: #000000;
      margin-bottom: 20px;
      line-height: 1.5;
    }

    .modal-actions {
      display: flex;
      gap: 10px;
      justify-content: flex-end;
    }

    .empty-state {
      text-align: center;
      padding: 32px 16px;
      background: #FFFFFF;
      border: var(--border-black);
      border-radius: 14px;
      box-shadow: var(--shadow-dry-md);
      margin: 16px 0;
    }

    .empty-state p {
      color: var(--text-muted);
      font-size: 0.95rem;
      margin-bottom: 14px;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div id="toast-banner" class="toast-banner"></div>

  <!-- Topbar Fixa -->
  <header class="app-topbar">
    <div style="display: flex; align-items: center; gap: 8px; min-width: 0;">
      <button type="button" id="ios-topbar-back-btn" class="topbar-back-btn" onclick="app.voltarTelaAnterior()">‹ Voltar</button>
      <div class="topbar-brand" onclick="app.mostrarView('view-home')" style="cursor: pointer;">
        <div class="brand-icon">📝</div>
        <span>NumEsquece Lista</span>
      </div>
    </div>
    <button type="button" class="topbar-action-btn" onclick="app.abrirCriarLista()">+ Nova Lista</button>
  </header>

  <!-- Container Mobile -->
  <main class="main-container">
    <!-- View 1: Início -->
    <section id="view-home" class="view-section active">
      <div class="page-header">
        <span class="eyebrow">Aplicativo Mobile</span>
        <h1>Minhas Compras</h1>
        <p>Gerencie listas e acompanhe gastos direto na memória do aparelho.</p>
      </div>

      <div id="ios-pwa-install-banner" class="panel" style="display: none;">
        <div class="panel-header">
          <h2>Instalar no iPhone (iOS)</h2>
        </div>
        <p style="font-size: 0.9rem; color: #333333; line-height: 1.55;">
          Para instalar na Tela de Início como aplicativo: toque no botão <strong>Compartilhar (⬆️)</strong> do Safari e selecione <strong>"Adicionar à Tela de Início"</strong>.
        </p>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h2>Acesso Rápido</h2>
        </div>
        <div style="display: flex; flex-direction: column; gap: 12px;">
          <button type="button" class="btn btn-primary btn-block" onclick="app.mostrarView('view-lists')">
            <span>📋 Ver Minhas Listas</span>
          </button>
          <button type="button" class="btn btn-secondary btn-block" onclick="app.abrirCriarLista()">
            <span>➕ Criar Nova Lista</span>
          </button>
          <button type="button" class="btn btn-secondary btn-block" onclick="app.mostrarView('view-history')">
            <span>📜 Histórico de Compras</span>
          </button>
          <button type="button" class="btn btn-secondary btn-block" onclick="app.abrirModalTransferencia('import', null)">
            <span>📡 Bluetooth & Arquivos</span>
          </button>
        </div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h2>Armazenamento Offline</h2>
        </div>
        <p style="font-size: 0.92rem; color: var(--text-muted); line-height: 1.6;">
          Suas listas, produtos e histórico ficam salvos em objetos de classes diretamente na <strong>memória local do dispositivo</strong>. Funciona 100% offline.
        </p>
      </div>
    </section>

    <!-- View 2: Minhas Listas -->
    <section id="view-lists" class="view-section">
      <div class="page-header" style="display: flex; justify-content: space-between; align-items: center; gap: 12px;">
        <div style="flex: 1; min-width: 0;">
          <span class="eyebrow">Organização</span>
          <h1>Minhas Listas</h1>
          <p>Toque para adicionar itens ou iniciar compras.</p>
        </div>
        <button type="button" class="btn btn-primary btn-small" style="flex-shrink: 0;" onclick="app.abrirCriarLista()">+ Nova</button>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px;">
        <button type="button" class="btn btn-secondary btn-small" style="padding: 11px 10px;" onclick="app.abrirModalTransferencia('import', null)">
          <span>📥 Importar Arquivo</span>
        </button>
        <button type="button" class="btn btn-secondary btn-small" style="padding: 11px 10px;" onclick="app.abrirModalTransferencia('export', null)">
          <span>📤 Via Bluetooth</span>
        </button>
      </div>

      <div id="lists-container"></div>
    </section>

    <!-- View 3: Detalhes / Adição de Itens -->
    <section id="view-list-detail" class="view-section">
      <div class="page-header">
        <span class="eyebrow">Lista Selecionada</span>
        <h1 id="detail-list-title">Nome da Lista</h1>
        <p id="detail-list-desc">Descrição</p>
      </div>

      <div style="margin-bottom: 16px; display: flex; gap: 8px; flex-wrap: wrap;">
        <button type="button" class="btn btn-primary" style="flex: 2; min-width: 150px;" onclick="app.iniciarCompras()">
          <span>🛒 Vamos Comprar?</span>
        </button>
        <button type="button" class="btn btn-secondary btn-small" onclick="app.abrirModalTransferencia('export', app.listaAtualId)" title="Enviar via Bluetooth ou Arquivo">📡 Enviar</button>
        <button type="button" class="btn btn-secondary btn-small" onclick="app.voltarOuIrPara('view-lists')">Voltar</button>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h2>Adicionar Produto</h2>
        </div>
        <form id="form-add-item" onsubmit="event.preventDefault(); app.adicionarItem(); return false;">
          <div class="form-group">
            <label for="item-name-input">Nome do item</label>
            <input type="text" id="item-name-input" class="input-field" placeholder="Ex: Arroz 5kg, Café..." />
            <div id="item-name-error" class="error-hint">Digite o nome do produto para adicionar.</div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <div class="form-group">
              <label for="item-qty-input">Quantidade</label>
              <input type="text" id="item-qty-input" inputmode="decimal" class="input-field" value="1" />
            </div>
            <div class="form-group">
              <label for="item-price-input">Preço estimado (R$)</label>
              <input type="text" id="item-price-input" inputmode="numeric" class="input-field" value="0,00" />
            </div>
          </div>
          <button type="button" class="btn btn-primary btn-block" onclick="app.adicionarItem()">+ Adicionar à Lista</button>
        </form>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h2>Itens Cadastrados</h2>
          <span class="badge-pill" id="items-count-badge">0 itens</span>
        </div>
        <div id="items-list-container"></div>
      </div>
    </section>

    <!-- View 4: Modo Supermercado -->
    <section id="view-shopping" class="view-section">
      <div class="page-header" style="display: flex; justify-content: space-between; align-items: center; gap: 12px;">
        <div style="flex: 1; min-width: 0;">
          <span class="eyebrow">Modo Mercado</span>
          <h1 id="shop-list-title">Compras em Andamento</h1>
          <p>Coloque os produtos no carrinho e confira o total.</p>
        </div>
        <button type="button" class="btn btn-secondary btn-small" style="flex-shrink: 0;" onclick="app.voltarParaDetalhes()">Voltar</button>
      </div>

      <div class="cart-summary-box">
        <div>
          <span class="label">Valor no Carrinho</span>
          <div class="total" id="shop-cart-total">R$ 0,00</div>
        </div>
        <button type="button" class="btn btn-primary btn-small" onclick="app.abrirModalFinalizar()">Finalizar</button>
      </div>

      <div style="display: flex; gap: 8px; margin-bottom: 14px;">
        <button type="button" class="btn btn-secondary btn-small" style="flex: 1;" onclick="app.moverTudoCarrinho()">Mover tudo pro carrinho</button>
        <button type="button" class="btn btn-secondary btn-small" onclick="app.abrirModalItemRapido()">+ Item rápido</button>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h2>Produtos na Prateleira</h2>
          <span class="badge-pill" id="shelf-count-badge">0</span>
        </div>
        <div id="shop-shelf-container"></div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <h2>Dentro do Carrinho 🛒</h2>
          <span class="badge-pill" id="cart-count-badge">0</span>
        </div>
        <div id="shop-cart-container"></div>
      </div>
    </section>

    <!-- View 5: Histórico -->
    <section id="view-history" class="view-section">
      <div class="page-header">
        <span class="eyebrow">Registro de Despesas</span>
        <h1>Histórico de Compras</h1>
        <p>Compras finalizadas e salvas localmente no aparelho.</p>
      </div>

      <div id="history-container"></div>
    </section>

    <!-- View 6: Criar / Editar Lista -->
    <section id="view-create-list" class="view-section">
      <div class="page-header">
        <span class="eyebrow">Nova Lista</span>
        <h1 id="create-view-heading">Criar Nova Lista</h1>
        <p>Defina o nome e toque em salvar para adicionar seus produtos.</p>
      </div>

      <div class="panel">
        <form id="form-create-list" onsubmit="event.preventDefault(); app.salvarLista(); return false;">
          <input type="hidden" id="edit-list-id" value="" />
          <div class="form-group">
            <label for="list-title-input">Nome da Lista</label>
            <input type="text" id="list-title-input" class="input-field" placeholder="Ex: Compras da Semana, Feira..." />
            <div id="list-title-error" class="error-hint">Por favor, informe um nome para a lista.</div>
          </div>
          <div class="form-group">
            <label for="list-desc-input">Descrição (opcional)</label>
            <textarea id="list-desc-input" class="input-field" style="min-height: 80px; resize: vertical;" placeholder="Observações, mercado..."></textarea>
          </div>
          <div style="display: flex; gap: 10px; margin-top: 18px;">
            <button type="button" class="btn btn-primary" style="flex: 2;" onclick="app.salvarLista()">Salvar Lista</button>
            <button type="button" class="btn btn-secondary" style="flex: 1;" onclick="app.voltarCancelarCriacao()">Cancelar</button>
          </div>
        </form>
      </div>
    </section>
  </main>

  <!-- Modal Finalizar Compra -->
  <div id="finish-modal" class="modal-overlay">
    <div class="modal-dialog">
      <h3>Finalizar Compra?</h3>
      <p id="finish-modal-msg">Deseja concluir a compra e salvar no histórico local?</p>
      <div class="modal-actions">
        <button type="button" class="btn btn-secondary" onclick="app.fecharModalFinalizar()">Continuar</button>
        <button type="button" class="btn btn-primary" onclick="app.executarFinalizacao()">Sim, Finalizar</button>
      </div>
    </div>
  </div>

  <!-- Modal Excluir Lista -->
  <div id="delete-modal" class="modal-overlay">
    <div class="modal-dialog">
      <h3>Excluir Lista?</h3>
      <p id="delete-modal-msg">Deseja realmente excluir esta lista?</p>
      <div class="modal-actions">
        <button type="button" class="btn btn-secondary" onclick="app.fecharModalExclusao()">Cancelar</button>
        <button type="button" class="btn btn-danger" onclick="app.executarExclusaoLista()">Sim, Excluir</button>
      </div>
    </div>
  </div>

  <!-- Modal Item Rápido -->
  <div id="quick-add-modal" class="modal-overlay">
    <div class="modal-dialog">
      <h3>+ Item Rápido no Carrinho</h3>
      <div class="form-group">
        <label for="quick-item-name">Nome do produto</label>
        <input type="text" id="quick-item-name" class="input-field" placeholder="Ex: Chocolate, Água..." />
      </div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div class="form-group">
          <label for="quick-item-qty">Qtd</label>
          <input type="text" id="quick-item-qty" inputmode="decimal" class="input-field" value="1" />
        </div>
        <div class="form-group">
          <label for="quick-item-price">Preço (R$)</label>
          <input type="text" id="quick-item-price" inputmode="numeric" class="input-field" value="0,00" />
        </div>
      </div>
      <div class="modal-actions">
        <button type="button" class="btn btn-secondary" onclick="app.fecharModalItemRapido()">Cancelar</button>
        <button type="button" class="btn btn-primary" onclick="app.executarAdicaoRapida()">Adicionar</button>
      </div>
    </div>
  </div>

  <!-- Modal Editar Produto -->
  <div id="edit-item-modal" class="modal-overlay">
    <div class="modal-dialog">
      <h3>✏️ Editar Produto</h3>
      <form id="form-edit-item" onsubmit="event.preventDefault(); app.salvarEdicaoItem(); return false;">
        <div class="form-group">
          <label for="edit-item-name">Nome do produto</label>
          <input type="text" id="edit-item-name" class="input-field" placeholder="Ex: Arroz 5kg, Café..." />
          <div id="edit-item-name-error" class="error-hint">Digite o nome do produto para salvar.</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
          <div class="form-group">
            <label for="edit-item-qty">Quantidade</label>
            <input type="text" id="edit-item-qty" inputmode="decimal" class="input-field" value="1" />
          </div>
          <div class="form-group">
            <label for="edit-item-price">Preço (R$)</label>
            <input type="text" id="edit-item-price" inputmode="numeric" class="input-field" value="0,00" />
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" onclick="app.fecharModalEditarItem()">Cancelar</button>
          <button type="button" class="btn btn-primary" onclick="app.salvarEdicaoItem()">Salvar</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Modal Bluetooth / Importar e Exportar Arquivos -->
  <div id="transfer-modal" class="modal-overlay">
    <div class="modal-dialog" style="max-height: 88vh; overflow-y: auto;">
      <h3>📡 Bluetooth & Ficheiros</h3>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 14px;">
        <button type="button" id="tab-transfer-export" class="btn btn-secondary btn-small" onclick="app.alternarModoTransferencia('export')">📤 Enviar / Exportar</button>
        <button type="button" id="tab-transfer-import" class="btn btn-primary btn-small" onclick="app.alternarModoTransferencia('import')">📥 Importar Ficheiro</button>
      </div>

      <div id="transfer-status-box" style="display: none; border: 2px solid #000000; background: #F5F5F5; border-radius: 10px; padding: 10px 12px; margin-bottom: 12px; font-size: 0.85rem; font-weight: 700;"></div>

      <div id="transfer-pane-export" style="display: none;">
        <p id="transfer-export-desc" style="font-size: 0.88rem; margin-bottom: 12px; line-height: 1.5;">
          Gere o arquivo da lista e envie via Bluetooth, AirDrop ou outro app.
        </p>
        <div class="form-group">
          <label for="transfer-scope-select">O que enviar?</label>
          <select id="transfer-scope-select" class="input-field" onchange="app.atualizarResumoExportacao()">
            <option value="all">Todas as minhas listas</option>
          </select>
        </div>
        <div style="background: #F5F5F5; border: 1.5px solid #000000; border-radius: 10px; padding: 10px 12px; margin-bottom: 14px; font-size: 0.84rem;">
          <strong>Arquivo:</strong> <span id="transfer-filename-preview" style="font-family: var(--font-mono);">listas_numesquece.json</span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 10px;">
          <button type="button" class="btn btn-primary btn-block" onclick="app.executarExportacaoBluetooth()">
            <span>📡 Enviar via Bluetooth / Compartilhar</span>
          </button>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <button type="button" class="btn btn-secondary btn-small" onclick="app.baixarJsonLista()">💾 Salvar Ficheiro</button>
            <button type="button" class="btn btn-secondary btn-small" onclick="app.copiarJsonTransferencia()">📋 Copiar JSON</button>
          </div>
        </div>
      </div>

      <div id="transfer-pane-import" style="display: block;">
        <p id="transfer-import-desc" style="font-size: 0.88rem; margin-bottom: 12px; line-height: 1.5;">
          Solicite acesso aos arquivos do celular (pastas <strong>Downloads</strong>, <strong>Bluetooth</strong> ou <strong>Arquivos</strong>) para carregar, editar e usar a lista recebida.
        </p>
        <input type="file" id="transfer-file-input" accept=".json,.numesquece,.txt,application/json,text/plain" style="display: none;" />
        <button type="button" class="btn btn-primary btn-block" onclick="app.solicitarImportacaoArquivo()" style="margin-bottom: 12px;">
          <span>📂 Procurar Listas nos Ficheiros do Celular</span>
        </button>

        <div class="form-group" style="margin-top: 8px;">
          <label for="transfer-json-paste">Ou cole o conteúdo JSON recebido (opcional)</label>
          <textarea id="transfer-json-paste" class="input-field" style="min-height: 76px; font-family: var(--font-mono); font-size: 0.8rem;" placeholder='{"app":"NumEsqueceLista","listas":[...]}'></textarea>
        </div>
        <button type="button" class="btn btn-secondary btn-block btn-small" onclick="app.importarTextoColado()" style="margin-bottom: 6px;">
          <span>📥 Importar JSON Colado</span>
        </button>
      </div>

      <div class="modal-actions" style="margin-top: 14px;">
        <button type="button" class="btn btn-secondary btn-block" onclick="app.fecharModalTransferencia()">Fechar</button>
      </div>
    </div>
  </div>

  <!-- Bottom Navigation Bar (Exclusivo Mobile) -->
  <nav class="mobile-bottom-nav">
    <button type="button" class="nav-tab active" data-view="view-home" onclick="app.mostrarView('view-home')">
      <span class="tab-icon">🏠</span>
      <span>Início</span>
    </button>
    <button type="button" class="nav-tab" data-view="view-lists" onclick="app.mostrarView('view-lists')">
      <span class="tab-icon">📋</span>
      <span>Listas</span>
    </button>
    <button type="button" class="nav-tab nav-tab-accent" data-view="view-create-list" onclick="app.abrirCriarLista()">
      <span class="tab-icon">➕</span>
      <span>Nova</span>
    </button>
    <button type="button" class="nav-tab" data-view="view-history" onclick="app.mostrarView('view-history')">
      <span class="tab-icon">📜</span>
      <span>Histórico</span>
    </button>
  </nav>

  <script>
    const IS_IOS_PLATFORM = __IS_IOS__;
    const IS_PWA_MODE = __IS_PWA__;

    // =========================================================================
    // CLASSES ORIENTADAS A OBJETOS PARA ARMAZENAMENTO NA MEMÓRIA LOCAL
    // =========================================================================

    class ItemProduto {
      constructor({ id = null, nome = '', quantidade = '1', preco = '0,00', comprado = false } = {}) {
        this.id = id !== null ? id : Date.now() + Math.floor(Math.random() * 10000);
        this.nome = String(nome).trim();
        this.quantidade = String(quantidade || '1').trim();
        this.preco = String(preco || '0,00').trim();
        this.comprado = Boolean(comprado);
      }

      precoNumerico() {
        const str = String(this.preco || '0,00').replace(/\./g, '').replace(',', '.');
        const val = parseFloat(str);
        return isNaN(val) ? 0 : val;
      }

      quantidadeNumerica() {
        const str = String(this.quantidade || '1').replace(',', '.');
        const val = parseFloat(str);
        return isNaN(val) || val <= 0 ? 1 : val;
      }

      calcularSubtotal() {
        return this.precoNumerico() * this.quantidadeNumerica();
      }

      alternarComprado() {
        this.comprado = !this.comprado;
      }

      toJSON() {
        return {
          id: this.id,
          nome: this.nome,
          quantidade: this.quantidade,
          preco: this.preco,
          comprado: this.comprado
        };
      }

      static fromJSON(obj) {
        return new ItemProduto({
          id: obj.id,
          nome: obj.nome,
          quantidade: obj.quantidade,
          preco: obj.preco,
          comprado: obj.comprado ?? obj.is_bought ?? false
        });
      }
    }

    class ListaDeCompras {
      constructor({ id = null, titulo = '', descricao = '', atualizadoEm = null, itens = [] } = {}) {
        this.id = id !== null ? id : Date.now();
        this.titulo = String(titulo).trim();
        this.descricao = String(descricao || '').trim();
        this.atualizadoEm = atualizadoEm || new Date().toISOString();
        this.itens = (itens || []).map(it => it instanceof ItemProduto ? it : ItemProduto.fromJSON(it));
      }

      adicionarItem(nome, quantidade = '1', preco = '0,00', comprado = false) {
        const novoItem = new ItemProduto({ nome, quantidade, preco, comprado });
        this.itens.push(novoItem);
        this.atualizadoEm = new Date().toISOString();
        return novoItem;
      }

      editarItem(itemId, nome, quantidade = '1', preco = '0,00') {
        const item = this.buscarItem(itemId);
        if (!item) return null;
        item.nome = String(nome || '').trim();
        item.quantidade = String(quantidade || '1').trim() || '1';
        item.preco = String(preco || '0,00').trim() || '0,00';
        this.atualizadoEm = new Date().toISOString();
        return item;
      }

      removerItem(itemId) {
        this.itens = this.itens.filter(it => String(it.id) !== String(itemId));
        this.atualizadoEm = new Date().toISOString();
      }

      buscarItem(itemId) {
        return this.itens.find(it => String(it.id) === String(itemId)) || null;
      }

      toJSON() {
        return {
          id: this.id,
          titulo: this.titulo,
          descricao: this.descricao,
          atualizadoEm: this.atualizadoEm,
          itens: this.itens.map(it => it.toJSON())
        };
      }

      static fromJSON(obj) {
        return new ListaDeCompras({
          id: obj.id,
          titulo: obj.titulo,
          descricao: obj.descricao,
          atualizadoEm: obj.atualizadoEm || obj.updated_at,
          itens: obj.itens || obj.items || []
        });
      }
    }

    class CompraFinalizada {
      constructor({ id = null, titulo = '', dataCompra = null, totalCompra = 'R$ 0,00', itens = [] } = {}) {
        this.id = id !== null ? id : Date.now();
        this.titulo = String(titulo).trim();
        this.dataCompra = dataCompra || new Date().toISOString();
        this.totalCompra = totalCompra;
        this.itens = (itens || []).map(it => it instanceof ItemProduto ? it : ItemProduto.fromJSON(it));
      }

      toJSON() {
        return {
          id: this.id,
          titulo: this.titulo,
          dataCompra: this.dataCompra,
          totalCompra: this.totalCompra,
          itens: this.itens.map(it => it.toJSON())
        };
      }

      static fromJSON(obj) {
        return new CompraFinalizada({
          id: obj.id,
          titulo: obj.titulo,
          dataCompra: obj.dataCompra || obj.data_compra,
          totalCompra: obj.totalCompra || obj.total_compra,
          itens: obj.itens || obj.items || []
        });
      }
    }

    class ArmazenamentoLocal {
      constructor() {
        this.CHAVE_LISTAS = 'num_esquece_mobile_listas_v2';
        this.CHAVE_HISTORICO = 'num_esquece_mobile_historico_v2';
        this.memoria = {};
        this.db = null;
        this.listas = [];
        this.historico = [];
      }

      inicializar(onPronto) {
        this.carregarDadosSincrono();
        try {
          if (!window.indexedDB) {
            if (onPronto) onPronto();
            return;
          }
          const req = window.indexedDB.open('NumEsqueceMemoriaDB', 1);
          req.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains('dados')) {
              db.createObjectStore('dados');
            }
          };
          req.onsuccess = (e) => {
            this.db = e.target.result;
            const tx = this.db.transaction('dados', 'readonly');
            const store = tx.objectStore('dados');
            const r1 = store.get(this.CHAVE_LISTAS);
            const r2 = store.get(this.CHAVE_HISTORICO);
            tx.oncomplete = () => {
              if (r1.result && !this.lerLocalStorage(this.CHAVE_LISTAS)) {
                this.gravarLocalStorage(this.CHAVE_LISTAS, r1.result);
                this.carregarDadosSincrono();
              }
              if (r2.result && !this.lerLocalStorage(this.CHAVE_HISTORICO)) {
                this.gravarLocalStorage(this.CHAVE_HISTORICO, r2.result);
                this.carregarDadosSincrono();
              }
              if (onPronto) onPronto();
            };
            tx.onerror = () => { if (onPronto) onPronto(); };
          };
          req.onerror = () => { if (onPronto) onPronto(); };
        } catch (err) {
          if (onPronto) onPronto();
        }
      }

      lerLocalStorage(chave) {
        if (this.memoria[chave]) return this.memoria[chave];
        try {
          if (window.__IOS_PRELOADED_DATA__ && window.__IOS_PRELOADED_DATA__[chave]) {
            const rawIos = typeof window.__IOS_PRELOADED_DATA__[chave] === 'string'
              ? window.__IOS_PRELOADED_DATA__[chave]
              : JSON.stringify(window.__IOS_PRELOADED_DATA__[chave]);
            this.memoria[chave] = rawIos;
            return rawIos;
          }
        } catch (e) {}
        try {
          if (window.localStorage) {
            const raw = window.localStorage.getItem(chave);
            if (raw) {
              this.memoria[chave] = raw;
              return raw;
            }
          }
        } catch (e) {}
        return null;
      }

      gravarLocalStorage(chave, valorJson) {
        this.memoria[chave] = valorJson;
        try {
          if (window.localStorage) {
            window.localStorage.setItem(chave, valorJson);
          }
        } catch (e) {}
        try {
          if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.iosStorage) {
            window.webkit.messageHandlers.iosStorage.postMessage({ chave, valor: valorJson });
          }
        } catch (e) {}
        try {
          if (this.db) {
            const tx = this.db.transaction('dados', 'readwrite');
            tx.objectStore('dados').put(valorJson, chave);
          }
        } catch (e) {}
      }

      carregarDadosSincrono() {
        const rawListas = this.lerLocalStorage(this.CHAVE_LISTAS);
        if (rawListas) {
          try {
            const arr = JSON.parse(rawListas);
            if (Array.isArray(arr)) {
              this.listas = arr.map(obj => ListaDeCompras.fromJSON(obj));
            }
          } catch (e) { this.listas = []; }
        } else {
          // Lista inicial padrão de exemplo
          const exemplo = new ListaDeCompras({
            id: 1,
            titulo: 'Compras do Mês',
            descricao: 'Itens essenciais para a casa',
            itens: [
              new ItemProduto({ id: 101, nome: 'Arroz 5kg', quantidade: '2', preco: '28,90' }),
              new ItemProduto({ id: 102, nome: 'Feijão Carioca 1kg', quantidade: '3', preco: '7,49' }),
              new ItemProduto({ id: 103, nome: 'Café 500g', quantidade: '2', preco: '16,50' })
            ]
          });
          this.listas = [exemplo];
          this.salvarListas();
        }

        const rawHist = this.lerLocalStorage(this.CHAVE_HISTORICO);
        if (rawHist) {
          try {
            const arrH = JSON.parse(rawHist);
            if (Array.isArray(arrH)) {
              this.historico = arrH.map(obj => CompraFinalizada.fromJSON(obj));
            }
          } catch (e) { this.historico = []; }
        }
      }

      salvarListas() {
        const payload = JSON.stringify(this.listas.map(l => l.toJSON()));
        this.gravarLocalStorage(this.CHAVE_LISTAS, payload);
      }

      salvarHistorico() {
        const payload = JSON.stringify(this.historico.map(c => c.toJSON()));
        this.gravarLocalStorage(this.CHAVE_HISTORICO, payload);
      }

      obterListas() {
        return this.listas;
      }

      buscarLista(listaId) {
        return this.listas.find(l => String(l.id) === String(listaId)) || null;
      }

      criarLista(titulo, descricao) {
        const nova = new ListaDeCompras({ titulo, descricao, itens: [] });
        this.listas.unshift(nova);
        this.salvarListas();
        return nova;
      }

      atualizarLista(listaId, titulo, descricao) {
        const lista = this.buscarLista(listaId);
        if (!lista) return null;
        lista.titulo = titulo;
        lista.descricao = descricao;
        lista.atualizadoEm = new Date().toISOString();
        this.salvarListas();
        return lista;
      }

      duplicarLista(listaId) {
        const orig = this.buscarLista(listaId);
        if (!orig) return null;
        const itensCopiados = orig.itens.map(it => new ItemProduto({
          nome: it.nome,
          quantidade: it.quantidade,
          preco: it.preco,
          comprado: false
        }));
        const copia = new ListaDeCompras({
          titulo: `${orig.titulo} (Cópia)`,
          descricao: orig.descricao,
          itens: itensCopiados
        });
        this.listas.unshift(copia);
        this.salvarListas();
        return copia;
      }

      excluirLista(listaId) {
        this.listas = this.listas.filter(l => String(l.id) !== String(listaId));
        this.salvarListas();
      }

      registrarCompraFinalizada(lista, itensNoCarrinho, totalFormatado) {
        const itensCopia = itensNoCarrinho.map(it => new ItemProduto({
          nome: it.nome,
          quantidade: it.quantidade,
          preco: it.preco,
          comprado: true
        }));
        const compra = new CompraFinalizada({
          titulo: lista.titulo,
          totalCompra: totalFormatado,
          itens: itensCopia
        });
        this.historico.unshift(compra);
        this.salvarHistorico();

        lista.itens.forEach(it => {
          if (itensNoCarrinho.some(c => String(c.id) === String(it.id))) {
            it.comprado = true;
          }
        });
        this.salvarListas();
        return compra;
      }

      _gerarIdUnico(salto = 0) {
        return Date.now() + Math.floor(Math.random() * 10000) + salto;
      }

      exportarPacoteJSON(listaId = null, origem = null) {
        let listasAlvo = [];
        if (listaId !== null && listaId !== undefined && String(listaId) !== '' && String(listaId) !== 'all') {
          const encontrada = this.buscarLista(listaId);
          if (encontrada) listasAlvo = [encontrada];
        } else {
          listasAlvo = [...this.listas];
        }
        return JSON.stringify({
          app: 'NumEsqueceLista',
          versao: 1,
          exportadoEm: new Date().toISOString(),
          origem: origem || (IS_IOS_PLATFORM ? 'iOS' : 'Android'),
          listas: listasAlvo.map(l => l.toJSON())
        }, null, 2);
      }

      importarPacoteJSON(entrada) {
        let dados = entrada;
        if (typeof entrada === 'string') {
          const limpo = entrada.trim();
          if (!limpo) {
            throw new Error('Conteúdo JSON vazio.');
          }
          dados = JSON.parse(limpo);
        }

        let listasBrutas = [];
        if (dados && typeof dados === 'object' && Array.isArray(dados.listas)) {
          listasBrutas = dados.listas;
        } else if (Array.isArray(dados)) {
          listasBrutas = dados;
        } else if (dados && typeof dados === 'object' && (dados.titulo || Array.isArray(dados.itens))) {
          listasBrutas = [dados];
        } else {
          throw new Error('Formato de arquivo de lista inválido.');
        }

        const importadas = [];
        const idExistentes = new Set(this.listas.map(l => String(l.id)));

        listasBrutas.forEach((bruta, idx) => {
          if (!bruta || typeof bruta !== 'object') return;
          const titulo = String(bruta.titulo || '').trim();
          if (!titulo) return;

          let novoListaId = this._gerarIdUnico((idx + 1) * 37);
          while (idExistentes.has(String(novoListaId))) {
            novoListaId += 1;
          }
          idExistentes.add(String(novoListaId));

          const itensBrutos = Array.isArray(bruta.itens) ? bruta.itens : [];
          const itensObjetos = [];
          itensBrutos.forEach((it, itemIdx) => {
            if (!it || typeof it !== 'object') return;
            const nomeItem = String(it.nome || '').trim();
            if (!nomeItem) return;
            itensObjetos.push(new ItemProduto({
              id: this._gerarIdUnico((idx + 1) * 1000 + itemIdx + 1),
              nome: nomeItem,
              quantidade: String(it.quantidade !== undefined ? it.quantidade : '1'),
              preco: String(it.preco !== undefined ? it.preco : '0,00'),
              comprado: Boolean(it.comprado || it.no_carrinho)
            }));
          });

          const novaLista = new ListaDeCompras({
            id: novoListaId,
            titulo,
            descricao: String(bruta.descricao || bruta.subtitulo || ''),
            itens: itensObjetos
          });
          this.listas.unshift(novaLista);
          importadas.push(novaLista);
        });

        if (!importadas.length) {
          throw new Error('Nenhuma lista válida foi encontrada neste arquivo.');
        }

        this.salvarListas();
        return { totalImportadas: importadas.length, listas: importadas };
      }
    }

    // =========================================================================
    // CONTROLADOR DO APLICATIVO MOBILE
    // =========================================================================
    class AplicativoNumEsquece {
      constructor() {
        this.storage = new ArmazenamentoLocal();
        this.listaAtualId = null;
        this.listaExcluirId = null;
        this.itemEditarId = null;
        this.editandoListaId = null;
        this.transferListaId = null;
        this.transferModo = 'import';
        this.viewAtual = 'view-home';
        this.pilhaNavegacao = [];
        this._historyListenerRegistrado = false;
        this.carrinhoIds = new Set();
        this.toastTimer = null;
      }

      iniciar() {
        ['item-price-input', 'quick-item-price', 'edit-item-price'].forEach(id => {
          const el = document.getElementById(id);
          if (el) {
            el.addEventListener('input', () => {
              el.value = this.formatarCampoPreco(el.value);
            });
          }
        });

        const fileInp = document.getElementById('transfer-file-input');
        if (fileInp) {
          fileInp.addEventListener('change', (ev) => {
            const file = ev.target && ev.target.files && ev.target.files[0];
            if (!file) return;
            if (typeof FileReader === 'undefined') {
              this.toast('Leitor de arquivos indisponível neste ambiente.');
              return;
            }
            const reader = new FileReader();
            reader.onload = () => {
              try {
                this.receberArquivoImportado(String(reader.result || ''), file.name || 'lista.json');
              } catch (e) {
                this._mostrarStatusTransferencia(`❌ ${e.message || 'Erro ao ler arquivo.'}`);
              } finally {
                fileInp.value = '';
              }
            };
            reader.onerror = () => {
              this._mostrarStatusTransferencia('❌ Não foi possível ler o arquivo selecionado.');
              fileInp.value = '';
            };
            reader.readAsText(file, 'utf-8');
          });
        }

        const titleInp = document.getElementById('list-title-input');
        if (titleInp) titleInp.addEventListener('input', () => this.limparErroTitulo());

        const itemInp = document.getElementById('item-name-input');
        if (itemInp) itemInp.addEventListener('input', () => this.limparErroItem());

        const editItemInp = document.getElementById('edit-item-name');
        if (editItemInp) editItemInp.addEventListener('input', () => this.limparErroEdicaoItem());

        if (!this._historyListenerRegistrado && typeof window !== 'undefined' && typeof window.addEventListener === 'function') {
          window.addEventListener('popstate', (ev) => this.aoVoltarHistorico(ev));
          const emWKWebViewNativo = Boolean(window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.iosStorage);
          if (IS_IOS_PLATFORM && !emWKWebViewNativo) {
            let toqueInicioX = null;
            let toqueInicioY = null;
            window.addEventListener('touchstart', (ev) => {
              const t = ev.touches && ev.touches[0];
              if (t && t.clientX <= 30) {
                toqueInicioX = t.clientX;
                toqueInicioY = t.clientY;
              } else {
                toqueInicioX = null;
              }
            }, { passive: true });
            window.addEventListener('touchend', (ev) => {
              if (toqueInicioX === null) return;
              const t = ev.changedTouches && ev.changedTouches[0];
              if (t) {
                const dx = t.clientX - toqueInicioX;
                const dy = Math.abs(t.clientY - toqueInicioY);
                if (dx >= 75 && dy < 60 && this.viewAtual !== 'view-home') {
                  this.voltarTelaAnterior();
                }
              }
              toqueInicioX = null;
            }, { passive: true });
          }
          this._historyListenerRegistrado = true;
        }

        if (IS_IOS_PLATFORM && IS_PWA_MODE) {
          const banner = document.getElementById('ios-pwa-install-banner');
          const emStandalone = Boolean(
            (typeof window !== 'undefined' && window.navigator && window.navigator.standalone) ||
            (typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) ||
            (typeof window !== 'undefined' && window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.iosStorage)
          );
          if (banner && !emStandalone) {
            banner.style.display = 'block';
          }
          if (typeof navigator !== 'undefined' && navigator.serviceWorker && typeof navigator.serviceWorker.register === 'function') {
            navigator.serviceWorker.register('./sw.js').catch(() => {});
          }
        }

        this.storage.inicializar(() => {
          const active = document.querySelector('.view-section.active');
          if (active && active.id === 'view-lists') this.renderizarListas();
          if (active && active.id === 'view-history') this.renderizarHistorico();
        });

        this.mostrarView('view-home', { historyMode: 'replace' });
      }

      toast(msg) {
        const el = document.getElementById('toast-banner');
        if (!el) return;
        el.textContent = msg;
        el.classList.add('show');
        clearTimeout(this.toastTimer);
        this.toastTimer = setTimeout(() => el.classList.remove('show'), 2800);
      }

      escaparHtml(texto) {
        if (texto === null || texto === undefined) return '';
        return String(texto)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;')
          .replace(/'/g, '&#39;');
      }

      formatarCampoPreco(val) {
        const digits = String(val || '').replace(/\D/g, '');
        if (!digits) return '0,00';
        if (digits.length === 1) return '0,0' + digits;
        if (digits.length === 2) return '0,' + digits;
        const intPart = digits.slice(0, -2).replace(/^0+(?=\d)/, '') || '0';
        const decPart = digits.slice(-2);
        const formattedInt = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        return formattedInt + ',' + decPart;
      }

      formatarMoeda(valor) {
        try {
          return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
        } catch (e) {
          return 'R$ ' + valor.toFixed(2).replace('.', ',');
        }
      }

      _historicoDisponivel() {
        return (
          typeof window !== 'undefined' &&
          window.history &&
          typeof window.history.pushState === 'function' &&
          typeof window.history.replaceState === 'function'
        );
      }

      _montarEstadoNavegacao(viewId, extras = {}) {
        const ehDetalheOuMercado = viewId === 'view-list-detail' || viewId === 'view-shopping';
        const listaId = extras.listaAtualId !== undefined
          ? extras.listaAtualId
          : (ehDetalheOuMercado ? this.listaAtualId : null);
        const editId = extras.editListId !== undefined
          ? extras.editListId
          : (viewId === 'view-create-list' ? this.editandoListaId : null);
        return { viewId, listaAtualId: listaId, editListId: editId };
      }

      _montarHashNavegacao(estado) {
        if (estado.viewId === 'view-list-detail' && estado.listaAtualId) {
          return `#view-list-detail-${estado.listaAtualId}`;
        }
        if (estado.viewId === 'view-shopping' && estado.listaAtualId) {
          return `#view-shopping-${estado.listaAtualId}`;
        }
        if (estado.viewId === 'view-create-list' && estado.editListId) {
          return `#view-edit-list-${estado.editListId}`;
        }
        return `#${estado.viewId}`;
      }

      _estadosNavegacaoIguais(a, b) {
        return Boolean(
          a && b &&
          a.viewId === b.viewId &&
          String(a.listaAtualId || '') === String(b.listaAtualId || '') &&
          String(a.editListId || '') === String(b.editListId || '')
        );
      }

      _registrarHistorico(viewId, mode = 'push', extras = {}) {
        if (mode === 'none') return;
        const estado = this._montarEstadoNavegacao(viewId, extras);
        const hash = this._montarHashNavegacao(estado);
        const topo = this.pilhaNavegacao.length ? this.pilhaNavegacao[this.pilhaNavegacao.length - 1] : null;

        let modoEfetivo = mode;
        if (modoEfetivo === 'push' && this._estadosNavegacaoIguais(topo, estado)) {
          modoEfetivo = 'replace';
        }

        if (modoEfetivo === 'push') {
          this.pilhaNavegacao.push(estado);
        } else if (modoEfetivo === 'replace') {
          if (this.pilhaNavegacao.length) {
            this.pilhaNavegacao[this.pilhaNavegacao.length - 1] = estado;
          } else {
            this.pilhaNavegacao.push(estado);
          }
        }

        if (this._historicoDisponivel()) {
          try {
            if (modoEfetivo === 'push') {
              window.history.pushState(estado, '', hash);
            } else {
              window.history.replaceState(estado, '', hash);
            }
          } catch (e) {}
        }
      }

      fecharTodosModais() {
        this.fecharModalFinalizar();
        this.fecharModalExclusao();
        this.fecharModalItemRapido();
        this.fecharModalEditarItem();
        this.fecharModalTransferencia();
      }

      aoVoltarHistorico(event) {
        this.fecharTodosModais();
        const st = (event && event.state && event.state.viewId)
          ? event.state
          : { viewId: 'view-home', listaAtualId: null, editListId: null };

        if (this.pilhaNavegacao.length > 1) {
          this.pilhaNavegacao.pop();
        }

        if (st.viewId === 'view-list-detail' && st.listaAtualId) {
          this.abrirDetalhesLista(st.listaAtualId, { historyMode: 'none' });
        } else if (st.viewId === 'view-shopping' && st.listaAtualId) {
          this.abrirModoMercado(st.listaAtualId, { historyMode: 'none' });
        } else if (st.viewId === 'view-create-list') {
          if (st.editListId) {
            this.editarLista(st.editListId, { historyMode: 'none' });
          } else {
            this.abrirCriarLista({ historyMode: 'none' });
          }
        } else {
          this.mostrarView(st.viewId || 'view-home', { historyMode: 'none' });
        }
      }

      voltarOuIrPara(fallbackViewId) {
        const anterior = this.pilhaNavegacao.length >= 2
          ? this.pilhaNavegacao[this.pilhaNavegacao.length - 2]
          : null;
        if (anterior && anterior.viewId === fallbackViewId && this._historicoDisponivel() && typeof window.history.back === 'function') {
          window.history.back();
          return;
        }
        this.mostrarView(fallbackViewId);
      }

      voltarParaDetalhes() {
        const anterior = this.pilhaNavegacao.length >= 2
          ? this.pilhaNavegacao[this.pilhaNavegacao.length - 2]
          : null;
        if (
          anterior &&
          anterior.viewId === 'view-list-detail' &&
          String(anterior.listaAtualId || '') === String(this.listaAtualId || '') &&
          this._historicoDisponivel() &&
          typeof window.history.back === 'function'
        ) {
          window.history.back();
          return;
        }
        this.abrirDetalhesLista(this.listaAtualId);
      }

      voltarCancelarCriacao() {
        if (this.pilhaNavegacao.length >= 2 && this._historicoDisponivel() && typeof window.history.back === 'function') {
          window.history.back();
          return;
        }
        this.mostrarView('view-lists');
      }

      voltarTelaAnterior() {
        this.fecharTodosModais();
        if (this.pilhaNavegacao.length >= 2 && this._historicoDisponivel() && typeof window.history.back === 'function') {
          window.history.back();
          return;
        }
        if (this.viewAtual !== 'view-home') {
          this.mostrarView('view-home', { historyMode: 'replace' });
        }
      }

      atualizarBotaoVoltarTopo() {
        if (!IS_IOS_PLATFORM) return;
        const btn = document.getElementById('ios-topbar-back-btn');
        if (!btn) return;
        if (this.viewAtual !== 'view-home') {
          btn.style.display = 'inline-flex';
        } else {
          btn.style.display = 'none';
        }
      }

      mostrarView(viewId, opcoes = {}) {
        const historyMode = opcoes.historyMode || 'push';
        if (viewId !== 'view-create-list') {
          this.editandoListaId = null;
        }
        this.viewAtual = viewId;

        document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
        const target = document.getElementById(viewId);
        if (target) target.classList.add('active');

        document.querySelectorAll('.nav-tab').forEach(tab => {
          if (tab.dataset.view === viewId) tab.classList.add('active');
          else tab.classList.remove('active');
        });

        window.scrollTo(0, 0);

        if (viewId === 'view-lists') this.renderizarListas();
        if (viewId === 'view-history') this.renderizarHistorico();

        this._registrarHistorico(viewId, historyMode, opcoes.extras || {});
        this.atualizarBotaoVoltarTopo();
      }

      limparErroTitulo() {
        document.getElementById('list-title-input')?.classList.remove('input-error');
        document.getElementById('list-title-error')?.classList.remove('visible');
      }

      limparErroItem() {
        document.getElementById('item-name-input')?.classList.remove('input-error');
        document.getElementById('item-name-error')?.classList.remove('visible');
      }

      abrirCriarLista(opcoes = {}) {
        this.editandoListaId = null;
        document.getElementById('create-view-heading').textContent = 'Criar Nova Lista';
        document.getElementById('edit-list-id').value = '';
        document.getElementById('list-title-input').value = '';
        document.getElementById('list-desc-input').value = '';
        this.limparErroTitulo();
        this.mostrarView('view-create-list', {
          historyMode: opcoes.historyMode || 'push',
          extras: { editListId: null }
        });
        if (opcoes.historyMode !== 'none') {
          setTimeout(() => document.getElementById('list-title-input')?.focus(), 150);
        }
      }

      editarLista(listaId, opcoes = {}) {
        const lista = this.storage.buscarLista(listaId);
        if (!lista) {
          this.mostrarView('view-lists', { historyMode: 'replace' });
          return;
        }
        this.editandoListaId = lista.id;
        document.getElementById('create-view-heading').textContent = 'Editar Lista';
        document.getElementById('edit-list-id').value = lista.id;
        document.getElementById('list-title-input').value = lista.titulo;
        document.getElementById('list-desc-input').value = lista.descricao || '';
        this.limparErroTitulo();
        this.mostrarView('view-create-list', {
          historyMode: opcoes.historyMode || 'push',
          extras: { editListId: lista.id }
        });
      }

      salvarLista() {
        const inpTitle = document.getElementById('list-title-input');
        const inpDesc = document.getElementById('list-desc-input');
        const inpEdit = document.getElementById('edit-list-id');

        const titulo = (inpTitle.value || '').trim();
        const desc = (inpDesc.value || '').trim();
        const editId = (inpEdit.value || '').trim();

        if (!titulo) {
          inpTitle.classList.add('input-error');
          document.getElementById('list-title-error').classList.add('visible');
          inpTitle.focus();
          this.toast('Digite o nome da lista!');
          return;
        }

        let listaAlvo = null;
        if (editId) {
          listaAlvo = this.storage.atualizarLista(editId, titulo, desc);
        }
        if (!listaAlvo) {
          listaAlvo = this.storage.criarLista(titulo, desc);
        }

        inpTitle.value = '';
        inpDesc.value = '';
        inpEdit.value = '';
        this.editandoListaId = null;

        this.toast(editId ? '✓ Lista atualizada!' : '✓ Lista criada! Adicione os itens.');
        this.abrirDetalhesLista(listaAlvo.id, { historyMode: 'replace' });
      }

      duplicarLista(listaId) {
        this.storage.duplicarLista(listaId);
        this.renderizarListas();
        this.toast('✓ Lista duplicada!');
      }

      confirmarExclusaoLista(listaId) {
        this.listaExcluirId = listaId;
        const lista = this.storage.buscarLista(listaId);
        const nome = lista ? lista.titulo : 'esta lista';
        document.getElementById('delete-modal-msg').textContent = `Deseja excluir "${nome}" e todos os seus produtos?`;
        document.getElementById('delete-modal').classList.add('active');
      }

      fecharModalExclusao() {
        this.listaExcluirId = null;
        document.getElementById('delete-modal').classList.remove('active');
      }

      executarExclusaoLista() {
        if (this.listaExcluirId !== null) {
          this.storage.excluirLista(this.listaExcluirId);
        }
        this.fecharModalExclusao();
        this.renderizarListas();
        this.toast('🗑️ Lista excluída!');
      }

      renderizarListas() {
        const listas = this.storage.obterListas();
        const container = document.getElementById('lists-container');
        if (!listas.length) {
          container.innerHTML = `
            <div class="empty-state">
              <p>Nenhuma lista cadastrada ainda.</p>
              <button type="button" class="btn btn-primary" onclick="app.abrirCriarLista()">+ Criar Primeira Lista</button>
            </div>
          `;
          return;
        }

        container.innerHTML = listas.map(lista => {
          let dataStr = '';
          try { dataStr = new Date(lista.atualizadoEm).toLocaleDateString('pt-BR'); } catch (e) { dataStr = 'Hoje'; }
          const totalItens = lista.itens.length;
          return `
            <article class="record-item">
              <div class="list-card-header">
                <span class="badge-pill">🛒 ${totalItens} ${totalItens === 1 ? 'item' : 'itens'}</span>
                <span class="badge-pill">📅 ${dataStr}</span>
              </div>
              <h3 class="list-card-title" onclick="app.abrirDetalhesLista(${lista.id})" style="cursor: pointer;">${this.escaparHtml(lista.titulo)}</h3>
              <p class="list-card-desc">${this.escaparHtml(lista.descricao) || 'Toque para gerenciar os itens.'}</p>
              <div class="list-card-actions">
                <button type="button" class="btn btn-primary btn-small" onclick="app.abrirDetalhesLista(${lista.id})">📝 Ver / Add Itens</button>
                <button type="button" class="btn btn-secondary btn-small" onclick="app.abrirModoMercado(${lista.id})">🛒 Comprar</button>
                <button type="button" class="btn btn-secondary btn-small" onclick="app.abrirModalTransferencia('export', ${lista.id})" title="Enviar via Bluetooth ou Arquivo">📡</button>
                <button type="button" class="btn btn-secondary btn-small" onclick="app.editarLista(${lista.id})">✏️</button>
                <button type="button" class="btn btn-secondary btn-small" onclick="app.duplicarLista(${lista.id})">📋</button>
                <button type="button" class="btn btn-danger btn-small" onclick="app.confirmarExclusaoLista(${lista.id})">🗑️</button>
              </div>
            </article>
          `;
        }).join('');
      }

      abrirDetalhesLista(listaId, opcoes = {}) {
        const lista = this.storage.buscarLista(listaId);
        if (!lista) {
          this.mostrarView('view-lists', { historyMode: 'replace' });
          return;
        }
        this.listaAtualId = lista.id;
        document.getElementById('detail-list-title').textContent = lista.titulo;
        document.getElementById('detail-list-desc').textContent = lista.descricao || 'Lista de compras';
        this.limparErroItem();
        this.renderizarItensLista();
        this.mostrarView('view-list-detail', {
          historyMode: opcoes.historyMode || 'push',
          extras: { listaAtualId: lista.id }
        });
      }

      renderizarItensLista() {
        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista) return;
        const container = document.getElementById('items-list-container');
        const badge = document.getElementById('items-count-badge');
        const itens = lista.itens;
        badge.textContent = `${itens.length} ${itens.length === 1 ? 'item' : 'itens'}`;

        if (!itens.length) {
          container.innerHTML = '<div class="empty-state"><p>Nenhum produto cadastrado ainda.<br>Use o formulário acima para adicionar!</p></div>';
          return;
        }

        container.innerHTML = itens.map(item => `
          <div class="shopping-item-card ${item.comprado ? 'is-bought' : ''}">
            <button type="button" class="item-check-toggle" onclick="app.alternarItemComprado('${item.id}')">
              ${item.comprado ? '✓' : ''}
            </button>
            <div class="item-info">
              <div class="item-title">${this.escaparHtml(item.nome)}</div>
              <div class="item-subtext">Qtd: ${this.escaparHtml(item.quantidade)} · R$ ${this.escaparHtml(item.preco)}</div>
            </div>
            <div style="display: flex; align-items: center; gap: 6px; flex-shrink: 0;">
              <button type="button" class="btn btn-secondary btn-small" aria-label="Editar item" onclick="app.abrirEditarItem('${item.id}')">✏️</button>
              <button type="button" class="btn btn-danger btn-small" aria-label="Excluir item" onclick="app.removerItem('${item.id}')">🗑️</button>
            </div>
          </div>
        `).join('');
      }

      limparErroEdicaoItem() {
        document.getElementById('edit-item-name')?.classList.remove('input-error');
        document.getElementById('edit-item-name-error')?.classList.remove('visible');
      }

      abrirEditarItem(itemId) {
        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista) return;
        const item = lista.buscarItem(itemId);
        if (!item) return;

        this.itemEditarId = item.id;
        document.getElementById('edit-item-name').value = item.nome;
        document.getElementById('edit-item-qty').value = item.quantidade || '1';
        document.getElementById('edit-item-price').value = item.preco || '0,00';
        this.limparErroEdicaoItem();
        document.getElementById('edit-item-modal').classList.add('active');
        setTimeout(() => document.getElementById('edit-item-name')?.focus(), 150);
      }

      fecharModalEditarItem() {
        this.itemEditarId = null;
        this.limparErroEdicaoItem();
        document.getElementById('edit-item-modal')?.classList.remove('active');
      }

      salvarEdicaoItem() {
        const inpNome = document.getElementById('edit-item-name');
        const inpQtd = document.getElementById('edit-item-qty');
        const inpPreco = document.getElementById('edit-item-price');

        const nome = (inpNome.value || '').trim();
        const qtd = (inpQtd.value || '').trim() || '1';
        const preco = (inpPreco.value || '').trim() || '0,00';

        if (!nome) {
          inpNome.classList.add('input-error');
          document.getElementById('edit-item-name-error')?.classList.add('visible');
          inpNome.focus();
          this.toast('Digite o nome do produto!');
          return;
        }

        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista || this.itemEditarId === null) return;

        const atualizado = lista.editarItem(this.itemEditarId, nome, qtd, preco);
        if (!atualizado) {
          this.fecharModalEditarItem();
          return;
        }

        this.storage.salvarListas();
        this.fecharModalEditarItem();

        if (this.viewAtual === 'view-shopping') {
          this.renderizarModoMercado();
        } else {
          this.renderizarItensLista();
        }
        this.toast(`✓ "${nome}" atualizado!`);
      }

      adicionarItem() {
        const inpNome = document.getElementById('item-name-input');
        const inpQtd = document.getElementById('item-qty-input');
        const inpPreco = document.getElementById('item-price-input');

        const nome = (inpNome.value || '').trim();
        const qtd = (inpQtd.value || '').trim() || '1';
        const preco = (inpPreco.value || '').trim() || '0,00';

        if (!nome) {
          inpNome.classList.add('input-error');
          document.getElementById('item-name-error').classList.add('visible');
          inpNome.focus();
          this.toast('Digite o nome do produto!');
          return;
        }

        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista) return;

        lista.adicionarItem(nome, qtd, preco, false);
        this.storage.salvarListas();

        inpNome.value = '';
        inpQtd.value = '1';
        inpPreco.value = '0,00';
        this.limparErroItem();
        this.renderizarItensLista();
        this.toast(`✓ "${nome}" adicionado!`);
      }

      alternarItemComprado(itemId) {
        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista) return;
        const item = lista.buscarItem(itemId);
        if (item) {
          item.alternarComprado();
          this.storage.salvarListas();
          this.renderizarItensLista();
        }
      }

      removerItem(itemId) {
        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista) return;
        lista.removerItem(itemId);
        this.storage.salvarListas();
        this.renderizarItensLista();
        this.toast('Item removido.');
      }

      iniciarCompras() {
        if (this.listaAtualId) this.abrirModoMercado(this.listaAtualId);
      }

      abrirModoMercado(listaId, opcoes = {}) {
        const lista = this.storage.buscarLista(listaId);
        if (!lista) {
          this.mostrarView('view-lists', { historyMode: 'replace' });
          return;
        }
        this.listaAtualId = lista.id;
        this.carrinhoIds.clear();
        document.getElementById('shop-list-title').textContent = lista.titulo;
        this.renderizarModoMercado();
        this.mostrarView('view-shopping', {
          historyMode: opcoes.historyMode || 'push',
          extras: { listaAtualId: lista.id }
        });
      }

      renderizarModoMercado() {
        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista) return;
        const itens = lista.itens;
        const prateleira = itens.filter(it => !this.carrinhoIds.has(String(it.id)));
        const carrinho = itens.filter(it => this.carrinhoIds.has(String(it.id)));

        document.getElementById('shelf-count-badge').textContent = prateleira.length;
        document.getElementById('cart-count-badge').textContent = carrinho.length;

        const shelfContainer = document.getElementById('shop-shelf-container');
        if (!itens.length) {
          shelfContainer.innerHTML = '<p style="color: var(--text-muted); padding: 12px 0;">Nenhum produto nesta lista. Adicione usando "+ Item rápido".</p>';
        } else if (!prateleira.length) {
          shelfContainer.innerHTML = '<p style="color: var(--text-muted); padding: 12px 0;">Todos os produtos estão no carrinho!</p>';
        } else {
          shelfContainer.innerHTML = prateleira.map(it => `
            <div class="shopping-item-card">
              <div class="item-info">
                <div class="item-title">${this.escaparHtml(it.nome)}</div>
                <div class="item-subtext">Qtd: ${this.escaparHtml(it.quantidade)} · R$ ${this.escaparHtml(it.preco)}</div>
              </div>
              <div style="display: flex; align-items: center; gap: 6px; flex-shrink: 0;">
                <button type="button" class="btn btn-secondary btn-small" aria-label="Editar item" onclick="app.abrirEditarItem('${it.id}')">✏️</button>
                <button type="button" class="btn btn-primary btn-small" onclick="app.moverParaCarrinho('${it.id}')">+ Carrinho</button>
              </div>
            </div>
          `).join('');
        }

        const cartContainer = document.getElementById('shop-cart-container');
        let somaTotal = 0;
        if (!carrinho.length) {
          cartContainer.innerHTML = '<p style="color: var(--text-muted); padding: 12px 0;">Nenhum produto no carrinho ainda.</p>';
        } else {
          cartContainer.innerHTML = carrinho.map(it => {
            const sub = it.calcularSubtotal();
            somaTotal += sub;
            return `
              <div class="shopping-item-card is-bought">
                <div class="item-info">
                  <div class="item-title">${this.escaparHtml(it.nome)}</div>
                  <div class="item-subtext">Qtd: ${this.escaparHtml(it.quantidade)} · Subtotal: ${this.formatarMoeda(sub)}</div>
                </div>
                <div style="display: flex; align-items: center; gap: 6px; flex-shrink: 0;">
                  <button type="button" class="btn btn-secondary btn-small" aria-label="Editar item" onclick="app.abrirEditarItem('${it.id}')">✏️</button>
                  <button type="button" class="btn btn-secondary btn-small" onclick="app.tirarDoCarrinho('${it.id}')">Tirar</button>
                </div>
              </div>
            `;
          }).join('');
        }

        document.getElementById('shop-cart-total').textContent = this.formatarMoeda(somaTotal);
      }

      moverParaCarrinho(itemId) {
        this.carrinhoIds.add(String(itemId));
        this.renderizarModoMercado();
      }

      tirarDoCarrinho(itemId) {
        this.carrinhoIds.delete(String(itemId));
        this.renderizarModoMercado();
      }

      moverTudoCarrinho() {
        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista) return;
        lista.itens.forEach(it => this.carrinhoIds.add(String(it.id)));
        this.renderizarModoMercado();
        this.toast('Todos os itens movidos para o carrinho!');
      }

      abrirModalItemRapido() {
        document.getElementById('quick-item-name').value = '';
        document.getElementById('quick-item-qty').value = '1';
        document.getElementById('quick-item-price').value = '0,00';
        document.getElementById('quick-add-modal').classList.add('active');
        setTimeout(() => document.getElementById('quick-item-name')?.focus(), 150);
      }

      fecharModalItemRapido() {
        document.getElementById('quick-add-modal').classList.remove('active');
      }

      executarAdicaoRapida() {
        const nome = (document.getElementById('quick-item-name').value || '').trim();
        const qtd = (document.getElementById('quick-item-qty').value || '').trim() || '1';
        const preco = (document.getElementById('quick-item-price').value || '').trim() || '0,00';

        if (!nome) {
          this.toast('Digite o nome do produto!');
          return;
        }
        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista) return;

        const novoItem = lista.adicionarItem(nome, qtd, preco, true);
        this.storage.salvarListas();
        this.carrinhoIds.add(String(novoItem.id));
        this.fecharModalItemRapido();
        this.renderizarModoMercado();
        this.toast(`✓ "${nome}" no carrinho!`);
      }

      abrirModalFinalizar() {
        const total = document.getElementById('shop-cart-total').textContent;
        document.getElementById('finish-modal-msg').textContent = `Deseja finalizar a compra (${total}) e salvar na memória do aparelho?`;
        document.getElementById('finish-modal').classList.add('active');
      }

      fecharModalFinalizar() {
        document.getElementById('finish-modal').classList.remove('active');
      }

      executarFinalizacao() {
        this.fecharModalFinalizar();
        const lista = this.storage.buscarLista(this.listaAtualId);
        if (!lista) return;

        const itensNoCarrinho = lista.itens.filter(it => this.carrinhoIds.has(String(it.id)));
        const total = document.getElementById('shop-cart-total').textContent;

        this.storage.registrarCompraFinalizada(lista, itensNoCarrinho, total);
        this.toast('✓ Compra finalizada e salva!');
        this.mostrarView('view-history');
      }

      renderizarHistorico() {
        const compras = this.storage.historico;
        const container = document.getElementById('history-container');

        if (!compras.length) {
          container.innerHTML = `
            <div class="empty-state">
              <p>Nenhuma compra salva no histórico ainda.</p>
              <button type="button" class="btn btn-primary" onclick="app.mostrarView('view-lists')">Ir para Minhas Listas</button>
            </div>
          `;
          return;
        }

        container.innerHTML = compras.map((c, idx) => {
          let dataStr = '';
          try { dataStr = new Date(c.dataCompra).toLocaleDateString('pt-BR'); } catch (e) { dataStr = 'Hoje'; }
          return `
            <article class="panel">
              <div class="panel-header">
                <div>
                  <span class="eyebrow">${idx === 0 ? 'Última Compra' : 'Compra Anterior'}</span>
                  <h2>${this.escaparHtml(c.titulo)}</h2>
                </div>
                <span class="badge-pill">${dataStr}</span>
              </div>
              <div style="background: #F8F8F8; border: 1.5px solid #000000; border-radius: 10px; padding: 12px 16px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase;">Total Gasto</span>
                <strong style="font-size: 1.4rem; font-family: var(--font-mono); font-weight: 800;">${this.escaparHtml(c.totalCompra)}</strong>
              </div>
              <div>
                <p style="font-weight: 700; font-size: 0.9rem; margin-bottom: 8px;">Itens Adquiridos (${c.itens.length}):</p>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                  ${c.itens.map(it => `
                    <div style="display: flex; justify-content: space-between; font-size: 0.88rem; padding: 6px 10px; border: 1px solid #E0E0E0; border-radius: 6px; background: #FFFFFF;">
                      <span>${this.escaparHtml(it.nome)} (x${this.escaparHtml(it.quantidade)})</span>
                      <span style="font-weight: 700; font-family: var(--font-mono);">R$ ${this.escaparHtml(it.preco)}</span>
                    </div>
                  `).join('')}
                </div>
              </div>
            </article>
          `;
        }).join('');
      }

      // =======================================================================
      // IMPORTAÇÃO / EXPORTAÇÃO VIA BLUETOOTH E ARQUIVOS (ANDROID & iOS)
      // =======================================================================
      abrirModalTransferencia(modo = 'import', listaId = null) {
        this.transferListaId = listaId !== undefined && listaId !== null ? listaId : null;
        this._popularSelectTransferencia();
        this._mostrarStatusTransferencia('');
        const pasteEl = document.getElementById('transfer-json-paste');
        if (pasteEl) pasteEl.value = '';
        this.alternarModoTransferencia(modo === 'export' ? 'export' : 'import');

        const descExp = document.getElementById('transfer-export-desc');
        if (descExp) {
          descExp.innerHTML = IS_IOS_PLATFORM
            ? 'Gera um arquivo <code>.numesquece.json</code> e abre o menu do iOS (<strong>AirDrop / Bluetooth / Arquivos</strong>) para transferir entre celulares.'
            : 'Gera um arquivo <code>.numesquece.json</code>, pede permissão Bluetooth se necessário e abre o envio por <strong>Bluetooth / Compartilhar</strong> do Android.';
        }
        const descImp = document.getElementById('transfer-import-desc');
        if (descImp) {
          descImp.innerHTML = IS_IOS_PLATFORM
            ? 'Peça permissão ao iPhone/iPad para procurar o arquivo recebido em <strong>Arquivos / Downloads / iCloud</strong> e carregar a lista para usar e editar.'
            : 'O app solicitará acesso aos arquivos do celular para você escolher o arquivo recebido via <strong>Bluetooth / Downloads</strong> e carregar a lista para usar e editar.';
        }
        document.getElementById('transfer-modal')?.classList.add('active');
      }

      fecharModalTransferencia() {
        document.getElementById('transfer-modal')?.classList.remove('active');
      }

      alternarModoTransferencia(modo) {
        this.transferModo = modo === 'export' ? 'export' : 'import';
        const paneExp = document.getElementById('transfer-pane-export');
        const paneImp = document.getElementById('transfer-pane-import');
        const tabExp = document.getElementById('tab-transfer-export');
        const tabImp = document.getElementById('tab-transfer-import');
        if (paneExp) paneExp.style.display = this.transferModo === 'export' ? 'block' : 'none';
        if (paneImp) paneImp.style.display = this.transferModo === 'import' ? 'block' : 'none';
        if (tabExp && tabImp) {
          if (this.transferModo === 'export') {
            tabExp.className = 'btn btn-primary btn-small';
            tabImp.className = 'btn btn-secondary btn-small';
          } else {
            tabExp.className = 'btn btn-secondary btn-small';
            tabImp.className = 'btn btn-primary btn-small';
          }
        }
        this.atualizarResumoExportacao();
      }

      _popularSelectTransferencia() {
        const sel = document.getElementById('transfer-scope-select');
        if (!sel) return;
        const listas = this.storage.obterListas();
        const opts = ['<option value="all">Todas as minhas listas (' + listas.length + ')</option>'];
        listas.forEach(l => {
          opts.push(`<option value="${this.escaparHtml(String(l.id))}">${this.escaparHtml(l.titulo)} (${l.itens.length} itens)</option>`);
        });
        sel.innerHTML = opts.join('');
        if (this.transferListaId !== null && this.storage.buscarLista(this.transferListaId)) {
          sel.value = String(this.transferListaId);
        } else {
          sel.value = 'all';
        }
      }

      _obterEscopoExportacaoSelecionado() {
        const sel = document.getElementById('transfer-scope-select');
        const val = sel ? sel.value : 'all';
        return val === 'all' ? null : val;
      }

      _gerarNomeArquivoExportacao(listaId = null) {
        if (listaId && String(listaId) !== 'all') {
          const lista = this.storage.buscarLista(listaId);
          if (lista && lista.titulo) {
            const slug = lista.titulo
              .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
              .toLowerCase()
              .replace(/[^a-z0-9]+/g, '_')
              .replace(/^_+|_+$/g, '')
              .slice(0, 32) || 'lista';
            return `${slug}.numesquece.json`;
          }
        }
        return 'todas_listas.numesquece.json';
      }

      atualizarResumoExportacao() {
        const escopo = this._obterEscopoExportacaoSelecionado();
        const preview = document.getElementById('transfer-filename-preview');
        if (preview) {
          preview.textContent = this._gerarNomeArquivoExportacao(escopo);
        }
      }

      _mostrarStatusTransferencia(msg) {
        const box = document.getElementById('transfer-status-box');
        if (!box) return;
        if (!msg) {
          box.style.display = 'none';
          box.textContent = '';
          return;
        }
        box.textContent = msg;
        box.style.display = 'block';
      }

      _decodificarBase64Utf8(b64) {
        const limpo = String(b64 || '').replace(/\s+/g, '');
        if (!limpo) return '';
        let bin = '';
        if (typeof atob === 'function') {
          bin = atob(limpo);
        } else if (typeof Buffer !== 'undefined') {
          return Buffer.from(limpo, 'base64').toString('utf-8');
        }
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) {
          bytes[i] = bin.charCodeAt(i);
        }
        if (typeof TextDecoder !== 'undefined') {
          return new TextDecoder('utf-8').decode(bytes);
        }
        let pct = '';
        for (let i = 0; i < bytes.length; i++) {
          pct += '%' + bytes[i].toString(16).padStart(2, '0');
        }
        return decodeURIComponent(pct);
      }

      executarExportacaoBluetooth(listaIdOverride = undefined) {
        if (!this.storage.obterListas().length) {
          this._mostrarStatusTransferencia('❌ Crie ao menos uma lista antes de exportar.');
          this.toast('Nenhuma lista para exportar.');
          return false;
        }
        const escopo = listaIdOverride !== undefined ? listaIdOverride : this._obterEscopoExportacaoSelecionado();
        const jsonStr = this.storage.exportarPacoteJSON(escopo, IS_IOS_PLATFORM ? 'iOS' : 'Android');
        const fileName = this._gerarNomeArquivoExportacao(escopo);

        if (typeof window !== 'undefined' && window.AndroidBridge && typeof window.AndroidBridge.exportarViaBluetoothECompartilhar === 'function') {
          window.AndroidBridge.exportarViaBluetoothECompartilhar(jsonStr, fileName, true);
          this._mostrarStatusTransferencia('📡 Seletor Bluetooth / Compartilhar do Android aberto!');
          return true;
        }

        if (typeof window !== 'undefined' && window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.iosShare) {
          window.webkit.messageHandlers.iosShare.postMessage({ json: jsonStr, fileName });
          this._mostrarStatusTransferencia('📡 Compartilhamento iOS (AirDrop / Bluetooth / Arquivos) aberto!');
          return true;
        }

        if (typeof navigator !== 'undefined' && typeof navigator.share === 'function') {
          try {
            if (typeof File === 'function') {
              const file = new File([jsonStr], fileName, { type: 'application/json' });
              if (!navigator.canShare || navigator.canShare({ files: [file] })) {
                navigator.share({
                  title: 'NumEsquece Lista - Transferência',
                  text: 'Lista de compras exportada pelo NumEsquece Lista',
                  files: [file]
                }).catch(() => {});
                this._mostrarStatusTransferencia('📡 Escolha AirDrop, Bluetooth ou Arquivos no menu!');
                return true;
              }
            }
            navigator.share({
              title: 'NumEsquece Lista - ' + fileName,
              text: jsonStr
            }).catch(() => {});
            this._mostrarStatusTransferencia('📡 Compartilhamento aberto!');
            return true;
          } catch (e) {}
        }

        return this.baixarJsonLista(escopo);
      }

      baixarJsonLista(listaIdOverride = undefined) {
        if (!this.storage.obterListas().length) {
          this.toast('Nenhuma lista para salvar.');
          return false;
        }
        const escopo = listaIdOverride !== undefined ? listaIdOverride : this._obterEscopoExportacaoSelecionado();
        const jsonStr = this.storage.exportarPacoteJSON(escopo, IS_IOS_PLATFORM ? 'iOS' : 'Android');
        const fileName = this._gerarNomeArquivoExportacao(escopo);

        if (typeof window !== 'undefined' && window.AndroidBridge && typeof window.AndroidBridge.exportarViaBluetoothECompartilhar === 'function') {
          window.AndroidBridge.exportarViaBluetoothECompartilhar(jsonStr, fileName, false);
          this._mostrarStatusTransferencia('💾 Escolha "Salvar nos Arquivos" ou outro app para guardar o arquivo.');
          return true;
        }

        if (typeof window !== 'undefined' && window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.iosShare) {
          window.webkit.messageHandlers.iosShare.postMessage({ json: jsonStr, fileName });
          this._mostrarStatusTransferencia('💾 Toque em "Salvar em Arquivos" para guardar a lista no iPhone.');
          return true;
        }

        if (typeof Blob === 'function' && typeof URL !== 'undefined' && typeof URL.createObjectURL === 'function') {
          const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = fileName;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          setTimeout(() => URL.revokeObjectURL(url), 1000);
          this._mostrarStatusTransferencia(`✓ Arquivo "${fileName}" gerado!`);
          this.toast('✓ Arquivo salvo!');
          return true;
        }
        return false;
      }

      copiarJsonTransferencia() {
        const escopo = this._obterEscopoExportacaoSelecionado();
        const jsonStr = this.storage.exportarPacoteJSON(escopo, IS_IOS_PLATFORM ? 'iOS' : 'Android');
        const pasteEl = document.getElementById('transfer-json-paste');
        if (pasteEl) pasteEl.value = jsonStr;
        if (typeof navigator !== 'undefined' && navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
          navigator.clipboard.writeText(jsonStr).then(() => {
            this._mostrarStatusTransferencia('✓ Código JSON copiado!');
            this.toast('✓ JSON copiado!');
          }).catch(() => {
            this._mostrarStatusTransferencia('Código exibido abaixo na aba Importar.');
          });
          return true;
        }
        this._mostrarStatusTransferencia('Código JSON gerado.');
        return true;
      }

      solicitarImportacaoArquivo() {
        if (typeof window !== 'undefined' && window.AndroidBridge && typeof window.AndroidBridge.solicitarImportacaoArquivo === 'function') {
          this._mostrarStatusTransferencia('📂 Abrindo seletor de arquivos / pastas Bluetooth do Android...');
          window.AndroidBridge.solicitarImportacaoArquivo();
          return true;
        }
        if (typeof window !== 'undefined' && window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.iosImportFile) {
          this._mostrarStatusTransferencia('📂 Abrindo app Arquivos do iOS...');
          window.webkit.messageHandlers.iosImportFile.postMessage({});
          return true;
        }
        const inp = document.getElementById('transfer-file-input');
        if (inp) {
          inp.click();
          return true;
        }
        this.toast('Use o campo de colar JSON abaixo.');
        return false;
      }

      importarTextoColado() {
        const pasteEl = document.getElementById('transfer-json-paste');
        const txt = pasteEl ? pasteEl.value : '';
        return this.receberArquivoImportado(txt, 'codigo_colado.json');
      }

      receberArquivoImportadoBase64(b64, nomeArquivo = 'recebido.json') {
        try {
          const texto = this._decodificarBase64Utf8(b64);
          return this.receberArquivoImportado(texto, nomeArquivo);
        } catch (e) {
          const msg = e && e.message ? e.message : 'Erro ao decodificar arquivo.';
          this._mostrarStatusTransferencia(`❌ ${msg}`);
          this.toast('Erro ao ler arquivo importado.');
          return null;
        }
      }

      receberArquivoImportado(conteudoTexto, nomeArquivo = 'recebido.json') {
        try {
          const res = this.storage.importarPacoteJSON(conteudoTexto);
          const primeira = res.listas[0];
          const resumo = res.totalImportadas === 1
            ? `✓ Lista "${primeira.titulo}" (${primeira.itens.length} itens) importada de ${nomeArquivo}!`
            : `✓ ${res.totalImportadas} listas importadas de ${nomeArquivo}!`;
          this._mostrarStatusTransferencia(resumo);
          this.toast(resumo);
          this.renderizarListas();
          if (res.totalImportadas === 1 && primeira) {
            this.fecharModalTransferencia();
            this.abrirDetalhesLista(primeira.id);
          } else {
            this.fecharModalTransferencia();
            this.mostrarView('view-lists');
          }
          return res;
        } catch (e) {
          const msg = e && e.message ? e.message : 'Arquivo inválido.';
          this._mostrarStatusTransferencia(`❌ ${msg}`);
          this.toast('Arquivo inválido ou incompatível.');
          return null;
        }
      }

      atualizarStatusTransferenciaNativa(ok, mensagem) {
        this._mostrarStatusTransferencia((ok ? '✓ ' : 'ℹ️ ') + String(mensagem || ''));
        if (mensagem) this.toast(String(mensagem));
      }
    }

    var app = new AplicativoNumEsquece();
    window.app = app;
    document.addEventListener('DOMContentLoaded', () => app.iniciar());
  </script>
</body>
</html>'''

    return (
        html.replace("__BG_IMAGE_URI__", bg_data_uri)
        .replace("__EXTRA_HEAD__", extra_head)
        .replace("__IS_IOS__", "true" if eh_ios else "false")
        .replace("__IS_PWA__", "true" if (eh_ios and modo_pwa) else "false")
    )
