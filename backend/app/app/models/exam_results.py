from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class ExamResult(Base):
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    allocation_id = Column(Integer, ForeignKey("allocations.id"), nullable=False)   
    total_obtained = Column(Integer, nullable=False)
    status = Column(String(20)) #pending,published,reviewed
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = relationship("User", back_populates="exam_results")
    exam = relationship("Exam", back_populates="exam_results")
    allocation = relationship("Allocation", back_populates="exam_results")
    