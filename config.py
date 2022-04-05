import os

from db import DATABASE_NAME

CONFIG_DIRECTION = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "yandex_lyceum_test_system"

    MAIL_SERVER = "smtp.mail.ru"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "vyazgd@mail.ru"
    MAIL_DEFAULT_SENDER = "vyazgd@mail.ru"
    MAIL_PASSWORD = "hH0SjYWnZGMT26U28402"


class DevelopmentConfig(BaseConfig):
    # DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///db/{DATABASE_NAME}?check_same_thread=False"
