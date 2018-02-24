from flask import render_template

from quizgo import app, db
from quizgo.room.roomview import rc


@app.route('/roompool', methods=['GET'])
def get_roompool():
    room_pool = rc.all_rooms_in_pool()
    ret = []
    for key, value in room_pool.items():
        usernames = []
        clients = value.get('clients')
        for c in clients:
            usernames.append(c.get('username'))
        ret.append([key, usernames])
    return render_template('managetable.html', ret=ret)


@app.route('/cleanroom', methods=['GET'])
def clean_room():
    room_pool = rc.all_rooms_in_pool()
    for key, value in room_pool.items():
        clients = value.get('clients')
        if clients is not None and len(clients) == 0:
            room_pool.pop(key)
    return render_template('success.html')


@app.route('/resetdb', methods=['GET'])
def reset_db():
    db.session.close_all()
    db.engine.dispose()
    db.create_scoped_session()
    return render_template('success.html')
