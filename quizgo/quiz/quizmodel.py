from quizgo import db


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), unique=True)
    answer = db.Column(db.String(200))
    difficulty = db.Column(db.Integer)

    def __init__(self, question, answer, difficulty):
        self.difficulty = difficulty
        self.answer = answer
        self.question = question


if __name__ == '__main__':
    db.create_all()