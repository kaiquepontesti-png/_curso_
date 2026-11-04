import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


def validate_password_strength(form, field):
    password = field.data or ""
    if len(password) < 8:
        raise ValidationError("A senha deve ter no mínimo 8 caracteres.")
    if not any(char.isupper() for char in password):
        raise ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
    if not any(char.islower() for char in password):
        raise ValidationError("A senha deve conter pelo menos uma letra minúscula.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("A senha deve conter pelo menos um número.")
    if not any(not char.isalnum() for char in password):
        raise ValidationError("A senha deve conter pelo menos um caractere especial.")


def validate_cpf(form, field):
    raw_value = re.sub(r"\D", "", field.data or "")
    if len(raw_value) != 11 or not raw_value.isdigit():
        raise ValidationError("CPF inválido. Use o formato 000.000.000-00.")


class RegisterForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(message="Informe seu nome."), Length(min=2, max=120)])
    email = StringField("E-mail", validators=[DataRequired(message="Informe seu e-mail."), Email(message="E-mail inválido.")])
    cpf = StringField(
        "CPF",
        validators=[
            DataRequired(message="Informe seu CPF."),
            Length(min=14, max=14, message="Use o formato 000.000.000-00."),
            validate_cpf,
        ],
    )
    password = PasswordField(
        "Senha",
        validators=[DataRequired(message="Informe uma senha."), validate_password_strength],
    )
    confirm_password = PasswordField(
        "Repetir senha",
        validators=[
            DataRequired(message="Repita a senha."),
            EqualTo("password", message="As senhas não coincidem."),
        ],
    )
    submit = SubmitField("Criar conta")


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(message="Informe seu e-mail."), Email(message="E-mail inválido.")])
    password = PasswordField("Senha", validators=[DataRequired(message="Informe sua senha.")])
    submit = SubmitField("Entrar")
