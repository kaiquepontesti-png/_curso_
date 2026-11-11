# NumEsquece Lista

Aplicação web para criação e controle inteligente de listas de compras no supermercado, cadastro, consulta e histórico de despesas, desenvolvida em Python com Flask e arquitetura modular.

---

## 🎨 Design System: Monocromático Clássico & Minimalista de Alto Contraste

A interface do **NumEsquece Lista** adota a linguagem visual **Monocromático Clássico & Minimalista de Alto Contraste** (estilo Neo-Brutalist limpo / High-Contrast Monochrome), proporcionando máxima legibilidade, foco absoluto nas tarefas e uma estética contemporânea, precisa e elegante:

- **Fundo Ilustrado com Doodles Sutis**: Canvas branco com padrão contínuo de ilustrações manuais de mercado (`url('../images/bg-doodle.jpg')`) e overlay clareador calibrado (`linear-gradient(rgba(255, 255, 255, 0.83), rgba(255, 255, 255, 0.83))`), mantendo as linhas pretas dos doodles com opacidade suave entre **15% e 20%**;
- **Cards e Containers**: Fundo branco sólido (`#FFFFFF`), borda preta sólida de **1.5px a 2px** (`#000000`), cantos levemente arredondados (`rounded-xl` / 14px) e **sombra seca deslocada sem borrão** (`box-shadow: 4px 4px 0px #000000`), destacando os cartões do fundo com precisão arquitetônica;
- **Botões Refinados de Alto Contraste**:
  - *Botão Primário* (`.btn-primary`, `.save-btn`, `.btn-hero-shop`): Fundo preto absoluto (`#000000`), texto branco nítido (`#FFFFFF`), cantos `rounded-lg` (8px), borda preta de 2px e sombra seca `3px 3px 0px #000000`. Efeito tátil de pressão ao clicar (`active: translate(2px, 2px); box-shadow: 1px 1px 0px #000000`);
  - *Botão Secundário / Contorno* (`.btn-secondary`): Fundo branco sólido (`#FFFFFF`), texto preto (`#000000`), borda preta de 2px e sombra seca `3px 3px 0px #000000`, com hover em cinza sutil (`#F5F5F5`);
  - *Botão de Exclusão / Perigo* (`.btn-danger`, `.remove-cart-btn`): Fundo branco com borda preta de 2px, invertendo para fundo preto e texto branco no hover;
  - *Toggle de Item Pego* (`.item-check-toggle`): Caixa de marcação tátil de 44px com borda preta de 2px; ao ser marcado, preenche com fundo preto sólido (`#000000`), ícone `✓` branco nítido e aplica tachado elegante ao produto;
- **Campos de Busca e Formulários (Inputs)**: Fundo branco puro (`#FFFFFF`), contorno preto bem definido de 2px (`#000000`), placeholder em cinza neutro (`#757575`) e foco de alta precisão com sombra seca (`box-shadow: 3px 3px 0px #000000; outline: none`);
- **Tipografia Geométrica e Moderna**: Fonte Sans-serif geométrica **Inter** (Google Fonts), com hierarquia rigorosa: títulos e números em peso 700/800 e corpo de texto em peso 400/500/600.

---

### 1. Paleta Monocromática Oficial (`:root`)

```css
:root {
  /* Canvas e Superfície de Alto Contraste */
  --bg-papel-escuro: #FFFFFF;    /* Canvas base branco puro */
  --bg-superficie: #FFFFFF;      /* Cartões, painéis e sidebar em branco sólido */
  --text-grafite-6b: #000000;    /* Tipografia principal: Preto absoluto (#000000) */
  --text-grafite-2h: #757575;    /* Tipografia secundária / Placeholders: Cinza neutro (#757575) */
  --divisorias-regua: #000000;   /* Linhas de contorno estrutural: Preto absoluto (#000000) */

  /* Cores de Interação Monocromática */
  --caneta-azul-destaque: #000000;
  --caneta-azul-hover: #1A1A1A;
  --etiqueta-laranja: #000000;
  --caneta-verde-sucesso: #000000;
  --marca-texto-amarelo: #000000;
  --caneta-vermelha-urgencia: #000000;

  /* Sombras Secas Deslocadas (Offset Shadows sem blur) */
  --shadow-dry-xs: 2px 2px 0px #000000;
  --shadow-dry-sm: 3px 3px 0px #000000;
  --shadow-dry-md: 4px 4px 0px #000000;
  --shadow-dry-lg: 6px 6px 0px #000000;
}
```

