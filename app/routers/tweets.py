from fastapi import APIRouter

router = APIRouter(
    prefix="/tweets",
    tags=["tweets"],
    responses={404: {"description": "Not found"}},
)


@router.get()
def get_tweet():
    pass  


@router.post()
def create_tweet():
    pass


@router.put()
def update_tweet():
    pass


@router.delete()
def delete_tweet():
    pass
