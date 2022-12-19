from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import schema, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# Algorithm
# Expiration_time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def creat_access_token(data: dict):

    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiry})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def _verify_access_token(token: str, credintials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get('user_id')

        if not id:
            raise credintials_exception

        token_data = schema.TokenData(id=id)
    except JWTError as error:
        raise credintials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credintials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='could not validate credintials', headers={"WWW-Authenticate": "Bearer"})
    token_data = _verify_access_token(token, credintials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    return user