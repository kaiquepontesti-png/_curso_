from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms.shopping_forms import ShoppingItemForm, ShoppingListForm
from app.models.shopping import ShoppingItem, ShoppingList

shopping_bp = Blueprint("shopping", __name__, template_folder="../templates")


@shopping_bp.route("/listas")
@login_required
def list_lists():
    lists = (
        ShoppingList.query.filter_by(user_id=current_user.id)
        .order_by(ShoppingList.updated_at.desc())
        .all()
    )
    return render_template("shopping/list_lists.html", lists=lists)


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
        db.session.commit()
        flash("Lista criada com sucesso!", "success")
        return redirect(url_for("shopping.detail_list", list_id=record.id))
    return render_template("shopping/form_list.html", form=form, title="Nova lista")


@shopping_bp.route("/listas/<int:list_id>", methods=["GET", "POST"])
@login_required
def detail_list(list_id: int):
    shopping_list = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    form = ShoppingItemForm()

    if form.validate_on_submit():
        item = ShoppingItem(
            shopping_list_id=shopping_list.id,
            nome=form.nome.data.strip(),
            quantidade=form.quantidade.data.strip() or "1",
            categoria=form.categoria.data.strip() or "geral",
            comprado=bool(form.comprado.data),
        )
        db.session.add(item)
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
                comprado=item.comprado,
            )
        )

    db.session.commit()
    flash("Lista duplicada com sucesso!", "success")
    return redirect(url_for("shopping.list_lists"))


@shopping_bp.route("/listas/<int:list_id>/excluir", methods=["POST"])
@login_required
def delete_list(list_id: int):
    shopping_list = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    db.session.delete(shopping_list)
    db.session.commit()
    flash("Lista removida com sucesso!", "success")
    return redirect(url_for("shopping.list_lists"))


@shopping_bp.route("/listas/<int:list_id>/itens/<int:item_id>/toggle", methods=["POST"])
@login_required
def toggle_item(list_id: int, item_id: int):
    item = ShoppingItem.query.join(ShoppingList).filter(
        ShoppingItem.id == item_id,
        ShoppingList.id == list_id,
        ShoppingList.user_id == current_user.id,
    ).first_or_404()
    item.comprado = not item.comprado
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
    db.session.commit()
    flash("Item removido com sucesso!", "success")
    return redirect(url_for("shopping.detail_list", list_id=list_id))
