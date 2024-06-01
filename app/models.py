from .database import Base
from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


# SQLAlchemy Models
# Referring to Database Models Schema

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    rating = Column(Integer, nullable=True, server_default='0')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

