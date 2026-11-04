from flask import Flask
from sqlalchemy import inspect, text

from app.config import config
from app.extensions import csrf, db, login_manager, migrate
from app.models.num_esquece import NumEsquece
from app.models.shopping import ShoppingItem, ShoppingList, User
from app.routes.auth_routes import auth_bp
from app.routes.num_esquece_routes import num_esquece_bp
from app.routes.shopping_routes import shopping_bp


@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))


def ensure_user_schema():
    inspector = inspect(db.engine)
    columns = [column["name"] for column in inspector.get_columns("users")]
    if "cpf" not in columns:
        db.session.execute(text("ALTER TABLE users ADD COLUMN cpf VARCHAR(14)"))
        db.session.commit()


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        ensure_user_schema()

    app.register_blueprint(auth_bp)
    app.register_blueprint(shopping_bp)
    app.register_blueprint(num_esquece_bp)

    @app.errorhandler(404)
    def not_found(error):
        return "<h1>Página não encontrada</h1>", 404

    @app.errorhandler(500)
    def internal_error(error):
        return "<h1>Erro interno do servidor</h1>", 500

    return app
