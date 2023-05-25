from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get()
def get_user_info():
    pass  


@router.post()
def register_user():
    pass


@router.put()
def update_user_info():
    pass


@router.delete()
def delete_user_account():
    pass

