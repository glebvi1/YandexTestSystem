from data.db_session import create_session
from data.group import Module
from data.test import Test, Question, AnswerOption
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
