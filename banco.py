from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from models import TabelaNome

# Conexão com o banco de dados aula_teste no MySQL / phpMyAdmin
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/bank_kaique"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def salvar_contato(nome, telefone):
    session = Session()
    try:
        novo_registro = TabelaNome(nome=nome, telefone=telefone)
        session.add(novo_registro)
        session.commit()
    finally:
        session.close()

def salvar_telefone(telefone):
    session = Session()
    try:
        novo_registro = TabelaNome(telefone=telefone)
        session.add(novo_registro)
        session.commit()
    finally:
        session.close()

def listar_nomes(pesquisa=""):
    session = Session()
    try:
        if pesquisa:
            termo = f"%{pesquisa}%"
            return session.query(TabelaNome).filter(
                or_(
                    TabelaNome.nome.like(termo),
                    TabelaNome.telefone.like(termo)
                )
            ).all()
        return session.query(TabelaNome).all()
    finally:
        session.close()

def excluir_nome(id_registro):
    session = Session()
    try:
        registro = session.query(TabelaNome).filter_by(id=id_registro).first()
        if registro:
            session.delete(registro)
            session.commit()
            return True
        return False
    finally:
        session.close()