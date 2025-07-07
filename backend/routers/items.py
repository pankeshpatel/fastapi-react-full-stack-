from fastapi import APIRouter

router = APIRouter(tags=["items"])


@router.get("/items")
def read_items():
    return {"message": "read items"}


# add query string parameters
@router.get("/items/{id}")
def read_item():
    return {"message": "read an item by id"}


@router.post("/items")
def create_item():
    return {"message": "create an item"}


@router.put("/items/{id}")
def update_item():
    return {"message": "update an item by id"}


@router.delete("/items/{id}")
def delete_item():
    return {"message": "delete an item by id"}
