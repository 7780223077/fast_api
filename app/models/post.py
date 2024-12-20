from app.dependencies.database import Base
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
# from .user import User

class Post(Base):
    __tablename__ = 'posts'

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String, nullable=False, index=True)
    content:Mapped[str] = mapped_column(String, nullable=False, index=True)
    published:Mapped[bool] = mapped_column(Boolean, server_default='TRUE', nullable=False)
    created_at:Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # user: Mapped[User] = relationship("User")