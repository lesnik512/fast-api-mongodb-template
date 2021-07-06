import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.apps.decks import models
from tests.decks.conftest import get_deck_data


def test_get_decks_empty(client: TestClient):
    response = client.get("/api/decks/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["items"]) == 0


def test_get_decks(client: TestClient, deck: models.Deck):
    response = client.get("/api/decks/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) == 1
    for k, v in data["items"][0].items():
        if k == "_id":
            assert v == str(deck.id)
            continue
        assert v == getattr(deck, k)


def test_get_deck(client: TestClient, deck: models.Deck):
    response = client.get(f"/api/decks/{deck.id}")
    assert response.status_code == status.HTTP_200_OK
    for k, v in response.json().items():
        if k == "_id":
            assert v == str(deck.id)
            continue
        assert v == getattr(deck, k)


@pytest.mark.parametrize(
    "name,description",
    [
        ("test deck", None),
        ("test deck", "test deck description"),
    ],
)
def test_post_decks(
    client: TestClient,
    name: str,
    description: str,
):
    data = {"name": name, "description": description}
    response = client.post("/api/decks/", json=data)
    assert response.status_code == status.HTTP_200_OK

    item_id = response.json()["_id"]
    response = client.get(f"/api/decks/{item_id}/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    for k, v in data.items():
        assert v == response_data.get(k)


def test_post_decks_empty_fields(client: TestClient):
    response = client.post(
        "/api/decks/",
        json={"name": None, "description": None},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed",
            }
        ]
    }


@pytest.mark.parametrize(
    "name,description",
    [
        ("test deck updated", None),
        (
            get_deck_data()["name"],
            "test deck description updated",
        ),
        (
            "test deck updated",
            "test deck description updated",
        ),
    ],
)
def test_put_decks(
    client: TestClient,
    deck: models.Deck,
    name: str,
    description: str,
):
    data = {"name": name, "description": description}
    response = client.put(f"/api/decks/{deck.id}/", json=data)
    assert response.status_code == status.HTTP_200_OK

    item_id = response.json()["_id"]
    response = client.get(f"/api/decks/{item_id}/")
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    for k, v in data.items():
        assert v == response_data.get(k)


def test_put_decks_empty_fields(client: TestClient, deck: models.Deck):
    data = {"name": None, "description": None}
    response = client.put(f"/api/decks/{deck.id}/", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed",
            }
        ]
    }


def test_delete_deck(client: TestClient, deck: models.Deck):
    response = client.delete(f"/api/decks/{deck.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    response = client.get(f"/api/decks/{deck.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.delete(f"/api/decks/{deck.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Deck is not found"}


def test_delete_deck_wrong_object_id(client: TestClient):
    response = client.delete("/api/decks/0/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "deck_id"],
                "msg": "Invalid ObjectId",
                "type": "value_error",
            }
        ]
    }
