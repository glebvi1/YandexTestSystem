from typing import List, Tuple, Dict

from data.db_session import create_session
from data.group import Module, Group
from data.test import Test, Question, AnswerOption
from service.general_service import parse_object_ids, get_object_by_id


def save_test(name: str, questions: List[str], answers: List[Tuple[Tuple[str, bool]]],
              marks: List[str], module_id: int) -> bool:
    """Сохранение теста в БД
    :param name: название теста
    :param questions: список вопросов
    :param answers: список вариантов ответов
    :param marks: список критерий оценивания
    :param module_id: id модуля, в котором создается тест
    """
    session = create_session()

    test_from_db = session.query(Test).filter((Test.name == name) & (Test.module_id == module_id)).first()
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


def do_test(answers: List[Tuple[str]], test_id: int, questions: List[Question],
            answer_options: List[AnswerOption], student_id: int) -> None:
    """Прохождение теста учеником
    :param answers: ответы пользователя
    :param test_id: id теста, который сейчас проходят
    :param questions: список вопросов данного теста
    :param answer_options: варианты ответа данного теста
    :param student_id: id ученика, который делает тест
    """
    session = create_session()

    test = session.query(Test).filter(Test.id == test_id).first()

    count_right_questions = __count_right_answers(answers, questions, answer_options)
    mark = __put_mark(test.criteria, count_right_questions, len(questions))

    test.append_mark(student_id, mark)
    session.commit()


def parse_questions_id(questions_id: str):
    """Достаем вопросы и варианты ответов по id вопросам
    :param questions_id:  id вопросов
    """
    if len(questions_id) == 0:
        return ()
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


def get_marks_by_tests(tests: List[Test], student_id: int) -> List[int]:
    """Все оценки пользователя по заданным тестам
    :param tests: тесты, по которым берем оценку; если оценки нет, то ставим None
    :param student_id: id студента
    """
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


def get_student_to_mark_in_tests(all_tests: List[Test]) -> List[Dict[int:str]]:
    """Создаем словарь ученик-оценка по каждому тесту
    :param all_tests: тесты, по которым
    """
    lst_student_to_mark = []

    for test in all_tests:
        student_to_mark = {}
        if test.marks is None:
            lst_student_to_mark.append((test.name, student_to_mark))
            continue
        for pair in test.marks.split(";"):
            student_id, mark = pair.split("-")
            student_to_mark[int(student_id)] = mark

        lst_student_to_mark.append((test.name, student_to_mark))

    return lst_student_to_mark


def get_all_tests_by_group_id(group_id: int) -> List[Test]:
    """Достать все тесты в группы
    :param group_id: id группы, из которой достаем все тесты
    """
    all_tests = []
    group = get_object_by_id(group_id, Group)
    all_modules = parse_object_ids(group.modules_id, Module)

    for module in all_modules:
        tests = parse_object_ids(module.tests_id, Test)
        all_tests.extend(tests)
    return all_tests


def get_all_tests_by_module_id(module_id: int) -> List[Test]:
    """Достать из БД все тесты по модуль
    :param module_id: id модуля, из которого достаем тесты
    """
    module = get_object_by_id(module_id, Module)
    return parse_object_ids(module.tests_id, Test)


def get_statistics(data: list) -> Tuple[int, float, int]:
    """Статистика по данным
    :param data: список оценок
    """
    int_data = tuple(filter(lambda a: a is not None, data))
    int_data = tuple(map(int, int_data))

    return __min(int_data), __mean(int_data), __max(int_data)


def __mean(data: Tuple[int]) -> float:
    return round(sum(data) / len(data), 2) if len(data) != 0 else 0


def __min(data: Tuple[int]) -> int:
    return min(data) if len(data) != 0 else 0


def __max(data: Tuple[int]) -> int:
    return max(data) if len(data) != 0 else 0


def __count_right_answers(answers: List[Tuple[str]], questions: List[Question],
                          answer_options: List[AnswerOption]) -> int:
    """Количество правильных ответов
    :param answers: ответы студента
    :param questions: вопросы
    :param answer_options: варианты ответа
    """
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


def __put_mark(criteria: str, count_right_questions: int, count_question: int) -> int:
    """Возвращает оценку по критериям
    :param criteria: критерии
    :param count_right_questions: количество правильных ответов
    :param count_question: количество вопросов
    """
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
