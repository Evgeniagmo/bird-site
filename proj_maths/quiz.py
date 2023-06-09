import os
from . import birds_db
from random import choices


class Quiz:
    def __init__(self):
        random_birds = choices(birds_db.db_get_birds_for_table(), k=int(os.getenv("QUIZ_Q_NUMBER")))

        self.qna = []
        cnt = 0
        for rb in random_birds:
            qna_item = []
            cnt += 1
            qna_item.append(cnt)
            qna_item = qna_item + rb[1:3]
            self.qna.append(qna_item)

        self.user_answers = []

    def record_user_answer(self, a):
        """Добавляет ответ пользователя в переменную экземпляра (список ответов)"""
        self.user_answers.append(a)

    def get_user_answers(self):
        return self.user_answers

    def check_quiz(self):
        """Проверяет ответы и возвращает список эмодзи"""
        correct_answers = [qna_item[2] for qna_item in self.qna]
        answers_true_false = [i.lower() == j.lower() for i, j in zip(self.user_answers, correct_answers)]
        return answers_true_false
