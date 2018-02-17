from flask import session

from quizgo import socketio, req
from quizgo.game.quizgame import QuizGame
from quizgo.room.roomcontroller import RoomController
from flask_socketio import join_room, leave_room, emit, rooms, disconnect

rc = RoomController()


# 连接事件
@socketio.on('connect')
def on_connect():
    # print('Client connected')
    pass


# 连接断开事件
@socketio.on('disconnect')
def on_disconnect():
    conn_rooms = rooms()
    for room in conn_rooms:
        leave_room(room)
        rc.client_leave_room(sid=req.sid, room=room)
        # print('Client disconnected')
        emit("info", req.sid + ' left the room.', room=room)
        emit("clients", rc.all_clients_in_room(room=room), room=room)


# 创建房间
@socketio.on('createroom')
def on_create_room():
    sid = req.sid
    room = rc.create_room()
    emit("createroom", {"room": room}, room=sid)


# 获取房间客户端信息
@socketio.on('getroominfo')
def on_get_room_info(data):
    room = data['room']
    emit("clients", rc.all_clients_in_room(room=room), room=room)


# 加入房间
@socketio.on('joinroom')
def on_join(data):
    room = data['room']
    join_room(room)
    user_data = {'username': data['username'], 'avatar': data['avatar'], 'sid': req.sid}
    rc.client_join_room(user_data=user_data, room=room)
    # print(rc.all_rooms_in_poll())
    emit("info", data['username'] + ' has entered the room.', room=room)
    emit("clients", rc.all_clients_in_room(room=room), room=room)


# 离开房间
@socketio.on('leaveroom')
def on_leave():
    conn_rooms = rooms()
    for room in conn_rooms:
        if room != req.sid:
            leave_room(room)
            rc.client_leave_room(sid=req.sid, room=room)
            emit("info", req.sid + ' left the room.', room=room)
            emit("clients", rc.all_clients_in_room(room=room), room=room)


# 开始游戏
@socketio.on('startgame')
def on_start_game(data):
    room = data['room']
    if rc.create_game(room=room):
        if rc.start_game(room=room):
            emit("msg", "开始游戏", room=room)
        else:
            emit("alert", {'msg': "请等待所有玩家准备"}, room=req.sid)
    else:
        emit("alert", {'msg': "游戏正在进行，请旁观"}, room=req.sid)


# 结束游戏
@socketio.on('stopgame')
def on_stop_game(data):
    room = data['room']
    emit("msg", "结束游戏", room=room)


# 准备
@socketio.on('ready')
def on_ready(data):
    room = data['room']
    ready = data['ready']
    if rc.set_ready(room=room, ready=ready, sid=req.sid):
        emit("clients", rc.all_clients_in_room(room=room), room=room)


# sid是否是房主
@socketio.on('isowner')
def on_get_is_owner(data):
    room = data['room']
    emit("isowner", rc.get_is_owner(sid=req.sid, room=room), room=req.sid)


# 发送信息
@socketio.on('sendmsg')
def on_send_msg(data):
    msg = '%s:%s' % (data['username'], data['msg'])
    room = data['room']
    # if not rc.validate_answer(room=room, answer=data['msg']):
    #     emit("msg", msg, room=room)
    emit("msg", msg, room=room)


# 检查答案
@socketio.on('answer')
def on_validate_answer(data):
    room = data['room']
    if rc.validate_user_in_game(room=room, sid=req.sid):
        emit("answer", rc.validate_answer(room=room, sid=req.sid, answer=data['answer']), room=req.sid)
    else:
        emit("alert", {'msg': "旁观者无法答题"}, room=req.sid)
