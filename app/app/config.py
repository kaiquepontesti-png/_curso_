import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    database_url = os.getenv("DATABASE_URL", "").strip()
    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///num_esquece.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS = {}


class ProductionConfig(Config):
    DEBUG = False


config = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
