from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Date,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class AcademicYear(Base):
    __tablename__ = "academic_years"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(String(20), nullable=False, unique=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False)

    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    allocations = relationship("Allocation", back_populates="academic_year")
    school_fees = relationship("SchoolFees", back_populates="academic_year")