from fastapi import APIRouter

router = APIRouter(
    prefix="/login",
    tags=["login"]
    )


@router.get("/token")
def login():
    pass  
