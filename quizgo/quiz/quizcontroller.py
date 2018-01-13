import random
import re

from quizgo import db
from quizgo.quiz.quizmodel import Quiz


class QuizController:
    def __init__(self):
        pass

    def insert_quiz(self, q, a, d):
        quiz = Quiz(q, a, d)
        db.session.add(quiz)
        db.session.commit()

    def get_rand_quiz(self):
        quiz_len = Quiz.query.count()
        rand_id = random.randint(0, quiz_len)
        return Quiz.query.filter_by(id=rand_id).first()


    def get_quiz_file(self):
        filename = '/Users/wei/Downloads/quizgo/Questions.txt'
        with open(filename, 'r', encoding='utf8') as file_to_read:
            while True:
                line = file_to_read.readline()
                if not line:
                    break
                q = re.findall(u"Question = [\"](.+?)[\"]", line)
                a = re.findall(u"Answer = [\"](.+?)[\"]", line)
                qc = QuizController()
                if Quiz.query.filter_by(question=q).first() is None:
                    qc.insert_quiz(q[0], a[0], 0)


