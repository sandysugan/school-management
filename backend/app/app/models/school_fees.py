from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class SchoolFees(Base):
    __tablename__ = "school_fees"

    id = Column(Integer, primary_key=True, index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    fee_type = Column(String(50), nullable=False)  # e.g., Tuition, Transport, Hostel
    amount = Column(Integer, nullable=False)

    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    academic_year = relationship("AcademicYear", back_populates="school_fees")
    class_ = relationship("Class", back_populates="school_fees")
    group = relationship("Group", back_populates="school_fees")
    student_fees = relationship("StudentFees", back_populates="school_fee")