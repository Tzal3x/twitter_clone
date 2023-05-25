from fastapi import APIRouter

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
    responses={404: {"description": "Not found"}},
)

""" Likes on tweets """
@router.put()
def add_like_to_tweet():
    pass

@router.delete()
def remove_like_from_tweet():
    pass


""" Likes on comments """
@router.put()
def add_like_to_comment():
    pass

@router.delete()
def remove_like_from_comment():
    pass
