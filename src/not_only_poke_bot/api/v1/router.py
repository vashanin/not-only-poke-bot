from fastapi import APIRouter

from .routes import battle, chat, health

api_v1 = APIRouter()
api_v1.include_router(health.router)
api_v1.include_router(chat.router)
api_v1.include_router(battle.router)
