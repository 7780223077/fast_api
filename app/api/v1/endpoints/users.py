from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.dependencies.database import get_db
from app.models.user import User
import app.utils.password_encoder as password_encoder
from app.utils import jwtservice

router = APIRouter()

#FOR USERS
@router.post("/user", response_model=schemas.UserOut)
async def create_user(user: schemas.UserBase, session:Session = Depends(get_db)):
    #hash the password
    user.password = password_encoder.hash(user.password)
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user



@router.get("/user", response_model=schemas.UserOut)
async def get_user_details(session: Session = Depends(get_db), current_user: User = Depends(jwtservice.get_current_user)):
    return current_user



@router.get("/user/{id}", response_model=schemas.UserOut)
async def get_user_by_id(id: int, session: Session= Depends(get_db)):
    user = session.query(User).filter(User.id == id).first()
    return user