from fastapi import APIRouter

router = APIRouter(
    prefix="/follows",
    tags=["follows"],
    responses={404: {"description": "Not found"}},
)

""" List followers per user """
@router.get()
def list_followers():
    pass


""" List following per user """
@router.get()
def list_following():
    pass


""" Follow user """
@router.post()
def follow():
    pass


""" Unfollow user """
@router.delete()
def unfollow():
    pass