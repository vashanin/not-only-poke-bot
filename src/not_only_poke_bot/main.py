from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_v1
from core.settings import settings


def create_app() -> FastAPI:
    _app = FastAPI(title=settings.app_name, debug=settings.debug)

    _app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(api_v1, prefix="/api/v1")

    return _app


app = create_app()
