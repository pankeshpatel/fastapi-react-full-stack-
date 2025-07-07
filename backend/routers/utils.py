from fastapi import APIRouter

router = APIRouter(tags=["utils"])


@router.post("/utils/test-email/")
def test_email():
    return {"message": "test_email"}
