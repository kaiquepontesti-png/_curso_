from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms.shopping_forms import ShoppingItemForm, ShoppingListForm
from app.models.num_esquece import NumEsquece
from app.models.shopping import ShoppingItem, ShoppingList

shopping_bp = Blueprint("shopping", __name__, template_folder="../templates")


def sync_shopping_list_to_library(shopping_list: ShoppingList):
    library_record = NumEsquece.query.filter_by(shopping_list_id=shopping_list.id).first()
    if library_record is None:
        library_record = NumEsquece(
            titulo=shopping_list.titulo,
            descricao=shopping_list.descricao or "Lista de compras salva na biblioteca.",
            categoria="compras",
            status="pendente",
            shopping_list_id=shopping_list.id,
        )
        db.session.add(library_record)
        return library_record

    library_record.titulo = shopping_list.titulo
    library_record.descricao = shopping_list.descricao or "Lista de compras salva na biblioteca."
    library_record.categoria = "compras"
    library_record.status = "pendente" if not shopping_list.items else "em_andamento" if any(item.comprado for item in shopping_list.items) else "pendente"
    return library_record


@shopping_bp.route("/listas")
@login_required
def list_lists():
    lists = (
        ShoppingList.query.filter_by(user_id=current_user.id)
        .order_by(ShoppingList.updated_at.desc())
        .all()
    )
    return render_template("shopping/list_lists.html", lists=lists)


@shopping_bp.route("/listas/iniciar")
@login_required
def start_shopping():
    lists = (
        ShoppingList.query.filter_by(user_id=current_user.id)
        .order_by(ShoppingList.updated_at.desc())
        .all()
    )

    if len(lists) > 1:
        return render_template("shopping/start_shopping.html", lists=lists)

    return render_template("shopping/start_blank.html")


@shopping_bp.route("/listas/nova", methods=["GET", "POST"])
@login_required
def create_list():
    form = ShoppingListForm()
    if form.validate_on_submit():
        record = ShoppingList(
            titulo=form.titulo.data.strip(),
            descricao=form.descricao.data.strip() if form.descricao.data else None,
            user_id=current_user.id,
        )
        db.session.add(record)
        db.session.flush()
        sync_shopping_list_to_library(record)
        db.session.commit()
        flash("Lista criada com sucesso!", "success")
        return redirect(url_for("shopping.detail_list", list_id=record.id))
    return render_template("shopping/form_list.html", form=form, title="Nova lista")


@shopping_bp.route("/listas/<int:list_id>/iniciar-selecionada", methods=["GET", "POST"])
@login_required
def start_selected_list(list_id: int):
    shopping_list = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        item_id = request.form.get("item_id", type=int)
        nome = (request.form.get("nome") or "").strip()

        if item_id is not None:
            item = ShoppingItem.query.join(ShoppingList).filter(
                ShoppingItem.id == item_id,
                ShoppingList.id == list_id,
                ShoppingList.user_id == current_user.id,
            ).first_or_404()

            quantidade = (request.form.get("quantidade") or "1").strip()
            if quantidade.isdigit():
                quantidade = str(int(quantidade))

            preco = (request.form.get("preco") or "0,00").strip()
            if not preco:
                preco = "0,00"

            item.quantidade = quantidade
            item.preco = preco
            if item.nome != nome and nome:
                item.nome = nome
            sync_shopping_list_to_library(shopping_list)
            db.session.commit()
            return render_template("shopping/selected_blank.html", shopping_list=shopping_list)

        if nome:
            quantidade = (request.form.get("quantidade") or "1").strip()
            if quantidade.isdigit():
                quantidade = str(int(quantidade))

            preco = (request.form.get("preco") or "0,00").strip()
            if not preco:
                preco = "0,00"

            item = ShoppingItem(
                shopping_list_id=shopping_list.id,
                nome=nome,
                quantidade=quantidade,
                categoria=(request.form.get("categoria") or "geral").strip() or "geral",
                preco=preco,
                comprado=False,
            )
            db.session.add(item)
            sync_shopping_list_to_library(shopping_list)
            db.session.commit()
            return render_template("shopping/selected_blank.html", shopping_list=shopping_list)

    return render_template("shopping/selected_blank.html", shopping_list=shopping_list)


@shopping_bp.route("/listas/<int:list_id>", methods=["GET", "POST"])
@login_required
def detail_list(list_id: int):
    shopping_list = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    form = ShoppingItemForm()

    if form.validate_on_submit():
        quantidade = form.quantidade.data.strip() or "1"
        if quantidade.isdigit():
            quantidade = str(int(quantidade))

        preco = form.preco.data.strip() if form.preco.data else "0,00"
        if form.preco_indefinido.data:
            preco = "0,00"

        item = ShoppingItem(
            shopping_list_id=shopping_list.id,
            nome=form.nome.data.strip(),
            quantidade=quantidade,
            categoria=form.categoria.data.strip() or "geral",
            preco=preco,
            comprado=False,
        )
        db.session.add(item)
        sync_shopping_list_to_library(shopping_list)
        db.session.commit()
        flash("Item adicionado com sucesso!", "success")
        return redirect(url_for("shopping.detail_list", list_id=shopping_list.id))

    return render_template("shopping/detail_list.html", shopping_list=shopping_list, form=form)


