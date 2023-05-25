from fastapi import APIRouter

router = APIRouter(
    prefix="/comment",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.put()
def add_comment_to_tweet():
    pass


@router.delete()
def remove_comment_from_tweet():
    pass
