from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String(100), nullable=False)
    subject_code=Column(String(20), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)

    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    marks = relationship("Marks", back_populates="subject")
    ebooks = relationship("EBook", back_populates="subject")
    allocated_members = relationship("AllocatedMember", back_populates="subject")
    timetables = relationship("TimeTable", back_populates="subject")
    group = relationship("Group", back_populates="subjects")

 