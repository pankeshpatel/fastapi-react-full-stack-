from fastapi import APIRouter

router = APIRouter(prefix="/utils", tags=["utils"])


@router.post("/utils/test-email/")
def test_email():
    return {"message": "test_email"}


@router.get("/health-check/")
async def health_check() -> bool:
    return True
