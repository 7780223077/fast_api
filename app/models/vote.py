from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import mapped_column
from app.dependencies.database import Base

class Vote(Base):
    __tablename__ = "votes"
    user_id = mapped_column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = mapped_column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)