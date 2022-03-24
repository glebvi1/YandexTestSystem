import os

CONFIG_DIRECTION = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "yandex_lyceum_test_system"

    MAIL_SERVER = "smtp.yandex.ru"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "glebnasty.glebnasty@yandex.ru"
    MAIL_DEFAULT_SENDER = "glebnasty.glebnasty@yandex.ru"
    MAIL_PASSWORD = "xbqpvozehfiusdik"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/test_system.sqlite?check_same_thread=False"
