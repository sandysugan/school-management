from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base 

class BookIssue(Base):
    __tablename__ = "book_issues"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    issue_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="issued")  # issued / returned / overdue / lost

    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    book = relationship("Book", back_populates="book_issues")
    student = relationship("User", back_populates="book_issues")