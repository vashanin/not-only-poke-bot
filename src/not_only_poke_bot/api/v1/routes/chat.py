from fastapi import APIRouter

from agents.controller import Controller

from ..schemas.chat import ChatRequest


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat(payload: ChatRequest):
    controller = Controller(
        answer_key="answer",
        answer_example="Pikachu has an electric-type advantage over Bulbasaur, so it would likely win."
    )

    return controller.chat(payload.question)
