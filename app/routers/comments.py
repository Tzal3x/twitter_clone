from fastapi import APIRouter, status, Depends, Body, HTTPException, Response
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import exc
from app.models import Comments
from app.schemas import CommentCreate, CommentReturn, UserReturn
from app.database import get_db
from app.security import authorize_user

router = APIRouter(
    prefix="/comment",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.post('/{tweet_id}', status_code=status.HTTP_201_CREATED, response_model=CommentReturn)
def add_comment_to_tweet(
    tweet_id: int,
    comment: Annotated[CommentCreate, Body],
    current_user: Annotated[UserReturn, Depends(authorize_user)],
    db: Session = Depends(get_db)):
    
    new_comment = Comments(tweet_id=tweet_id, user_id=current_user.id, **comment.dict())
    try:
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tweet with id: {tweet_id} does not exist")
    except exc.DataError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Character limit exceeded")
    
    return new_comment


@router.put('/{comment_id}', response_model=CommentReturn)
def update_comment_to_tweet(
    comment_id: int,
    updated_comment: Annotated[CommentCreate, Body],
    current_user: Annotated[UserReturn, Depends(authorize_user)],
    db: Session = Depends(get_db)):
    
    comment_query = db.query(Comments).filter(Comments.id == comment_id)

    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id: {comment_id} does not exist")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    comment_query.update(updated_comment.dict(), synchronize_session=False)
    db.commit()
    return comment_query.first()


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_comment_from_tweet(comment_id: int,
                              current_user: Annotated[UserReturn, Depends(authorize_user)],
                              db: Annotated[Session, Depends(get_db)]):
    
    comment_query = db.query(Comments).filter(Comments.id == comment_id)

    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with id: {id} does not exist")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
