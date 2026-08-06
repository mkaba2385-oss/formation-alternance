# Refactor multi-patterns sur Sini

## Version 1 — Strategy

### Code

```python
from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    def envoyer(self, message, utilisateur):
        pass


class SMSNotification(NotificationStrategy):
    def envoyer(self, message, utilisateur):
        print(f"SMS envoyé à {utilisateur} : {message}")


class PushNotification(NotificationStrategy):
    def envoyer(self, message, utilisateur):
        print(f"Push envoyé à {utilisateur} : {message}")


class InAppNotification(NotificationStrategy):
    def envoyer(self, message, utilisateur):
        print(f"Notification In-App pour {utilisateur} : {message}")


class NotificationService:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def envoyer(self, message, utilisateur):
        self.strategy.envoyer(message, utilisateur)


service = NotificationService(SMSNotification())
service.envoyer("Bienvenue sur Sini !", "Alice")

service.strategy = PushNotification()
service.envoyer("Bienvenue sur Sini !", "Alice")
```

---

# Version 2 — Chain of Responsibility

### Code

```python
from abc import ABC, abstractmethod


class CanalNotification(ABC):
    def __init__(self):
        self.suivant = None

    def set_suivant(self, suivant):
        self.suivant = suivant
        return suivant

    @abstractmethod
    def envoyer(self, message, utilisateur):
        pass


class SMS(CanalNotification):
    def envoyer(self, message, utilisateur):
        print("Échec SMS")
        if self.suivant:
            self.suivant.envoyer(message, utilisateur)


class Push(CanalNotification):
    def envoyer(self, message, utilisateur):
        print("Échec Push")
        if self.suivant:
            self.suivant.envoyer(message, utilisateur)


class InApp(CanalNotification):
    def envoyer(self, message, utilisateur):
        print(f"Notification In-App envoyée à {utilisateur}")


sms = SMS()
push = Push()
inapp = InApp()

sms.set_suivant(push).set_suivant(inapp)

sms.envoyer("Bienvenue sur Sini !", "Alice")
```

---

# Version 3 — Observer

### Code

```python
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def notifier(self, message, utilisateur):
        pass


class Sujet:
    def __init__(self):
        self.observers = []

    def abonner(self, observer):
        self.observers.append(observer)

    def publier(self, message, utilisateur):
        for observer in self.observers:
            observer.notifier(message, utilisateur)


class SMSObserver(Observer):
    def notifier(self, message, utilisateur):
        print(f"SMS envoyé à {utilisateur}")


class PushObserver(Observer):
    def notifier(self, message, utilisateur):
        print(f"Push envoyé à {utilisateur}")


class InAppObserver(Observer):
    def notifier(self, message, utilisateur):
        print(f"Notification In-App envoyée à {utilisateur}")


notification = Sujet()

notification.abonner(SMSObserver())
notification.abonner(PushObserver())
notification.abonner(InAppObserver())

notification.publier("Bienvenue sur Sini !", "Alice")
```

---

# Comparaison des approches

| Pattern | Quand l'utiliser | Avantages | Inconvénients |
|----------|-----------------|-----------|---------------|
| **Strategy** | Lorsque l'on veut choisir un seul canal (SMS, Push ou In-App). | Code simple, facilement extensible, changement de stratégie à l'exécution. | Un seul canal est utilisé à la fois. |
| **Chain of Responsibility** | Lorsque plusieurs canaux sont essayés jusqu'à ce que l'un fonctionne. | Gestion automatique des échecs et des solutions de secours. | La chaîne peut devenir complexe si elle est longue. |
| **Observer** | Lorsque plusieurs canaux doivent être notifiés simultanément. | Très flexible, ajout ou suppression d'observateurs sans modifier le sujet. | Tous les observateurs sont exécutés, même si un seul aurait suffi. |

# Conclusion

- **Strategy** est le meilleur choix lorsqu'un seul canal de notification est utilisé selon le contexte.
- **Chain of Responsibility** est adaptée lorsqu'il faut prévoir un canal de secours en cas d'échec.
- **Observer** est idéale lorsqu'un même événement doit être diffusé à plusieurs canaux en parallèle.