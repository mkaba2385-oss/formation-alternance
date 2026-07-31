from .models import User
from .orders import create_order


def register_user(name):
    user = User(name)
    create_order(user)