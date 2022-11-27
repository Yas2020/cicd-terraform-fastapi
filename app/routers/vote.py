from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix='/vote',
    tags=['Vote'] ## Used For grouping routes in FastAPI documantation
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    ## Check if the post exists
    post_query = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post {vote.post_id} does not exist')

    vote_query = db.query(models.Vote).filter(models.Vote.user_id==current_user.id, models.Vote.post_id==vote.post_id)
    found_vote = vote_query.first()
    if vote.dir == 1: 
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        else:
            new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            return {"message": "successfully added vote"}
    elif found_vote:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
    
    # new_user = models.Vote(**vote.dict())
    # db.add(new_user)
    # db.commit()
    # # retrieve the new item and save it into 'new_post' to be returned
    # db.refresh(new_user)

    # return new_user