@shopping_bp.route("/listas/<int:list_id>/editar", methods=["GET", "POST"])
@login_required
def edit_list(list_id: int):
    shopping_list = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    form = ShoppingListForm(obj=shopping_list)
    if form.validate_on_submit():
        shopping_list.titulo = form.titulo.data.strip()
        shopping_list.descricao = form.descricao.data.strip() if form.descricao.data else None
        sync_shopping_list_to_library(shopping_list)
        db.session.commit()
        flash("Lista atualizada com sucesso!", "success")
        return redirect(url_for("shopping.detail_list", list_id=shopping_list.id))
    return render_template("shopping/form_list.html", form=form, title="Editar lista")


@shopping_bp.route("/listas/<int:list_id>/duplicar", methods=["POST"])
@login_required
def duplicate_list(list_id: int):
    shopping_list = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    new_list = ShoppingList(
        titulo=f"{shopping_list.titulo} (cópia)",
        descricao=shopping_list.descricao,
        user_id=current_user.id,
    )
    db.session.add(new_list)
    db.session.flush()

    for item in shopping_list.items:
        db.session.add(
            ShoppingItem(
                shopping_list_id=new_list.id,
                nome=item.nome,
                quantidade=item.quantidade,
                categoria=item.categoria,
                preco=item.preco,
                comprado=item.comprado,
            )
        )

    sync_shopping_list_to_library(new_list)
    db.session.commit()
    flash("Lista duplicada com sucesso!", "success")
    return redirect(url_for("shopping.list_lists"))


@shopping_bp.route("/listas/<int:list_id>/excluir", methods=["POST"])
@login_required
def delete_list(list_id: int):
    shopping_list = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    library_record = NumEsquece.query.filter_by(shopping_list_id=shopping_list.id).first()
    if library_record is not None:
        db.session.delete(library_record)
    db.session.delete(shopping_list)
    db.session.commit()
    flash("Lista removida com sucesso!", "success")
    return redirect(url_for("shopping.list_lists"))


@shopping_bp.route("/listas/<int:list_id>/itens/<int:item_id>/editar", methods=["GET", "POST"])
@login_required
def edit_item(list_id: int, item_id: int):
    item = ShoppingItem.query.join(ShoppingList).filter(
        ShoppingItem.id == item_id,
        ShoppingList.id == list_id,
        ShoppingList.user_id == current_user.id,
    ).first_or_404()

    form = ShoppingItemForm(obj=item)
    form.preco_indefinido.data = item.preco == "0,00"

    if form.validate_on_submit():
        quantidade = form.quantidade.data.strip() or "1"
        if quantidade.isdigit():
            quantidade = str(int(quantidade))

        preco = form.preco.data.strip() if form.preco.data else "0,00"
        if form.preco_indefinido.data:
            preco = "0,00"

        item.nome = form.nome.data.strip()
        item.quantidade = quantidade
        item.categoria = form.categoria.data.strip() or "geral"
        item.preco = preco
        sync_shopping_list_to_library(item.shopping_list)
        db.session.commit()
        flash("Item atualizado com sucesso!", "success")
        return redirect(url_for("shopping.detail_list", list_id=list_id))

    return render_template("shopping/edit_item.html", form=form, shopping_list=item.shopping_list, item=item)


@shopping_bp.route("/listas/<int:list_id>/itens/<int:item_id>/toggle", methods=["POST"])
@login_required
def toggle_item(list_id: int, item_id: int):
    item = ShoppingItem.query.join(ShoppingList).filter(
        ShoppingItem.id == item_id,
        ShoppingList.id == list_id,
        ShoppingList.user_id == current_user.id,
    ).first_or_404()
    item.comprado = not item.comprado
    sync_shopping_list_to_library(item.shopping_list)
    db.session.commit()
    flash("Status do item atualizado!", "success")
    return redirect(url_for("shopping.detail_list", list_id=list_id))


@shopping_bp.route("/listas/<int:list_id>/itens/<int:item_id>/excluir", methods=["POST"])
@login_required
def delete_item(list_id: int, item_id: int):
    item = ShoppingItem.query.join(ShoppingList).filter(
        ShoppingItem.id == item_id,
        ShoppingList.id == list_id,
        ShoppingList.user_id == current_user.id,
    ).first_or_404()
    db.session.delete(item)
    sync_shopping_list_to_library(item.shopping_list)
    db.session.commit()
    flash("Item removido com sucesso!", "success")
    return redirect(url_for("shopping.detail_list", list_id=list_id))
