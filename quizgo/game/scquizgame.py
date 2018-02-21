from quizgo.game.game import Game
import eventlet

from quizgo.quiz.quizcontroller import SCQuizController


class SCQuizGame(Game):
    __quiz = ''

    def __init__(self, socketio, room, clients):
        super().__init__(socketio, room, clients)

    # 开始游戏
    def start(self):
        super().start()
        self._game_round = 0
        while self._game_start and self._game_round < 7:
            self.socketio.emit("clients", self.clients, room=self.room)
            self.start_new_round()
            self._game_round += 1
            self._game_left_time = 13
            self.__quiz = SCQuizController().get_rand_scquiz()
            if self.__quiz is None:
                continue
            game_state = {"isPlaying": True, "round": self._game_round, "question": self.__quiz.question,
                          "choices": self.__quiz.choices}
            self.socketio.emit("gamestate", game_state, room=self.room)
            while self._game_left_time > 0:
                eventlet.sleep(1)
                self._game_left_time -= 1
            if self._game_left_time > -7:
                self.socketio.emit("msg", "时间结束，答案是：" + self.__quiz.answer, room=self.room)
            self.socketio.emit("clients", self.clients, room=self.room)
        self.stop()
        score_table = self.get_score_table()
        self.socketio.emit("gamestate", {"isPlaying": False, "scoreTable": score_table}, room=self.room)

    # 停止游戏
    def stop(self):
        super().stop()
        self._game_left_time = -10

    # 接受玩家的答案
    def answer(self, answer, sid):
        # print(answer, self.__quiz.answer)
        if answer == self.__quiz.answer:
            score = self._game_left_time
            self.set_client_state(sid, score)
            answer_ret = {'answer': self.__quiz.answer, 'correct': True, 'score': score}
        else:
            self.set_client_state(sid, 0)
            answer_ret = {'answer': self.__quiz.answer, 'correct': False, 'score': 0}
        if self.is_all_clients_answered():
            self._game_left_time = 3
        return answer_ret

    # 更改玩家分数与作答情况
    def set_client_state(self, sid, score):
        c = super().get_client_by_sid(sid=sid)
        if self.user_in_game(user=c):
            if c['answered'] is False:
                c['score'] += score
                c['answered'] = True

    # 开启新的一轮游戏
    def start_new_round(self):
        super().start_new_round()
        for c in self.clients:
            c['answered'] = False

    # 判断是否所有人已经作答
    def is_all_clients_answered(self):
        for c in self.clients:
            if self.user_in_game(user=c):
                if c['answered'] is False:
                    return False
        return True

    # 获取分数表
    def get_score_table(self):
        score_table = []
        for c in self.clients:
            if self.user_in_game(user=c):
                score_table.append({'username': c.get('username'), 'score': c.get('score'), 'avatar': c.get('avatar')})
        score_table.sort(key=lambda x: x["score"], reverse=True)
        return score_table
