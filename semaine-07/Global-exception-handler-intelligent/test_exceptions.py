from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_not_found_error():
    response = client.get("/users/404")

    assert response.status_code == 404

    assert response.json() == {
        "error_code": "NOT_FOUND",
        "message": "Utilisateur introuvable",
        "details": {
            "user_id": 404,
        },
    }


def test_conflict_error():
    response = client.get("/users/409")

    assert response.status_code == 409

    assert response.json() == {
        "error_code": "CONFLICT",
        "message": "Cet utilisateur existe déjà",
        "details": {
            "user_id": 409,
        },
    }


def test_validation_error():
    response = client.get("/users/422")

    assert response.status_code == 422

    assert response.json() == {
        "error_code": "VALIDATION_ERROR",
        "message": "Données utilisateur invalides",
        "details": {
            "field": "user_id",
        },
    }


def test_internal_server_error_hides_technical_details():
    response = client.get(
        "/users/500",
        raise_server_exceptions=False,
    )

    assert response.status_code == 500

    assert response.json() == {
        "error_code": "INTERNAL_SERVER_ERROR",
        "message": "Une erreur interne est survenue.",
        "details": None,
    }

    assert "Erreur technique secrète" not in response.text