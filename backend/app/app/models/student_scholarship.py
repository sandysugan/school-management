from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class StudentScholarship(Base):
    __tablename__ = "student_scholarships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    academic_year_id=Column(Integer,ForeignKey("academic_years.id"),nullable=False)
    scholarship_name = Column(String(100), nullable=False)
    discount_value = Column(Float, nullable=False)   

    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = relationship("User", back_populates="student_scholarships")
    student_fees = relationship("StudentFees", back_populates="scholarship")
 