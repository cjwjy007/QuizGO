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
        if room:
            user_name = user_data.get('username', default='wjy666')[0:7]
            user_avatar = user_data.get('avatar', default='')
            user = {'username': user_name, 'owner': True, 'sid': user_data['sid'],
                    'avatar': user_avatar, 'ready': False}
            if self.validate_room(room=room):
                if len(self.get_clients_by_room(room=room)) != 0:
                    user['owner'] = False
                self.get_clients_by_room(room=room).append(user)
            else:
                self.create_room(room)
                try:
                    self.room_pool[room]['clients'] = [user]
                except KeyError as e:
                    print(e)

    # 客户端离开房间
    def client_leave_room(self, sid, room):
        try:
            if room and self.validate_room(room=room):
                idx, val = self.get_client_by_sid(sid=sid, room=room)
                self.get_clients_by_room(room=room).pop(idx)
                if val.get('owner') is True and len(self.get_clients_by_room(room=room)) != 0:
                    self.room_pool[room]['clients'][0]['owner'] = True
                if len(self.get_clients_by_room(room=room)) == 0:
                    if self.get_game_by_room(room=room):
                        self.room_pool[room]['game'].stop()
                    self.room_pool.pop(room)
        except KeyError as e:
            print(e)

    # 放回房间中客户端信息
    def all_clients_in_room(self, room):
        if self.validate_room(room=room):
            return self.get_clients_by_room(room=room)
        else:
            return []

    # 放回房间池中所有房间信息
    def all_rooms_in_poll(self):
        return self.room_pool

    # 返回一个sid是否为房间房主
    def get_is_owner(self, sid, room):
        idx, val = self.get_client_by_sid(sid=sid, room=room)
        return val.get('owner')

    # 创建游戏
    def create_game(self, room, game_type='scquiz'):
        if self.validate_room(room=room):
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
        if self.validate_room(room=room):
            game = self.get_game_by_room(room=room)
            if not game.is_running() and self.is_all_clients_ready(room=room):
                socketio.start_background_task(target=game.start)
                return True
            else:
                return False

    # 判断答案是否正确
    def validate_answer(self, room, sid, answer=None):
        if self.validate_room(room=room):
            game = self.get_game_by_room(room=room)
            if game:
                return game.answer(sid=sid, answer=answer)
            return False

    # 判断用户是否在游戏中
    def validate_user_in_game(self, room, sid):
        if self.validate_room(room=room):
            game = self.get_game_by_room(room=room)
            if game:
                return game.user_in_game(sid=sid)
            return False

    # 准备与取消准备
    def set_ready(self, room, ready, sid):
        if self.validate_room(room=room):
            id, val = self.get_client_by_sid(sid=sid, room=room)
            if val.get('owner') is False:
                val['ready'] = ready
                return True
            return False

    # 判断是否所有客户端都准备
    def is_all_clients_ready(self, room):
        if self.validate_room(room=room):
            for c in self.get_clients_by_room(room=room):
                if c.get('ready') is False and c.get('owner') is not True:
                    return False
            return True

    # 根据sid获取客户端索引与对象
    def get_client_by_sid(self, sid, room):
        if self.validate_room(room=room):
            for idx, val in enumerate(self.get_clients_by_room(room=room)):
                if val['sid'] == sid:
                    return idx, val

    # 根据房间号获取游戏对象
    def get_game_by_room(self, room):
        try:
            return self.room_pool[room]['game']
        except KeyError as e:
            print(e)
            return []

    # 根据房间号获取客户端对象
    def get_clients_by_room(self, room):
        try:
            return self.room_pool[room]['clients']
        except KeyError as e:
            print(e)
            return []

    # 合法的房间号
    def validate_room(self, room):
        return room in self.room_pool
