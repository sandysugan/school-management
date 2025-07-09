from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Date,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # student,teacher
    allocation_id = Column(Integer, ForeignKey("allocations.id"), nullable=False)  
    date = Column(Date, nullable=False)
    status = Column(String(10), nullable=False)  # Present, Absent, Half day
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="attendance_records") 
    allocation = relationship("Allocation", back_populates="attendance_records")