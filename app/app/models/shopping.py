from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    shopping_lists = db.relationship("ShoppingList", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class ShoppingList(db.Model):
    __tablename__ = "shopping_lists"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    user = db.relationship("User", back_populates="shopping_lists")
    items = db.relationship("ShoppingItem", back_populates="shopping_list", cascade="all, delete-orphan")
    library_entry = db.relationship(
        "NumEsquece",
        uselist=False,
        foreign_keys="NumEsquece.shopping_list_id",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<ShoppingList {self.titulo}>"


class ShoppingItem(db.Model):
    __tablename__ = "shopping_items"

    id = db.Column(db.Integer, primary_key=True)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey("shopping_lists.id"), nullable=False, index=True)
    nome = db.Column(db.String(120), nullable=False)
    quantidade = db.Column(db.String(30), nullable=False, default="1")
    categoria = db.Column(db.String(80), nullable=False, default="geral")
    preco = db.Column(db.String(30), nullable=True, default="0")
    comprado = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    shopping_list = db.relationship("ShoppingList", back_populates="items")

    def __repr__(self):
        return f"<ShoppingItem {self.nome}>"
