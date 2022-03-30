from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data.test import Test
from service.general_service import get_object_by_id
from service.test_service import create_test, get_questions_by_test
from service.user_service import is_teacher

test_page = Blueprint("test_page", __name__, template_folder="templates")
count_questions = 5


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/create-test", methods=["GET"])
@login_required
def create_test_get(group_id, module_id):
    if not is_teacher(current_user):
        abort(403)
    return render_template("create_test.html", group_id=group_id,
                           module_id=module_id, count_arr=[x for x in range(1, count_questions + 1)])


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/create-test", methods=["POST"])
@login_required
def create_test_post(group_id, module_id):
    if not is_teacher(current_user):
        abort(403)

    global count_questions
    message = ""

    if request.form.get("button") == "Сохранить":
        count_questions = int(request.form.get("count"))
        if count_questions not in list(range(3, 16)):
            count_questions = 5
            message = "Количество вопросов может быть от 3 до 15."

    elif request.form.get("button2") == "Создать тест":

        name = request.form.get("title")
        questions = []
        answers = []
        marks = [request.form.get("mark3"), request.form.get("mark4"), request.form.get("mark5")]

        for question_number in range(1, count_questions + 1):
            questions.append(request.form.get(f"question{question_number}"))

            answer = []
            for answer_number in range(1, 6):
                current_answer = request.form.get(f"answer{question_number}{answer_number}")
                is_correct = request.form.get(f"isCorrect{question_number}{answer_number}")
                is_correct = False if is_correct is None else True

                if current_answer != "":
                    answer.append((current_answer, is_correct))

            answers.append(tuple(answer))

        if not create_test(name, questions, answers, marks, module_id):
            message = "Тест с таким названием уже существует."

    return render_template("create_test.html", group_id=group_id,
                           module_id=module_id, count_arr=[x for x in range(1, count_questions + 1)],
                           message=message)


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/test/<int:test_id>", methods=["GET"])
@login_required
def test_i(group_id, module_id, test_id):
    test = get_object_by_id(test_id, Test)
    name = test.name

    questions, answer_options = get_questions_by_test(test)
    print(questions)
    print(answer_options)
    return render_template("view_teacher_test.html", test_name=name,
                           questions=questions, answer_options=answer_options)
