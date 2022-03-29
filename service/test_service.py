from data.db_session import create_session
from data.group import Module
from data.test import Test, Question, AnswerOption


def create_test(name, questions, answers, marks, module_id):
    session = create_session()
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
