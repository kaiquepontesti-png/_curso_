from app.config import config


def get_config(name: str = "development"):
    return config.get(name, config["default"])
