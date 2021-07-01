from fastapi import APIRouter, HTTPException, status
from starlette.responses import Response

from app.apps.decks import models


decks_router = APIRouter()


@decks_router.get("/decks/", response_model=models.Decks)
async def list_decks() -> models.Decks:
    return await models.DeckManager.list()


@decks_router.get("/decks/{deck_id}/", response_model=models.Deck)
async def get_deck(deck_id: str) -> models.Deck:
    instance = await models.DeckManager.retrieve(deck_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Deck is not found")
    return instance


@decks_router.put("/decks/{deck_id}/", response_model=models.DeckCreate)
async def update_deck(deck_id: str, data: models.DeckCreate) -> models.Deck:
    instance = await models.DeckManager.update(deck_id, data)
    if not instance:
        raise HTTPException(status_code=404, detail="Deck is not found")
    return instance


@decks_router.post("/decks/", response_model=models.Deck)
async def create_deck(data: models.DeckCreate) -> models.Deck:
    return await models.DeckManager.add(data)


@decks_router.delete(
    "/decks/{deck_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_deck(deck_id: str) -> Response:
    is_deleted = await models.DeckManager.delete(deck_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Deck is not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
