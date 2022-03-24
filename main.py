import logging

from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail

from controllers.group_controller import group_page
from controllers.student_controller import student_page
from controllers.teacher_controller import teacher_page
from controllers.user_controller import user_page
from data.db_session import create_session
from data.db_session import global_init
from data.user import User

app = Flask(__name__, template_folder="templates")
app.config.from_object("config.DevelopmentConfig")

app.register_blueprint(user_page)
app.register_blueprint(teacher_page)
app.register_blueprint(student_page)
app.register_blueprint(group_page)

global_init("db/test_system.sqlite")

login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail()
mail.init_app(app)

logging.basicConfig(level=logging.INFO)


@login_manager.user_loader
def load_user(user_id):
    return create_session().query(User).get(user_id)


@app.route("/")
def index():
    logging.info("Start application")
    return render_template("start_page.html", title="Главная страница")


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")
