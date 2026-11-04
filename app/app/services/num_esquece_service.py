from sqlalchemy import or_

from app.extensions import db
from app.models.num_esquece import NumEsquece


def list_num_esquece(search: str | None = None):
    query = NumEsquece.query

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                NumEsquece.titulo.ilike(term),
                NumEsquece.categoria.ilike(term),
                NumEsquece.descricao.ilike(term),
            )
        )

    return query.order_by(NumEsquece.created_at.desc()).all()


def get_num_esquece(record_id: int):
    return db.session.get(NumEsquece, record_id)


def create_num_esquece(data: dict):
    record = NumEsquece(
        titulo=data["titulo"].strip(),
        descricao=data["descricao"].strip(),
        categoria=data["categoria"].strip(),
        status=data["status"],
        data_vencimento=data.get("data_vencimento"),
    )
    db.session.add(record)
    db.session.commit()
    return record


def update_num_esquece(record: NumEsquece, data: dict):
    record.titulo = data["titulo"].strip()
    record.descricao = data["descricao"].strip()
    record.categoria = data["categoria"].strip()
    record.status = data["status"]
    record.data_vencimento = data.get("data_vencimento")
    db.session.commit()
    return record


def delete_num_esquece(record: NumEsquece):
    db.session.delete(record)
    db.session.commit()


def count_num_esquece():
    return NumEsquece.query.count()


def count_by_status():
    counts = {
        "pendente": NumEsquece.query.filter_by(status="pendente").count(),
        "em_andamento": NumEsquece.query.filter_by(status="em_andamento").count(),
        "concluido": NumEsquece.query.filter_by(status="concluido").count(),
    }
    return counts
