class UserController:
    user_poll = {}

    def __init__(self):
        pass

    def add_user(self, sid, username):
        if sid in self.user_poll:
            self.user_poll[sid] = username

    def remove_user(self, sid):
        if sid in self.user_poll:
            del self.user_poll[sid]
