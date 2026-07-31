from .orders import create_order

class User:
    def __init__(self, name):
        self.name = name

def register_user(name):
    user = User(name)
    create_order(user)