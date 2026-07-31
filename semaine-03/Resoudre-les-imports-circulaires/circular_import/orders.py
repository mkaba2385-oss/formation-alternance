from .notifications import send_notification

def create_order(user):
    print(f"Commande créée pour {user.name}")
    send_notification(user)