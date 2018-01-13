from quizgo import app
from quizgo.quiz.quizcontroller import QuizController


@app.route('/getquiz', methods=['GET'])
def get_quiz():
    qc = QuizController()
    quiz = qc.get_rand_quiz()
    q = quiz.question
    a = quiz.answer
    return 'question:' + q + '\nanswer:' + a
