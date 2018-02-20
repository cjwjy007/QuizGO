from flask import render_template

from quizgo import app
from quizgo.room.roomview import rc


@app.route('/roompoll', methods=['GET'])
def get_roompoll():
    room_poll = rc.all_rooms_in_poll()
    ret = []
    for key, value in room_poll.items():
        usernames = []
        clients = value.get('clients')
        for c in clients:
            usernames.append(c.get('username'))
        ret.append([key, usernames])
    return render_template('managetable.html', ret=ret)
