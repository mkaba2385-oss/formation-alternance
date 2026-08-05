from abc import ABC, abstractmethod
import io
import torch
import psycopg2
import requests
from PIL import Image


# ==========================
# Abstractions
# ==========================

class DiagnosticModel(ABC):
    @abstractmethod
    def analyser(self, photo_bytes: bytes) -> int:
        pass


class TraitementRepository(ABC):
    @abstractmethod
    def recuperer_traitements(self, disease_id: int):
        pass


class Notifier(ABC):
    @abstractmethod
    def notifier(self, user_id: int, maladie: int):
        pass


class Logger(ABC):
    @abstractmethod
    def log(self, message: str):
        pass


# ==========================
# Implémentations
# ==========================

class TorchDiagnosticModel(DiagnosticModel):
    def __init__(self):
        self.model = torch.load("models/plant_disease.pt")

    def analyser(self, photo_bytes: bytes) -> int:
        img = Image.open(io.BytesIO(photo_bytes))

        # Prétraitement de l'image
        tensor = self._preprocess(img)

        # Inférence
        with torch.no_grad():
            prediction = self.model(tensor)

        return prediction[0]


class PostgresTraitementRepository(TraitementRepository):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            dbname="sini"
        )

    def recuperer_traitements(self, disease_id: int):
        cursor = self.db.cursor()

        cursor.execute(
            "SELECT * FROM treatments WHERE disease_id = %s",
            (disease_id,)
        )

        return cursor.fetchall()


class PushNotifier(Notifier):
    def notifier(self, user_id: int, maladie: int):
        requests.post(
            "https://fcm.google.com/send",
            json={}
        )


class FileLogger(Logger):
    def log(self, message: str):
        with open("/var/log/sini.log", "a") as fichier:
            fichier.write(message + "\n")


# ==========================
# Orchestrateur
# ==========================

class DiagnosticService:
    def __init__(
        self,
        model: DiagnosticModel,
        repository: TraitementRepository,
        notifier: Notifier,
        logger: Logger,
    ):
        self.model = model
        self.repository = repository
        self.notifier = notifier
        self.logger = logger

    def analyser(self, photo_bytes: bytes, user_id: int, culture: str):

        maladie = self.model.analyser(photo_bytes)

        traitements = self.repository.recuperer_traitements(maladie)

        self.notifier.notifier(user_id, maladie)

        self.logger.log(f"{user_id}: {maladie}")

        return {
            "disease": maladie,
            "treatments": traitements,
        }


# ==========================
# Utilisation
# ==========================

service = DiagnosticService(
    model=TorchDiagnosticModel(),
    repository=PostgresTraitementRepository(),
    notifier=PushNotifier(),
    logger=FileLogger(),
)

resultat = service.analyser(
    photo_bytes=image,
    user_id=12,
    culture="maïs",
)

print(resultat)