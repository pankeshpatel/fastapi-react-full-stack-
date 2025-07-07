from fastapi import APIRouter

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_access_token():
    return {"message": "login_access_token"}


@router.post("/login/test-token")
def test_token():
    return {"message": "test token"}


@router.post("/password-recovery/{email}")
def recover_password():
    return {"message": "recover_password"}


@router.post("/reset-password/")
def reset_password():
    return {"message": "reset_password"}


@router.post("/password-recovery-html-content/{email}")
def recover_password_html_content():
    return {"message": "recover_password_html_content"}
