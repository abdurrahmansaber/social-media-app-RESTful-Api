from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, utils,schema
from ..database import get_db
from .. import oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=schema.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Username or Password")

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Username or Password")

    token = oauth2.creat_access_token(data={"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}


