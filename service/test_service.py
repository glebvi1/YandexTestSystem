from data.db_session import create_session
from data.group import Module
from data.test import Test, Question, AnswerOption
from data.user import User
from service.general_service import parse_object_ids


def create_test(name, questions, answers, marks, module_id) -> bool:
    session = create_session()

    test_from_db = session.query(Test).filter(Test.name == name)
    if test_from_db is not None:
        return False

    questions_id = []

    for index, answer in enumerate(answers):
        answer_options_id = []
        for ao in answer:
            answer_option = AnswerOption()
            answer_option.answer = ao[0]
            answer_option.is_right = ao[1]

            session.add(answer_option)
            session.commit()

            answer_options_id.append(str(answer_option.id))

        question = Question()
        question.main_quest = questions[index]
        question.answer_options = ";".join(answer_options_id)

        session.add(question)
        session.commit()

        questions_id.append(str(question.id))

    test = Test()
    test.name = name
    test.module_id = module_id
    test.criteria = ";".join(marks)
    test.questions_id = ";".join(questions_id)

    session.add(test)
    session.commit()

    module = session.query(Module).filter(Module.id == module_id).first()
    module.append_test_id(test.id)
    session.commit()

    return True


def get_tests_by_module_id(module_id):
    session = create_session()
    module = session.query(Module).filter(Module.id == module_id).first()
    return parse_object_ids(module.tests_id, Test)


def parse_question_id(questions_id):
    if len(questions_id) == 0:
        return []
    session = create_session()
    questions = []
    answers_options = []
    for question_id in questions_id.split(";"):
        question = session.query(Question).filter(Question.id == question_id).first()
        aos = []
        for ao_id in question.answer_options.split(";"):
            ao = session.query(AnswerOption).filter(AnswerOption.id == ao_id).first()
            aos.append(ao)

        answers_options.append(tuple(aos))
        questions.append(question)
    return questions, answers_options


def get_questions_by_test(test):
    return parse_question_id(test.questions_id)


def do_test(answers: list, test_id, questions, answer_options, student_id: User):
    session = create_session()

    test = session.query(Test).filter(Test.id == test_id).first()

    count_right_questions = __count_right_answers(answers, questions, answer_options)
    mark = __put_mark(test.criteria, count_right_questions, len(questions))

    test.append_mark(student_id, mark)
    session.commit()


def get_marks_by_tests(tests, student_id):
    marks = []
    for test in tests:
        if test.marks is None:
            marks.append(None)
            continue

        value = None
        for pair in test.marks.split(";"):
            data = pair.split("-")
            if data[0] == str(student_id):
                value = data[1]
                break

        marks.append(value)

    return marks


def __count_right_answers(answers, questions, answer_options):
    count_right_questions = 0
    for number_question in range(len(questions)):

        count_answer_option = len(answer_options[number_question])
        if count_answer_option == 1:
            answer = answers[number_question][0]
            right_answer = answer_options[number_question][0].answer
            if answer == right_answer:
                count_right_questions += 1

        else:
            count_right_student_answer = 0
            for number_answer_option in range(count_answer_option):
                answer_option = answer_options[number_question][number_answer_option]
                answer = answer_option.answer
                is_right = answer_option.is_right

                if (answer in answers[number_question] and is_right) or\
                        (not is_right and answer not in answers[number_question]):
                    count_right_student_answer += 1

            if count_right_student_answer == count_answer_option:
                count_right_questions += 1

    return count_right_questions


def __put_mark(criteria, count_right_questions, count_question):
    tpl_criteria = tuple(map(int, criteria.split(";")))
    mark = 2

    percentage = count_right_questions / count_question * 100
    if percentage < tpl_criteria[0]:
        mark = 2
    elif tpl_criteria[0] <= percentage < tpl_criteria[1]:
        mark = 3
    elif tpl_criteria[1] <= percentage < tpl_criteria[2]:
        mark = 4
    elif tpl_criteria[2] <= percentage:
        mark = 5

    return mark
