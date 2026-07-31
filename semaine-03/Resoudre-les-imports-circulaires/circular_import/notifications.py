from .models import User


def send_notification(user: User):
    print(f"Notification envoyée à {user.name}")