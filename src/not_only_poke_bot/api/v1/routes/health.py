from fastapi import APIRouter


router = APIRouter(prefix="/-", tags=["meta"])


@router.get("/health")
async def health():
    return {"status": "ok"}
