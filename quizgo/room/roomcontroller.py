import random
import string

from quizgo import socketio
from quizgo.game.gamefactory import GameFactory


class RoomController:
    room_pool = {}

    def __init__(self):
        pass

    # 创建房间，随机房间号加入房间池
    def create_room(self, room=None):
        if room is None:
            while True:
                room = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                if room not in self.room_pool:
                    self.room_pool[room] = {'game': None, 'clients': []}
                    return room
        else:
            if room not in self.room_pool:
                self.room_pool[room] = {'game': None, 'clients': []}
                return room

    # 客户端加入房间
    def client_join_room(self, user_data, room):
        user = {'username': user_data['username'], 'owner': True, 'sid': user_data['sid'],
                'avatar': user_data['avatar'], 'ready': False}
        if room in self.room_pool:
            if len(self.get_clients_by_room(room=room)) != 0:
                user['owner'] = False
            self.get_clients_by_room(room=room).append(user)
        else:
            self.create_room(room)
            self.room_pool[room]['clients'] = [user]

    # 客户端离开房间
    def client_leave_room(self, sid, room):
        if room in self.room_pool:
            idx, val = self.get_client_by_sid(sid=sid, room=room)
            self.get_clients_by_room(room=room).pop(idx)
            if val['owner'] is True and len(self.get_clients_by_room(room=room)) != 0:
                self.room_pool[room]['clients'][0]['owner'] = True
            if len(self.get_clients_by_room(room=room)) == 0:
                if self.get_game_by_room(room=room):
                    self.room_pool[room]['game'].stop()
                self.room_pool.pop(room)

    # 放回房间中客户端信息
    def all_clients_in_room(self, room):
        if room in self.room_pool:
            return self.get_clients_by_room(room=room)
        else:
            return []

    # 放回房间池中所有房间信息
    def all_rooms_in_poll(self):
        return self.room_pool

    # 返回一个sid是否为房间房主
    def get_is_owner(self, sid, room):
        idx, val = self.get_client_by_sid(sid=sid, room=room)
        return val['owner']

    # 创建游戏
    def create_game(self, room, game_type='scquiz'):
        game = self.get_game_by_room(room=room)
        if game and game.is_running():
            return False
        else:
            game = GameFactory().new_game(game_type=game_type, socketio=socketio, room=room,
                                          clients=self.get_clients_by_room(room=room))
            self.room_pool[room]['game'] = game
            return True

    # 开始游戏
    def start_game(self, room):
        game = self.get_game_by_room(room=room)
        if not game.is_running() and self.is_all_clients_ready(room=room):
            socketio.start_background_task(target=game.start)
            return True
        else:
            return False

    # 判断答案是否正确
    def validate_answer(self, room, sid, answer=None):
        game = self.get_game_by_room(room=room)
        return game.answer(sid=sid, answer=answer)

    # 判断用户是否在游戏中
    def validate_user_in_game(self, room, sid):
        game = self.get_game_by_room(room=room)
        return game.user_in_game(sid=sid)

    # 准备与取消准备
    def set_ready(self, room, ready, sid):
        id, val = self.get_client_by_sid(sid=sid, room=room)
        if val['owner'] is False:
            val['ready'] = ready
            return True
        return False

    # 判断是否所有客户端都准备
    def is_all_clients_ready(self, room):
        for c in self.get_clients_by_room(room=room):
            if c['ready'] is False and c['owner'] is not True:
                return False
        return True

    # 根据sid获取客户端索引与对象
    def get_client_by_sid(self, sid, room):
        for idx, val in enumerate(self.get_clients_by_room(room=room)):
            if val['sid'] == sid:
                return idx, val

    # 根据房间号获取游戏对象
    def get_game_by_room(self, room):
        return self.room_pool[room]['game']

    # 根据房间号获取客户端对象
    def get_clients_by_room(self, room):
        return self.room_pool[room]['clients']
