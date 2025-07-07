from fastapi import APIRouter

router = APIRouter(tags=["users"])


@router.get("/users")
def read_users():
    return {"message": "read_users"}


@router.post("/users")
def create_user():
    return {"message": "create_users"}


@router.patch("/users/me")
def update_user_me():
    return {"message": "update_user_me"}


@router.patch("/users/me/password")
def update_password_me():
    return {"message": "update_password_me"}


@router.get("/users/me")
def read_user_me():
    return {"message": "read_user_me"}


@router.delete("/users/me")
def delete_user_me():
    return {"message": "delete_user_me"}


@router.post("/users/signup")
def register_user():
    return {"message": "register_user"}


@router.get("/users/{user_id}")
def read_user_by_id():
    return {"message": "read_user_by_id"}


@router.patch("/users/{user_id}")
def update_user():
    return {"message": "update_user"}


@router.delete("/users/{user_id}")
def delete_user():
    return {"message": "delete_user"}
