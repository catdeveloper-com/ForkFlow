from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    """Вернуть состояние доступности процесса сервиса."""
    return {"status": "ok", "service": "auth"}
