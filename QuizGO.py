from quizgo import app, socketio

if __name__ == '__main__':
    socketio.run(app=app, host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
