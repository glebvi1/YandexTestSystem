from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data.test import Test
from service.general_service import get_object_by_id
from service.group_service import group_contains_user
from service.test_service import save_test, do_test, get_marks_by_tests, parse_questions_id
from service.user_service import is_teacher, is_student

test_page = Blueprint("test_page", __name__, template_folder="templates")
count_questions = 5

"""Создание теста"""


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/create-test", methods=["GET"])
@login_required
def create_test_get(group_id, module_id):
    if not is_teacher(current_user) or not group_contains_user(group_id, current_user.id):
        abort(403)

    return render_template("create_test.html", group_id=group_id,
                           module_id=module_id, count_arr=[x for x in range(1, count_questions + 1)],
                           role="teacher")


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/create-test", methods=["POST"])
@login_required
def create_test_post(group_id, module_id):
    if not is_teacher(current_user) or not group_contains_user(group_id, current_user.id):
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

        for mark in marks:
            if not (0 <= int(mark) <= 100):
                message = "Оценка меряется в процентах. Оценка лежит в границах от 0 до 100."
                return render_template("create_test.html", group_id=group_id,
                                       module_id=module_id, count_arr=[x for x in range(1, count_questions + 1)],
                                       message=message)

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

        if not save_test(name, questions, answers, marks, module_id):
            message = "Тест с таким названием уже существует."

    return render_template("create_test.html", group_id=group_id,
                           module_id=module_id, count_arr=[x for x in range(1, count_questions + 1)],
                           message=message, role="teacher")


"""Просмотр теста учителем"""


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/test/<int:test_id>", methods=["GET"])
@login_required
def test_i(group_id, module_id, test_id):
    if not is_teacher(current_user) or not group_contains_user(group_id, current_user.id):
        abort(403)

    test = get_object_by_id(test_id, Test)
    name = test.name

    questions, answer_options = parse_questions_id(test.questions_id)

    return render_template("view_teacher_test.html", test_name=name,
                           questions=questions, answer_options=answer_options,
                           role="teacher", group_id=group_id, module_id=module_id)


""" Прохождение теста """


@test_page.route("/student/group/<int:group_id>/module/<int:module_id>/test/<int:test_id>", methods=["GET"])
@login_required
def do_test_get(group_id, module_id, test_id):
    if not group_contains_user(group_id, current_user.id):
        return abort(403)
    marks = get_marks_by_tests([get_object_by_id(test_id, Test)], current_user.id)
    if not is_student(current_user) or marks[0] is not None:
        abort(403)

    test = get_object_by_id(test_id, Test)
    name = test.name

    questions, answer_options = parse_questions_id(test.questions_id)

    return render_template("do_test.html", test_name=name, group_id=group_id, module_id=module_id, test_id=test_id,
                           questions=questions, answer_options=answer_options)


@test_page.route("/student/group/<int:group_id>/module/<int:module_id>/test/<int:test_id>", methods=["POST"])
@login_required
def do_test_post(group_id, module_id, test_id):
    if not is_student(current_user) or not group_contains_user(group_id, current_user.id):
        abort(403)

    test = get_object_by_id(test_id, Test)
    questions, answer_options = parse_questions_id(test.questions_id)

    if request.form.get("button") == "Отправить":
        answers = []

        for number_question in range(len(questions)):
            current_answers = []
            count_answer_option = len(answer_options[number_question])
            if count_answer_option == 1:
                answer = request.form.get(f"answer{number_question}0")
                current_answers.append(answer)
            else:
                for number_answer_option in range(count_answer_option):
                    answer = request.form.get(f"answer{number_question}{number_answer_option}")
                    if answer == "on":
                        current_answers.append(answer_options[number_question][number_answer_option].answer)

            answers.append(tuple(current_answers))

        do_test(answers, test_id, questions, answer_options, current_user.id)

    return redirect(f"/student/group/{group_id}/module/{module_id}")
