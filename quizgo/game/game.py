# 所有游戏的基类
class Game(object):
    _game_start = False
    _game_round = 0
    _game_left_time = 0

    def __init__(self, socketio, room, clients):
        self.clients = clients
        self.room = room
        self.socketio = socketio
        self.init_clients()

    # 开始游戏
    def start(self):
        if self._game_start:
            return
        else:
            self._game_start = True

    # 结束游戏
    def stop(self):
        self._game_start = False

    # 新建游戏时初始化玩家信息
    def init_clients(self):
        for c in self.clients:
            c['score'] = 0
            c['answered'] = False

    # 游戏是否进行当中
    def is_running(self):
        return self._game_start

    # 该sid玩家是否在游戏中
    def user_in_game(self, sid):
        c = self.get_client_by_sid(sid=sid)
        if 'score' in c:
            return True
        return False

    # 开启新的一轮游戏
    def start_new_round(self):
        pass

    # 根据sid获取客户端
    def get_client_by_sid(self, sid):
        for c in self.clients:
            if sid == c['sid']:
                return c
