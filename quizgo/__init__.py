from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
from flask_socketio import SocketIO

# make sure to use eventlet and call eventlet.monkey_patch()
import eventlet

eventlet.monkey_patch()
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
req = request

# make sure to set the async_mode as 'eventlet'
socketio = SocketIO(app, async_mode='eventlet')

import quizgo.router
