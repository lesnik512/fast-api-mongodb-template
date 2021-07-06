import pytest

from app.apps.decks import models


@pytest.fixture
async def deck(event_loop):
    deck_data = models.DeckCreate(**get_deck_data())
    deck = await models.DeckManager.add(deck_data)
    yield deck
    await models.DeckManager.delete(str(deck.id))


def get_deck_data():
    return {"name": "test deck", "description": "test deck description"}
