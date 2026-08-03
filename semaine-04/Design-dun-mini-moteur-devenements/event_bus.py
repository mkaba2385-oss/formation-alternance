import asyncio
import inspect 

# Hiérarchie des événements

class Event:
    """Classe de base des événements."""
    pass


class UserRegistered(Event):
    def __init__(self, username):
        self.username = username

class ParcelleCreated(Event):
    def __init__(self, parcelle):
        self.parcelle = parcelle

class DiagnosticDone(Event):
    def __init__(self, diagnostic):
        self.diagnostic = diagnostic

# Event Bus

class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, handler):
        """Inscrit un handler pour un type d'événement."""
        self._subscribers.setdefault(event_type, []).append(handler)

    async def publish(self, event):
        """Publie un événement à tous les handlers."""
        handlers = self._subscribers.get(type(event), [])

        for handler in handlers:
            try:
                if inspect.iscoroutinefunction(handler):
                    await handler(event)
                else :
                    handler(event)
            except Exception as e:
                print(f"Erreur dans le handler {handler}: {e}")
            
# handlers synchrones

def logger(event):
    print(f"[LOG] Nouvel utilisateur : {event.username}")

def erreur(event):
    raise ValueError("Erreur volontaire !")


# handler asynchrone

async def envoyer_sms(event):
    await asyncio.sleep(1)
    print(f"[SMS] Bienvenue {event.username} !")

# Handler sous forme de méthode

class NotificationService:
    def envoyer_email(self, event):
        print(f"[EMAIL] Bienvenue {event.username} !")


# Démonstration

async def main():
    bus = EventBus()
    service = NotificationService()

    bus.subscribe(UserRegistered, logger)
    bus.subscribe(UserRegistered, envoyer_sms)
    bus.subscribe(UserRegistered, service.envoyer_email)
    bus.subscribe(UserRegistered, erreur)

    event = UserRegistered("Alice")

    await bus.publish(event)


if __name__ == "__main__":
    asyncio.run(main())