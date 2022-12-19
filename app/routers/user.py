from ..schema import UserCreate, UserResponse
from .. import models, utils
from ..database import get_db

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # hash password before saving
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

    return user
