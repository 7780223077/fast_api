from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from app import schemas
from app.dependencies import database
from app.models.user import User
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm.strip('"')
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # print(f"ALGORITHM: {ALGORITHM}")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def verify_access_token(token: str, credentials_exception : HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # payload is dict
        id = payload.get("user_id")
        # email = payload.get("user_email")
        if id is None : #or email is None
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except InvalidTokenError as e:
        print(f"InvalidTokenError : {e}")
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials",
            headers= {"WWW-Authenticate":"Bearer"}
        )
    user_data = verify_access_token(token, credentials_exception)
    user = session.query(User).filter(User.id == user_data.id).first()
    if not user:
        raise credentials_exception
    
    return user
