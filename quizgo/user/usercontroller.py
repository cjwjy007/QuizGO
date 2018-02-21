class UserController:
    user_pool = {}

    def __init__(self):
        pass

    def add_user(self, sid, username):
        if sid in self.user_pool:
            self.user_pool[sid] = username

    def remove_user(self, sid):
        if sid in self.user_pool:
            del self.user_pool[sid]