---

### 2. Diretrizes de Layout e Responsividade (Mobile & Desktop)

- **Menu Lateral (Sidebar) inspirada no Gemini / ChatGPT**:
  - **Desktop (telas > 900px)**: A barra lateral permanece ancorada à esquerda com largura de `260px`, exibindo o logotipo da aplicação, atalhos de navegação e botão de recolher. A área de conteúdo principal (*Main Content*) utiliza a largura da tela de forma ampla e equilibrada (`width: min(1360px, calc(100% - 44px))`), evitando vazios excessivos em monitores Full HD e ultrawide.
  - **Otimização de Espaço em Grade (Dashboard & Split Layout)**:
    - *Minhas Listas*: Exibição em grade responsiva (*Cards Grid*) aproveitando a largura disponível em 2 a 3 colunas de cartões brancos com bordas pretas e sombras secas.
    - *Lista de Itens*: Disposição em 2 colunas (*Dual Grid*) em telas médias e grandes, permitindo visualizar mais produtos sem rolagem desnecessária.
    - *Modo Supermercado ("Vamos Comprar")*: Layout dividido (*Split Layout*) com produtos à esquerda e painel fixo (*Sticky Card*) do carrinho com valor total e finalização à direita.
    - *Barra de Adição Rápida*: Em telas médias/grandes, os campos de adicionar produto se alinham em uma barra horizontal compacta, reduzindo o consumo vertical de espaço.
  - **Mobile e Tablets (telas ≤ 900px)**: A sidebar se transforma automaticamente em uma **gaveta retrátil (*off-canvas*)**, acionada por um botão hambúrguer de toque rápido na barra superior (*Topbar*). Ao abrir, desliza suavemente sobre a tela com fundo translúcido escuro, sem distorcer os cartões de itens de compra.
  - **Fechamento Ágil**: Pode ser fechada tocando fora da gaveta (no backdrop), clicando no botão `✕` ou pressionando a tecla `Escape`.

---

### 3. Design de Botões, Cards e Interações Visuais Atraentes

- **Cards e Painéis em Branco Sólido com Contorno Preto e Sombra Seca**:
  - **Identidade Visual**: Fundo `#FFFFFF`, borda sólida de 2px `#000000` e cantos arredondados geométricos (`border-radius: 14px`).
  - **Sombras Secas Deslocadas (*Dry Offset Shadows*)**: Efeito nítido sem desfoque (`box-shadow: 4px 4px 0px #000000`), criando separação perfeita em relação ao fundo ilustrado de doodles.
  - **Micro-interações de Hover**: Ao passar o cursor, os cartões se elevam sutilmente (`transform: translate(-1px, -1px)` e `box-shadow: 5px 5px 0px #000000`).

- **Design de Botões e Feedback Tátil (*Tactile Click*)**:
  - **Área de Toque Confortável (*Touch Targets*)**: Mínimo de **44px a 52px** de altura, facilitando o uso no celular no corredor do mercado.
  - **Feedback Físico ao Clique**: Ao clicar (`:active`), o botão translada para frente (`transform: translate(2px, 2px)`) e a sombra encolhe para `1px 1px 0px #000000`, reproduzindo fielmente a sensação de um interruptor físico tátil.
  - **Pílulas de Categoria e Badges de Status**: Contorno fino de 1.5px preto, sombra seca de 2px e inversão visual para fundo preto com texto branco quando ativos ou concluídos.

---

### 4. Acessibilidade (WAI-ARIA e Navegação por Teclado)

- **Semântica HTML5 Estrita**: Uso de tags semânticas `<header>`, `<nav>`, `<aside>`, `<main>`, `<section>` e `<article>`.
- **Atributos `aria-label` e `aria-expanded`**: Presentes em todos os botões de ícones (abrir/fechar gaveta móvel, toggles de item comprado, botões de exclusão e visualização de senha).
- **Foco por Teclado Visível**: Estilização com contorno nítido no `:focus-visible` na cor `--caneta-azul-hover` (`outline: 2px solid var(--caneta-azul-hover); outline-offset: 3px;`).
- **Prevenção de Zoom Indesejado em Mobile**: Todos os campos de formulário utilizam tamanho de fonte base de `16px`, eliminando o zoom automático indesejado no iOS e navegadores móveis.
- **Respeito à Preferência de Movimento**: Suporte nativo à diretiva `@media (prefers-reduced-motion: reduce)`, desativando transições desnecessárias para usuários com sensibilidade visual.

