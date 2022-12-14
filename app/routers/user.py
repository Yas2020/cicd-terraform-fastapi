from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter(
    prefix='/users',
    tags=['Users'] ## Used for grouping routes in FastAPI documantation
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session=Depends(get_db)):
    ## Gash user password
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    ## Retrieve the new item and save it into 'new_post' to be returned
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def create_users(id: int, db: Session=Depends(get_db)):
    ## Hash user password
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist")
    
    return user