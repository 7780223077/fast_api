from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.utils import password_encoder, jwtservice
from app.models.user import User
from app import schemas

router = APIRouter()

@router.post("/login")
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db),
):
    user = db_session.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    if not password_encoder.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    jwt_token = jwtservice.create_access_token(data={"user_id": user.id})
    return schemas.Token(access_token=jwt_token, token_type="bearer")