---

### 5. Validação Robusta de Dados de Entrada (CPF e E-mail)

A aplicação conta com validação em duas camadas (no cliente via JavaScript com feedback imediato e no servidor via Flask-WTF):

- **Validação de CPF (Algoritmo Oficial Módulo 11 da Receita Federal)**:
  - Máscara dinâmica em tempo real no padrão `000.000.000-00`;
  - Rejeição automática de sequências inválidas com todos os dígitos iguais (como `000.000.000-00`, `111.111.111-11`, ..., `999.999.999-99`);
  - Cálculo dos dois dígitos verificadores via módulo 11, impedindo CPFs inventados;
  - Feedback visual imediato no formulário ao digitar ou ao sair do campo (`blur`).

- **Validação de E-mail contra Entradas Fictícias**:
  - Rejeição de valores puramente numéricos (como `00000000000`), sem `@` ou sem domínio;
  - Bloqueio de e-mails fictícios com sequências repetidas (ex: `00000000000@...` ou `00000@00000.com`);
  - Exigência de extensão de domínio válida com TLD alfabético de no mínimo 2 letras (ex: `.com`, `.com.br`, `.net`);
  - Bloqueio de domínios numéricos ou incompletos (ex: `test@test`);
  - Bloqueio de endereços de teste óbvios (`teste@teste.com`, `admin@admin.com`, etc.).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Flask** (Modular com Blueprints e Application Factory)
- **Flask-SQLAlchemy** (ORM)
- **Flask-Migrate** (Alembic)
- **Flask-WTF** (Validação e Proteção CSRF)
- **Jinja2** (Templates semânticos)
- **SQLite** (Configurável via variável `DATABASE_URL`)
- **pytest** (Testes automatizados)

---

## 📂 Estrutura de Diretórios

```text
app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── num_esquece_forms.py
│   │   └── shopping_forms.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── num_esquece.py
│   │   └── shopping.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── num_esquece_routes.py
│   │   └── shopping_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── num_esquece_service.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── num_esquece.css  # Componentes de lista, chips, status e toggles
│   │   │   └── style.css        # Layout base, design system, paleta e topbar/sidebar
│   │   ├── js/
│   │   │   ├── main.js          # Formatação de preços e confirmações
│   │   │   └── num_esquece.js   # Interações de formulário e salvamento
│   │   └── images/
│   └── templates/
│       ├── base.html            # App shell responsivo com drawer off-canvas
│       ├── index.html           # Página inicial institucional dark
│       ├── contato.html
│       ├── duvidas.html
│       ├── sobre.html
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── num_esquece/
│       │   ├── create.html
│       │   ├── detail.html
│       │   ├── edit.html
│       │   └── list.html
│       └── shopping/
│           ├── completed_purchases.html
│           ├── detail_list.html
│           ├── edit_item.html
│           ├── form_list.html
│           ├── list_lists.html
│           ├── selected_blank.html
│           ├── start_blank.html
│           └── start_shopping.html
├── migrations/
├── tests/
│   ├── conftest.py
│   └── test_num_esquece.py
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

## 🚀 Como Iniciar a Aplicação

### 1. Criar e Ativar o Ambiente Virtual

#### Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente
Copie o arquivo `.env.example` para `.env`:
```env
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///num_esquece.db
FLASK_ENV=development
```

### 4. Inicializar o Banco de Dados
```bash
python -m flask --app run.py db upgrade
```

### 5. Executar o Servidor de Desenvolvimento
```bash
python run.py
```
Acesse em seu navegador: **http://127.0.0.1:5000**

---

## 🧪 Como Executar os Testes Automatizados

Com o ambiente virtual ativo, execute:
```bash
pytest
```
Todos os testes cobrem criação de usuários, validação de CPF e senhas, CRUD completo, proteção CSRF e finalização de compras com cálculo de histórico.
