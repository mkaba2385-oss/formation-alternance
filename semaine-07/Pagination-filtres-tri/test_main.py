from fastapi.testclient import TestClient

from main import app, tasks

client = TestClient(app)


def setup_function() -> None:
    tasks.clear()


def create_task(
    titre: str,
    description: str,
    priorite: int,
) -> int:
    response = client.post(
        "/tasks",
        json={
            "titre": titre,
            "description": description,
            "priorite": priorite,
        },
    )

    return response.json()["id"]



def test_pagination() -> None:
    for index in range(5):
        create_task(
            titre=f"Task {index}",
            description="Description",
            priorite=1,
        )

    response = client.get(
        "/tasks?limit=2&offset=0"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["next_offset"] == 2


def test_last_page_has_no_next_offset() -> None:
    for index in range(3):
        create_task(
            titre=f"Task {index}",
            description="Description",
            priorite=1,
        )

    response = client.get(
        "/tasks?limit=2&offset=2"
    )

    data = response.json()

    assert len(data["items"]) == 1
    assert data["total"] == 3
    assert data["next_offset"] is None


def test_invalid_limit() -> None:
    response = client.get(
        "/tasks?limit=0"
    )

    assert response.status_code == 422


def test_invalid_offset() -> None:
    response = client.get(
        "/tasks?offset=-1"
    )

    assert response.status_code == 422



def test_filter_by_priority() -> None:
    create_task(
        "Task priorité 1",
        "Description",
        1,
    )

    create_task(
        "Task priorité 3",
        "Description",
        3,
    )

    response = client.get(
        "/tasks?priorite=3"
    )

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["priorite"] == 3


def test_filter_by_completed() -> None:
    task_id = create_task(
        "Task terminée",
        "Description",
        1,
    )

    client.patch(
        f"/tasks/{task_id}",
        json={
            "terminee": True,
        },
    )

    create_task(
        "Task non terminée",
        "Description",
        1,
    )

    response = client.get(
        "/tasks?terminee=true"
    )

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["terminee"] is True



def test_search_in_title() -> None:
    create_task(
        "Apprendre FastAPI",
        "Cours Python",
        1,
    )

    create_task(
        "Faire les courses",
        "Acheter du pain",
        2,
    )

    response = client.get(
        "/tasks?q=fastapi"
    )

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["titre"] == (
        "Apprendre FastAPI"
    )


def test_search_in_description() -> None:
    create_task(
        "Cours Python",
        "Apprendre FastAPI aujourd'hui",
        1,
    )

    response = client.get(
        "/tasks?q=fastapi"
    )

    data = response.json()

    assert data["total"] == 1


def test_search_is_case_insensitive() -> None:
    create_task(
        "Apprendre FASTAPI",
        "Description",
        1,
    )

    response = client.get(
        "/tasks?q=fastapi"
    )

    data = response.json()

    assert data["total"] == 1




def test_sort_priority_ascending() -> None:
    create_task(
        "Priorité 3",
        "Description",
        3,
    )

    create_task(
        "Priorité 1",
        "Description",
        1,
    )

    response = client.get(
        "/tasks",
        params={"sort": "+priorite"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"][0]["priorite"] == 1
    assert data["items"][1]["priorite"] == 3


def test_sort_priority_descending() -> None:
    create_task(
        "Priorité 1",
        "Description",
        1,
    )

    create_task(
        "Priorité 3",
        "Description",
        3,
    )

    response = client.get(
        "/tasks",
        params={"sort": "-priorite"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"][0]["priorite"] == 3
    assert data["items"][1]["priorite"] == 1

def test_invalid_sort() -> None:
    response = client.get(
        "/tasks?sort=+unknown"
    )

    assert response.status_code == 422