from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class NumEsqueceForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="O título é obrigatório."), Length(min=3, max=120)],
    )
    descricao = TextAreaField(
        "Descrição",
        validators=[DataRequired(message="A descrição é obrigatória."), Length(min=5, max=2000)],
    )
    categoria = StringField(
        "Categoria",
        validators=[DataRequired(message="A categoria é obrigatória."), Length(min=2, max=60)],
    )
    status = SelectField(
        "Status",
        choices=[
            ("pendente", "Pendente"),
            ("em_andamento", "Em andamento"),
            ("concluido", "Concluído"),
        ],
        validators=[DataRequired(message="O status é obrigatório.")],
    )
    data_vencimento = DateField("Data de vencimento", format="%Y-%m-%d", validators=[Optional()])
    submit = SubmitField("Salvar")
