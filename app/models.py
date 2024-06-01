from .database import Base
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

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
    # one-to-many relationship - 1 user can have many posts (ForeignKey)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Additional - grab information of User from users table
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
