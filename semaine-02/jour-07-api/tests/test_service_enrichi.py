from unittest.mock import MagicMock, patch
import pytest

# On importe les fonctions et la constante CACHE_DIR du script
from scripts.service_enrichi import (
    CACHE_DIR,
    fetch_all,
    get_quote,
    get_time,
    get_weather,
)


@pytest.fixture
def mock_apis():
    """Fixture Pytest qui mocke les appels HTTP vers les 3 APIs (Météo, Heure, Citation)."""

    def mock_httpx_get(url, *args, **kwargs):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None

        
        if "openweathermap.org" in url:
            mock_response.json.return_value = {
                "coord": {"lat": 48.8566, "lon": 2.3522},
                "sys": {"country": "FR"},
                "main": {"temp": 24.58, "humidity": 43},
                "weather": [{"description": "couvert"}],
            }

       
        elif "timeapi.io" in url:
            mock_response.json.return_value = {
                "time": "17:46:41",
                "date": "2026-07-23",
                "timeZone": "Europe/Paris",
            }


        elif "dummyjson.com" in url or "pensees.positives" in url:
            mock_response.json.return_value = {
                "quote": "La simplicité est la sophistication suprême.",
                "author": "Léonard de Vinci",
            }

        else:
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = Exception("URL non mockée")

        return mock_response

   
    with patch("scripts.service_enrichi.httpx.get", side_effect=mock_httpx_get) as _mock:
        yield _mock


# --- TESTS UNITAIRES ---


def test_get_weather_success(mock_apis, monkeypatch):
    """Vérifie le bon formatage de la météo quand la clé API est définie."""
    monkeypatch.setenv("OPENWATCHER_API_KEY", "fake_api_key_123")

    result = get_weather("paris")

    assert result["success"] is True
    assert result["data"]["city"] == "paris"
    assert result["data"]["temp"] == 24.58
    assert result["data"]["description"] == "couvert"


def test_get_time_success(mock_apis):
    """Vérifie la récupération de l'heure mockée avec des coordonnées."""
    result = get_time(48.8566, 2.3522)

    assert result["success"] is True
    assert result["data"]["time"] == "17:46:41"
    assert result["data"]["timeZone"] == "Europe/Paris"


def test_get_quote_success(mock_apis):
    """Vérifie la récupération de la citation mockée."""
    result = get_quote()

    assert result["success"] is True
    assert result["data"]["author"] == "Léonard de Vinci"


def test_fetch_all_complete(mock_apis, monkeypatch, tmp_path):
    """Vérifie l'agrégation des 3 APIs et la création du cache dans un dossier temporaire isolé."""
    monkeypatch.setenv("OPENWATCHER_API_KEY", "fake_api_key_123")
    
    
    fake_cache_dir = tmp_path / ".cache"
    monkeypatch.setattr("scripts.service_enrichi.CACHE_DIR", fake_cache_dir)

    data = fetch_all("paris")

   
    assert data["city"] == "paris"
    assert data["cached_response"] is False

   
    assert data["weather"]["success"] is True
    assert data["time"]["success"] is True
    assert data["quote"]["success"] is True

    
    assert (fake_cache_dir / "paris.json").exists()