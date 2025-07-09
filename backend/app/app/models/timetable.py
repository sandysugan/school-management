from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class TimeTable(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    allocation_id = Column(Integer, ForeignKey("allocations.id"), nullable=False)   
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.id"), nullable=False)  
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False) 
    
    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    allocation = relationship("Allocation", back_populates="timetables")
    subject = relationship("Subject", back_populates="timetables")
    teacher = relationship("User", back_populates="timetables")
    period = relationship("Period", back_populates="timetables")
    day = relationship("Day", back_populates="timetables")