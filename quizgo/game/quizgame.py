from quizgo.game.game import Game
import eventlet

from quizgo.quiz.quizcontroller import QuizController


class QuizGame(Game):
    __quiz = ''

    def __init__(self, socketio, room, clients):
        super().__init__(socketio, room, clients)

    def start(self):
        super().start()
        self._game_round = 0
        while self._game_start and self._game_round < 5:
            self._game_round += 1
            self._game_left_time = 30
            self.__quiz = QuizController().get_rand_quiz()
            game_state = {"isPlaying": True, "round": self._game_round, "question": self.__quiz.question,
                          "hint": len(self.__quiz.answer)}
            self.socketio.emit("gamestate", game_state, room=self.room)
            while self._game_left_time > 0:
                eventlet.sleep(1)
                self._game_left_time -= 1
            if self._game_left_time > -7:
                self.socketio.emit("msg", "时间结束，答案是：" + self.__quiz.answer, room=self.room)
        self.stop()
        self.socketio.emit("gamestate", {"isPlaying": False},room=self.room)

    def stop(self):
        super().stop()
        self._game_left_time = -10

    def answer(self, answer):
        print(answer, self.__quiz.answer)
        if answer == self.__quiz.answer:
            self.socketio.emit("msg", "有人回答正确，给他鼓掌！", room=self.room)
            self._game_left_time = 10
            return True
        elif answer == '跳过':
            self._game_left_time = 3
        elif answer == '答案':
            self.socketio.emit("msg", "答案是：" + self.__quiz.answer, room=self.room)
            self._game_left_time = 3
        return False

    def is_running(self):
        return self._game_start
