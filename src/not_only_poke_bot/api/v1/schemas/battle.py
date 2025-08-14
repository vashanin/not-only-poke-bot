from pydantic import BaseModel


class BattleResponse(BaseModel):
    reasoning: str
    winner: str
