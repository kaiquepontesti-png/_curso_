import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.extensions import db
from app.forms.auth_forms import LoginForm, RegisterForm
from app.models.shopping import User

auth_bp = Blueprint("auth", __name__, template_folder="../templates")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        cpf = re.sub(r"\D", "", form.cpf.data or "")

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Este e-mail já está cadastrado.", "warning")
            return render_template("auth/register.html", form=form)

        existing_cpf = User.query.filter_by(cpf=cpf).first()
        if existing_cpf:
            flash("Este CPF já está cadastrado.", "warning")
            return render_template("auth/register.html", form=form)

        user = User(
            nome=form.nome.data.strip(),
            email=email,
            cpf=cpf,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("shopping.list_lists"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(request.args.get("next") or url_for("shopping.list_lists"))

        flash("E-mail ou senha inválidos.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))
