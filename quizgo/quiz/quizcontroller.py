import random
import re

from quizgo import db
from quizgo.quiz.quizmodel import SCQuiz, Quiz


# unused
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
        return Quiz.query.get(rand_id).first()

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


class SCQuizController:
    def __init__(self):
        pass

    def insert_scquiz(self, q, c, a, d):
        quiz = SCQuiz(q, c, a, d)
        db.session.add(quiz)
        db.session.commit()

    def get_scquiz_file(self):
        filename = 'quiz.txt'
        with open(filename, 'r', encoding='utf8') as file_to_read:
            while True:
                line = file_to_read.readline()
                if not line:
                    break
                info = line.split("--")
                print(info[0])
                q = info[1]
                c = info[2]
                a = info[3]
                if c.endswith("|"):
                    c = c[:-1]
                if a.endswith("\n"):
                    a = a[:-1]
                scqc = SCQuizController()
                if SCQuiz.query.filter_by(question=q).first() is None:
                    scqc.insert_scquiz(q, c, a, 0)

    # 随机取出一个题目
    def get_rand_scquiz(self):
        try:
            quiz_len = SCQuiz.query.count()
            rand_id = random.randint(0, quiz_len)
            quiz = SCQuiz.query.filter_by(id=rand_id).first()
            if quiz:
                return quiz
            else:
                return None
        except Exception as e:
            db.session.close_all()
            db.engine.dispose()
            db.create_scoped_session()
            return None


if __name__ == '__main__':
    scqc = SCQuizController()
    scqc.get_scquiz_file()
