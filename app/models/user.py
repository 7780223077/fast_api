from app.dependencies.database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from typing import List
from .post import Post

class User(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email:Mapped[str]= mapped_column(String, nullable=False, unique=True, index=True)
    password:Mapped[str] = mapped_column(String, nullable=False, index=True)
    created_at:Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    posts : Mapped[List["Post"]] = relationship()


    
