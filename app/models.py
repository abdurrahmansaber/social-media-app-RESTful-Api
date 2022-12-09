from .database import Base

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, server_default='True', nullable=False)
    create_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    rating = Column(Integer, nullable=True, server_default='0') 