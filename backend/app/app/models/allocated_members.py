from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base 

class AllocatedMember(Base):
    __tablename__ = "allocated_members"

    id = Column(Integer, primary_key=True, index=True)
    allocation_id = Column(Integer, ForeignKey("allocations.id"), nullable=False)   
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)  
    is_subject_teacher=Column(Integer,default=0)
    role=Column(String(30),nullable=False)

    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="allocated_members")
    allocation = relationship("Allocation", back_populates="allocated_members")
    subject = relationship("Subject", back_populates="allocated_members")