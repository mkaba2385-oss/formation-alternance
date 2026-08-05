from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

# Configuration des logs pour suivre les tentatives et fallbacks
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SmsService")


# -------------------------------------------------------------------
# 1. Structures de données & Abstraction (DIP / ISP)
# -------------------------------------------------------------------

@dataclass(frozen=True)
class SmsResult:
    """Représente le résultat d'une tentative d'envoi."""
    success: bool
    provider_name: str
    error: str | None = None


class SmsChannel(ABC):
    """Interface unique pour tous les canaux d'envoi de SMS."""

    @abstractmethod
    def send(self, phone: str, message: str) -> SmsResult:
        """Envoie un SMS au numéro spécifié."""
        pass


# -------------------------------------------------------------------
# 2. Providers SMS (Concrétions SRP)
# -------------------------------------------------------------------

class AfricasTalkingProvider(SmsChannel):
    """Provider principal pour l'Afrique de l'Ouest (+223, etc.)."""

    def __init__(self, api_key: str, username: str, simulate_failure: bool = False):
        self.api_key = api_key
        self.username = username
        self.simulate_failure = simulate_failure

    def send(self, phone: str, message: str) -> SmsResult:
        if self.simulate_failure:
            return SmsResult(
                success=False,
                provider_name="Africa's Talking",
                error="HTTP 503: Gateway Unavailable"
            )
        # Simulation d'un appel réussi à l'API Africa's Talking
        return SmsResult(success=True, provider_name="Africa's Talking")


class TwilioProvider(SmsChannel):
    """Provider de secours / fallback international."""

    def __init__(self, account_sid: str, auth_token: str):
        self.account_sid = account_sid
        self.auth_token = auth_token

    def send(self, phone: str, message: str) -> SmsResult:
        # Simulation d'un appel réussi à l'API Twilio
        return SmsResult(success=True, provider_name="Twilio")


class MockSmsProvider(SmsChannel):
    """Provider factice pour le développement local et les tests unitaires."""

    def __init__(self, name: str = "MockProvider", should_fail: bool = False):
        self.name = name
        self.should_fail = should_fail
        self.sent_messages: list[tuple[str, str]] = []

    def send(self, phone: str, message: str) -> SmsResult:
        if self.should_fail:
            return SmsResult(
                success=False,
                provider_name=self.name,
                error="Mock Simulated Failure"
            )
        self.sent_messages.append((phone, message))
        return SmsResult(success=True, provider_name=self.name)


# -------------------------------------------------------------------
# 3. Service de Routage, Fallback et Logging (OCP / SRP)
# -------------------------------------------------------------------

class VersatileSmsService(SmsChannel):
    """Orchestrateur de routage, de fallback et de traçabilité des SMS."""

    def __init__(
        self,
        routes: dict[str, SmsChannel],
        default_channel: SmsChannel,
        fallback_channel: SmsChannel | None = None,
    ):
        self.routes = routes
        self.default_channel = default_channel
        self.fallback_channel = fallback_channel

    def _resolve_primary_channel(self, phone: str) -> SmsChannel:
        """Détermine le provider principal selon le préfixe du numéro."""
        for prefix, channel in self.routes.items():
            if phone.startswith(prefix):
                return channel
        return self.default_channel

    def send(self, phone: str, message: str) -> SmsResult:
        primary_channel = self._resolve_primary_channel(phone)

        # 1. Première tentative
        result = primary_channel.send(phone, message)
        logger.info(
            f"[SMS TENTATIVE] Destinataire: {phone} | Provider: {result.provider_name} | Succès: {result.success}"
        )

        # 2. Fallback si échec
        if not result.success and self.fallback_channel:
            logger.warning(
                f"[SMS FALLBACK] Échec du provider '{result.provider_name}' pour {phone}. Cause: {result.error}"
            )
            fallback_result = self.fallback_channel.send(phone, message)
            logger.info(
                f"[SMS TENTATIVE] Destinataire: {phone} | Provider: {fallback_result.provider_name} (Fallback) | Succès: {fallback_result.success}"
            )
            return fallback_result

        return result


# -------------------------------------------------------------------
# 4. Suite de Tests Unitaires (Exécution sans API distante)
# -------------------------------------------------------------------

def run_tests():
    print("\n=== DÉBUT DES TESTS UNITAIRES ===")

    # Setup des Mocks
    mock_at = MockSmsProvider(name="Mock Africa's Talking")
    mock_twilio = MockSmsProvider(name="Mock Twilio")
    mock_at_failing = MockSmsProvider(name="Mock Africa's Talking (Down)", should_fail=True)

    # 1. Test Routage +223 -> Africa's Talking
    service = VersatileSmsService(
        routes={"+223": mock_at},
        default_channel=mock_twilio,
        fallback_channel=mock_twilio
    )

    res_mali = service.send("+22370000000", "Alerte Sini: Pluie prévue")
    assert res_mali.success is True
    assert res_mali.provider_name == "Mock Africa's Talking"
    assert len(mock_at.sent_messages) == 1

    # 2. Test Routage Hors +223 (+33) -> Twilio par défaut
    res_france = service.send("+33612345678", "Bienvenue sur Sini")
    assert res_france.success is True
    assert res_france.provider_name == "Mock Twilio"
    assert len(mock_twilio.sent_messages) == 1

    # 3. Test Fallback automatique sur Twilio si Africa's Talking est Down
    service_failover = VersatileSmsService(
        routes={"+223": mock_at_failing},
        default_channel=mock_twilio,
        fallback_channel=mock_twilio
    )

    res_fallback = service_failover.send("+22379999999", "Alerte critique")
    assert res_fallback.success is True
    assert res_fallback.provider_name == "Mock Twilio"
    assert len(mock_twilio.sent_messages) == 2  # Le message s'est ajouté à Twilio

    print("=== TOUS LES TESTS SONT VALIDÉS AVEC SUCCÈS (3/3) ===\n")


if __name__ == "__main__":
    run_tests()