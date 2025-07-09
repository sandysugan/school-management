from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class StudentFees(Base):
    __tablename__ = "student_fees"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scl_fee_id = Column(Integer, ForeignKey("school_fees.id"), nullable=False)
    scholarship_id = Column(Integer, ForeignKey("student_scholarships.id"), nullable=True)
    paid_amount = Column(Integer, nullable=False, default=0)
    due_date = Column(DateTime, nullable=True)
    payment_mode = Column(String(50), nullable=True)  
    payment_date = Column(DateTime, nullable=True)
    receipt_no = Column(String(100), nullable=True, unique=True)

    status = Column(String(20), default="pending")  # pending / paid / partial / overdue
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = relationship("User", back_populates="student_fees")
    school_fee = relationship("SchoolFees", back_populates="student_fees")
    scholarship = relationship("StudentScholarship", back_populates="student_fees")
