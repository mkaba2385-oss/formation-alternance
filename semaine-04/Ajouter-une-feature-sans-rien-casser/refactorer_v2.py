# refactorer_v2.py

from abc import ABC, abstractmethod
import io
import torch
import psycopg2
import requests
from PIL import Image


# Nouvelles abstractions avec gestion de la confiance

class DiagnosticResult:
    """
    Nouveau objet résultat contenant :
    - la maladie détectée
    - le niveau de confiance
    """
    def __init__(self, maladie: int, confiance: float):
        self.maladie = maladie
        self.confiance = confiance


class DiagnosticModelV2(ABC):

    @abstractmethod
    def analyser(self, photo_bytes: bytes) -> DiagnosticResult:
        pass


# Nouvelle implémentation du modèle IA

class TorchDiagnosticModelV2(DiagnosticModelV2):

    def __init__(self):
        self.model = torch.load(
            "models/plant_disease.pt"
        )

    def analyser(self, photo_bytes: bytes) -> DiagnosticResult:

        img = Image.open(
            io.BytesIO(photo_bytes)
        )

        tensor = self._preprocess(img)

        with torch.no_grad():
            prediction = self.model(tensor)

        maladie = prediction.argmax().item()

        confiance = prediction.max().item()

        return DiagnosticResult(
            maladie,
            confiance
        )


# Réutilisation du repository existant

class TraitementRepository(ABC):

    @abstractmethod
    def recuperer_traitements(self, disease_id: int):
        pass


class PostgresTraitementRepository(
    TraitementRepository
):

    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            dbname="sini"
        )

    def recuperer_traitements(
        self,
        disease_id: int
    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT * FROM treatments
            WHERE disease_id = %s
            """,
            (disease_id,)
        )

        return cursor.fetchall()


# Notifications

class Notifier(ABC):

    @abstractmethod
    def notifier(
        self,
        user_id: int,
        maladie: int
    ):
        pass



class PushNotifier(Notifier):

    def notifier(
        self,
        user_id: int,
        maladie: int
    ):

        requests.post(
            "https://fcm.google.com/send",
            json={
                "user": user_id,
                "maladie": maladie
            }
        )



class ExpertNotifier(Notifier):
    """
    Nouvelle fonctionnalité :
    demande une validation humaine
    """

    def notifier(
        self,
        user_id: int,
        maladie: int
    ):

        print(
            f"Validation expert demandée "
            f"pour utilisateur {user_id}, "
            f"maladie {maladie}"
        )



class SmartNotifier:

    """
    Choisit automatiquement :
    - Push si confiance >= 50%
    - Expert sinon
    """

    def __init__(
        self,
        push_notifier: Notifier,
        expert_notifier: Notifier
    ):

        self.push_notifier = push_notifier
        self.expert_notifier = expert_notifier


    def notifier(
        self,
        user_id: int,
        resultat: DiagnosticResult
    ):

        if resultat.confiance >= 0.5:

            self.push_notifier.notifier(
                user_id,
                resultat.maladie
            )

        else:

            self.expert_notifier.notifier(
                user_id,
                resultat.maladie
            )


# Logger

class Logger(ABC):

    @abstractmethod
    def log(self, message: str):
        pass



class FileLogger(Logger):

    def log(
        self,
        message: str
    ):

        with open(
            "/var/log/sini.log",
            "a"
        ) as fichier:

            fichier.write(
                message + "\n"
            )

# Nouvel orchestrateur


class DiagnosticServiceV2:

    def __init__(
        self,
        model: DiagnosticModelV2,
        repository: TraitementRepository,
        notifier: SmartNotifier,
        logger: Logger
    ):

        self.model = model
        self.repository = repository
        self.notifier = notifier
        self.logger = logger


    def analyser(
        self,
        photo_bytes: bytes,
        user_id: int,
        culture: str
    ):

        resultat = self.model.analyser(
            photo_bytes
        )

        traitements = (
            self.repository
            .recuperer_traitements(
                resultat.maladie
            )
        )

        self.notifier.notifier(
            user_id,
            resultat
        )

        self.logger.log(
            f"{user_id}: "
            f"{resultat.maladie} "
            f"({resultat.confiance:.0%})"
        )

        return {
            "disease": resultat.maladie,
            "confidence": resultat.confiance,
            "treatments": traitements
        }


# Nouvelle composition de l'application

service = DiagnosticServiceV2(
    model=TorchDiagnosticModelV2(),

    repository=PostgresTraitementRepository(),

    notifier=SmartNotifier(
        push_notifier=PushNotifier(),
        expert_notifier=ExpertNotifier()
    ),

    logger=FileLogger()
)


resultat = service.analyser(
    photo_bytes=image,
    user_id=12,
    culture="maïs"
)


print(resultat)