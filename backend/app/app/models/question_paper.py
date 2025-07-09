# app/models/question_paper.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class QuestionPaper(Base):
    __tablename__ = "question_papers"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    allocation_id = Column(Integer, ForeignKey("allocations.id"), nullable=False)   
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)   
    file_path = Column(String(200), nullable=False)   
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


    exam = relationship("Exam")
    subject = relationship("Subject")
    teacher = relationship("User")
    allocation = relationship("Allocation")
