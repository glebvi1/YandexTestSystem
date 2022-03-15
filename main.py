import logging

from flask import Flask, render_template
from flask_login import LoginManager

from controllers.teacher_controller import teacher_page
from controllers.user_controller import user_page
from data.db_session import create_session
from data.db_session import global_init
from data.user import User

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "yandex_lyceum_test_system"
app.register_blueprint(user_page)
app.register_blueprint(teacher_page)

global_init("db/test_system.sqlite")
login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig(level=logging.INFO)


@login_manager.user_loader
def load_user(user_id):
    return create_session().query(User).get(user_id)


@app.route("/")
def index():
    return render_template("start_page.html", title="Главная страница")


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")
