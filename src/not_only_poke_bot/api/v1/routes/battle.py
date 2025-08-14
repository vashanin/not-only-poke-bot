from fastapi import APIRouter, Query

from agents.controller import Controller

from ..schemas.battle import BattleResponse


router = APIRouter(prefix="/battle", tags=["battle"])


@router.get("", response_model=BattleResponse)
async def battle(pokemon1: str = Query(...), pokemon2: str = Query(...)):
    controller = Controller(answer_key="winner", answer_example="Pikachu")

    return controller.battle(pokemon1, pokemon2)
