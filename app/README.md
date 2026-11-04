# NumEsquece

Aplicação web para cadastro, consulta, edição e exclusão de registros do sistema NumEsquece, desenvolvida em Python com Flask e arquitetura modular.

## Tecnologias utilizadas

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-WTF
- Jinja2
- SQLite (configurável via `DATABASE_URL`)
- pytest

## Estrutura de diretórios

```text
app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── forms/
│   │   ├── __init__.py
│   │   └── num_esquece_forms.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── num_esquece.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── num_esquece_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── num_esquece_service.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── num_esquece.css
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   └── num_esquece.js
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── num_esquece/
│           ├── create.html
│           ├── detail.html
│           ├── edit.html
│           └── list.html
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

## Pré-requisitos

- Python 3.11 ou superior
- pip
- Git

## Criação e ativação de ambiente virtual

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalação das dependências

```bash
pip install -r requirements.txt
```

## Configuração das variáveis de ambiente

Crie um arquivo `.env` com base no `.env.example`:

```env
SECRET_KEY=sua-chave-secreta
DATABASE_URL=sqlite:///num_esquece.db
FLASK_ENV=development
```

Para usar MySQL/MariaDB local (como no phpMyAdmin):

```env
SECRET_KEY=sua-chave-secreta
DATABASE_URL=mysql+pymysql://SEU_USUARIO:SUASENHA@localhost:3306/num_esquece
FLASK_ENV=development
```

> O projeto usa SQLite por padrão para facilitar execução local, mas a variável `DATABASE_URL` pode receber outro banco compatível com SQLAlchemy, incluindo MySQL/MariaDB.

## Configuração e inicialização do banco de dados

No diretório do projeto, execute:

```bash
flask --app run.py db init
flask --app run.py db migrate -m "Initial migration"
flask --app run.py db upgrade
```

Se o comando `flask` não estiver disponível, use:

```bash
python -m flask --app run.py db init
python -m flask --app run.py db migrate -m "Initial migration"
python -m flask --app run.py db upgrade
```

## Como iniciar a aplicação

```bash
python run.py
```

A aplicação estará disponível em:

- http://127.0.0.1:5000

## Como executar os testes

```bash
pytest
```

## Funcionalidades

- Cadastro de usuários com autenticação
- Login e logout com sessão segura
- Criação de listas de compras
- Visualização das listas do usuário autenticado
- Edição, exclusão e duplicação de listas
- Adição, remoção e marcação de itens como comprados
- Cadastro de registros do sistema anterior
- Listagem com busca por texto
- Visualização detalhada
- Edição de dados
- Exclusão com confirmação
- Mensagens de feedback via `flash`
- Validação de formulário no backend
- Estrutura modular por blueprints, services e models

## Observações

O modelo principal é a entidade `NumEsquece`, com campos essenciais como título, descrição, categoria, status, data de vencimento e timestamps. Os campos foram mantidos genéricos e adaptáveis para uso prático, sem introduzir regras de negócio fora do escopo definido.
