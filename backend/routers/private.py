from fastapi import APIRouter

router = APIRouter(tags=["private"])


@router.post("/private/users/")
def create_user():
    return {"message": "create_user"}
