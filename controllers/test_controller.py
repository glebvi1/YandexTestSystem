from flask import Blueprint, render_template, request
from flask_login import login_required
from werkzeug.utils import redirect

from service.test_service import create_test

test_page = Blueprint("test_page", __name__, template_folder="templates")
count_questions = 5


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/create-test", methods=["GET"])
@login_required
def create_test_get(group_id, module_id):
    return render_template("create_test.html", group_id=group_id,
                           module_id=module_id, count_arr=[x for x in range(1, count_questions + 1)])


@test_page.route("/teacher/group/<int:group_id>/module/<int:module_id>/create-test", methods=["POST"])
@login_required
def create_test_post(group_id, module_id):
    global count_questions

    if request.form.get("button") == "Сохранить":
        count_questions = int(request.form.get("count"))
        if count_questions not in list(range(3, 16)):
            count_questions = 5
        return redirect(f"/teacher/group/{group_id}/module/{module_id}/create-test")

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
                if is_correct is None:
                    is_correct = False
                else:
                    is_correct = True

                if current_answer != "":
                    answer.append((current_answer, is_correct))

            answers.append(tuple(answer))
        print(answers)
        create_test(name, questions, answers, marks, module_id)

    return render_template("create_test.html", group_id=group_id,
                           module_id=module_id, count_arr=[x for x in range(1, count_questions + 1)])
