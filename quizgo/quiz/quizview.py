from quizgo import app
from quizgo.quiz.quizcontroller import QuizController, SCQuizController


@app.route('/getquiz', methods=['GET'])
def get_quiz():
    qc = QuizController()
    quiz = qc.get_rand_quiz()
    q = quiz.question
    a = quiz.answer
    return 'question:' + q + '\nanswer:' + a


@app.route('/getscquiz', methods=['GET'])
def get_scquiz():
    qc = SCQuizController()
    quiz = qc.get_rand_scquiz()
    q = quiz.question
    c = quiz.choices
    a = quiz.answer
    return 'question:' + q + '\nchoices' + c + '\nanswer:' + a
