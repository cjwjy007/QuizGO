from flask import render_template

from quizgo import app
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
