import os

from db import DATABASE_NAME

CONFIG_DIRECTION = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIRECTORY = "D:/1.Code/2. Python/YandexTestSystem/"


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "yandex_lyceum_test_system"

    MAIL_SERVER = "smtp.mail.ru"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "vyazgd@mail.ru"
    MAIL_DEFAULT_SENDER = "vyazgd@mail.ru"
    MAIL_PASSWORD = "hH0SjYWnZGMT26U28402"

    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    UPLOAD_FOLDER = os.path.join(CONFIG_DIRECTION, "files")

    RECAPTCHA_PUBLIC_KEY = "6LfsHpwfAAAAAOsEHZ1XD3PqHrFjJ-4ChFqoYPYs"
    RECAPTCHA_PRIVATE_KEY = "6LfsHpwfAAAAAAYqZsvc2bUhXbLJEDi6IRPv4Y91"


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///db/{DATABASE_NAME}?check_same_thread=False"
