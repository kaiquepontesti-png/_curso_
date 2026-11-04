from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.extensions import db
from app.forms.num_esquece_forms import NumEsqueceForm
from app.models.num_esquece import NumEsquece
from app.services.num_esquece_service import (
    count_by_status,
    count_num_esquece,
    create_num_esquece,
    delete_num_esquece,
    get_num_esquece,
    list_num_esquece,
    update_num_esquece,
)

num_esquece_bp = Blueprint("num_esquece", __name__)


@num_esquece_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("shopping.list_lists"))
    return render_template("index.html")


@num_esquece_bp.route("/registros", methods=["GET"])
def list_records():
    search = request.args.get("q", "", type=str)
    records = list_num_esquece(search=search)
    return render_template("num_esquece/list.html", records=records, search=search)


@num_esquece_bp.route("/registros/novo", methods=["GET", "POST"])
def create_record():
    form = NumEsqueceForm()
    if form.validate_on_submit():
        data = {
            "titulo": form.titulo.data,
            "descricao": form.descricao.data,
            "categoria": form.categoria.data,
            "status": form.status.data,
            "data_vencimento": form.data_vencimento.data,
        }
        try:
            record = create_num_esquece(data)
            flash("Registro criado com sucesso!", "success")
            return redirect(url_for("num_esquece.detail_record", record_id=record.id))
        except Exception:
            db.session.rollback()
            flash("Não foi possível criar o registro. Verifique os dados e tente novamente.", "danger")
    return render_template("num_esquece/create.html", form=form)


@num_esquece_bp.route("/registros/<int:record_id>")
def detail_record(record_id: int):
    record = get_num_esquece(record_id)
    if record is None:
        flash("Registro não encontrado.", "warning")
        return redirect(url_for("num_esquece.list_records"))
    return render_template("num_esquece/detail.html", record=record)


@num_esquece_bp.route("/registros/<int:record_id>/editar", methods=["GET", "POST"])
def edit_record(record_id: int):
    record = get_num_esquece(record_id)
    if record is None:
        flash("Registro não encontrado.", "warning")
        return redirect(url_for("num_esquece.list_records"))

    form = NumEsqueceForm(obj=record)
    if form.validate_on_submit():
        data = {
            "titulo": form.titulo.data,
            "descricao": form.descricao.data,
            "categoria": form.categoria.data,
            "status": form.status.data,
            "data_vencimento": form.data_vencimento.data,
        }
        try:
            update_num_esquece(record, data)
            flash("Registro atualizado com sucesso!", "success")
            return redirect(url_for("num_esquece.detail_record", record_id=record.id))
        except Exception:
            db.session.rollback()
            flash("Não foi possível atualizar o registro. Verifique os dados e tente novamente.", "danger")
    return render_template("num_esquece/edit.html", form=form, record=record)


@num_esquece_bp.route("/registros/<int:record_id>/excluir", methods=["POST"])
def delete_record(record_id: int):
    record = get_num_esquece(record_id)
    if record is None:
        flash("Registro não encontrado.", "warning")
        return redirect(url_for("num_esquece.list_records"))

    try:
        delete_num_esquece(record)
        flash("Registro removido com sucesso!", "success")
    except Exception:
        db.session.rollback()
        flash("Não foi possível excluir o registro.", "danger")

    return redirect(url_for("num_esquece.list_records"))
