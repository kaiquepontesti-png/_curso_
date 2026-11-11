import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


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


def is_valid_cpf(cpf_str: str) -> bool:
    digits = re.sub(r"\D", "", cpf_str or "")
    if len(digits) != 11 or not digits.isdigit():
        return False
    # Rejeita CPFs com todos os dígitos iguais (ex: 00000000000, 11111111111, etc.)
    if len(set(digits)) == 1:
        return False

    # Primeiro dígito verificador
    soma1 = sum(int(digits[i]) * (10 - i) for i in range(9))
    resto1 = soma1 % 11
    d1 = 0 if resto1 < 2 else 11 - resto1
    if int(digits[9]) != d1:
        return False

    # Segundo dígito verificador
    soma2 = sum(int(digits[i]) * (11 - i) for i in range(10))
    resto2 = soma2 % 11
    d2 = 0 if resto2 < 2 else 11 - resto2
    if int(digits[10]) != d2:
        return False

    return True


def validate_cpf(form, field):
    raw_value = re.sub(r"\D", "", field.data or "")
    if len(raw_value) != 11 or not raw_value.isdigit():
        raise ValidationError("CPF incompleto. Use o formato 000.000.000-00.")

    if len(set(raw_value)) == 1:
        raise ValidationError(
            "CPF inválido. Não são permitidas sequências com todos os dígitos repetidos (como 000.000.000-00)."
        )

    if not is_valid_cpf(raw_value):
        raise ValidationError("CPF inválido. Certifique-se de digitar um CPF real e válido.")


def validate_email_format(form, field):
    raw = (field.data or "").strip()
    if not raw:
        raise ValidationError("Informe seu e-mail.")

    if "@" not in raw:
        raise ValidationError("E-mail inválido. Use o formato seu.nome@exemplo.com.")

    parts = raw.split("@")
    if len(parts) != 2:
        raise ValidationError("E-mail inválido. O e-mail deve conter apenas um caractere @.")

    user, domain = parts[0], parts[1]

    # Validação do usuário
    if len(user) < 2:
        raise ValidationError("E-mail inválido. O nome anterior ao @ deve ter pelo menos 2 caracteres.")

    # Não permitir repetição de caracteres / só zeros como 00000000000
    user_clean = re.sub(r"[\.\_\+\-]", "", user)
    if len(user_clean) >= 2 and len(set(user_clean)) == 1:
        raise ValidationError("E-mail inválido. Não são permitidas sequências repetidas como 00000000000.")

    if user_clean.isdigit() and (len(user_clean) < 4 or len(set(user_clean)) <= 2):
        raise ValidationError("E-mail inválido. Não utilize apenas números repetidos ou fictícios no e-mail.")

    # Validação do domínio
    if "." not in domain:
        raise ValidationError("E-mail inválido. O domínio deve conter uma extensão válida (ex: .com ou .com.br).")

    domain_parts = domain.split(".")
    if any(len(p) == 0 for p in domain_parts):
        raise ValidationError("E-mail inválido. Formato de domínio incorreto.")

    tld = domain_parts[-1]
    if not tld.isalpha() or len(tld) < 2:
        raise ValidationError("E-mail inválido. A extensão final do domínio deve ter pelo menos 2 letras (ex: .com, .br).")

    main_domain = domain_parts[0]
    if main_domain.isdigit() or (len(main_domain) >= 2 and len(set(main_domain)) == 1):
        raise ValidationError("E-mail inválido. O domínio informado não é válido.")

    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, raw):
        raise ValidationError("E-mail inválido. Contém caracteres ou formato não permitidos.")

    blacklist = {
        "teste@teste.com",
        "test@test.com",
        "admin@admin.com",
        "fake@fake.com",
        "exemplo@exemplo.com",
    }
    if raw.lower() in blacklist:
        raise ValidationError("E-mail inválido. Informe um endereço de e-mail real.")


class RegisterForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(message="Informe seu nome."), Length(min=2, max=120)])
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Informe seu e-mail."),
            validate_email_format,
        ],
    )
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
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Informe seu e-mail."),
            validate_email_format,
        ],
    )
    password = PasswordField("Senha", validators=[DataRequired(message="Informe sua senha.")])
    submit = SubmitField("Entrar")
