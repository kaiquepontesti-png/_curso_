from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ShoppingListForm(FlaskForm):
    titulo = StringField("Título da lista", validators=[DataRequired(message="O título é obrigatório."), Length(min=2, max=120)])
    descricao = TextAreaField("Descrição", validators=[Length(max=500)])
    submit = SubmitField("Salvar lista")


class ShoppingItemForm(FlaskForm):
    nome = StringField("Nome do item", validators=[DataRequired(message="Informe o nome do item."), Length(min=2, max=120)])
    quantidade = StringField("Quantidade", default="1", validators=[Length(max=30)])
    categoria = StringField("Categoria", default="geral", validators=[Length(max=80)])
    comprado = BooleanField("Já foi comprado")
    submit = SubmitField("Adicionar item")
