from flask import Blueprint, render_template, request
from flask_login import login_required

test_page = Blueprint("test_page", __name__, template_folder="templates")
count_questions = 5


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/create-test", methods=["GET"])
@login_required
def create_test_get(group_id, module_id):
    global count_questions
    count_questions = request.args.get("count")
    if count_questions not in range(3, 16):
        count_questions = 5

    return render_template("create_test.html", group_id=group_id, module_id=module_id)


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/create-test", methods=["POST"])
@login_required
def create_test_post(group_id, module_id):

    return render_template("create_test.html", group_id=group_id, module_id=module_id)
