from fastapi import FastAPI

from app.apps.decks.views import decks_router
from app.config import settings


def get_app() -> FastAPI:
    application = FastAPI(title=settings.SERVICE_NAME, debug=settings.DEBUG)
    application.include_router(decks_router, prefix="/api/decks")
    return application


app = get_app()
