from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base 

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100))
    publisher = Column(String(100))
    quantity = Column(Integer, default=1)  # total copies
    available = Column(Integer, default=1)  # available for issue

    status = Column(String(20), default="available")  # available / unavailable / damaged
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    book_issues = relationship("BookIssue", back_populates="book")