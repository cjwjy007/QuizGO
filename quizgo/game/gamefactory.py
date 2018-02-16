from quizgo.game.quizgame import QuizGame
from quizgo.game.scquizgame import SCQuizGame

# 游戏工厂返回不同游戏实例
class GameFactory:
    @staticmethod
    def new_game(game_type, socketio, room, clients):
        if game_type == 'quiz':
            return QuizGame(socketio=socketio, room=room, clients=clients)
        elif game_type == 'scquiz':
            return SCQuizGame(socketio=socketio, room=room, clients=clients)
