from typing import List, Optional

from bson import ObjectId
from pymongo.collection import Collection

from app.db import database
from app.pydantic import Base, PyObjectId
from pydantic import Field


class DeckBase(Base):
    name: str
    description: str = ""


class DeckCreate(DeckBase):
    pass


class Deck(DeckBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class Decks(Base):
    items: List[Deck]


class DeckManager:
    collection: Collection = database.get_collection("decks")

    @classmethod
    async def retrieve(cls, object_id: str) -> Optional[Deck]:
        deck = await cls.collection.find_one({"_id": ObjectId(object_id)})
        if deck:
            return Deck.parse_obj(deck)
        return None

    @classmethod
    async def list(cls) -> Decks:
        items = await cls.collection.find().to_list(None)
        return Decks.parse_obj({"items": items})

    @classmethod
    async def add(cls, deck: DeckCreate) -> Deck:
        result = await cls.collection.insert_one(deck.dict())
        new_deck = await cls.collection.find_one({"_id": result.inserted_id})
        return Deck.parse_obj(new_deck)

    @classmethod
    async def update(cls, object_id: str, deck: DeckCreate) -> Optional[Deck]:
        result = await cls.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": deck.dict()}
        )
        if result.modified_count > 0:
            deck = await cls.collection.find_one({"_id": ObjectId(object_id)})
            return Deck.parse_obj(deck)
        return None

    @classmethod
    async def delete(cls, object_id: str) -> bool:
        result = await cls.collection.delete_one({"_id": ObjectId(object_id)})
        return result.deleted_count > 0


class CardBase(Base):
    front: str
    back: Optional[str] = None
    hint: Optional[str] = None


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: str
    deck_id: str


class Cards(Base):
    items: List[Card]
