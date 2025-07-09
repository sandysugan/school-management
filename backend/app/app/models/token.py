from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey,BLOB,TIMESTAMP,NVARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from app.db.base_class import Base


class Apitoken(Base):
    __tablename__ = 'api_token'
    id= Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    token = Column(String(255))
    created_at = Column(DateTime)
    status = Column(TINYINT)