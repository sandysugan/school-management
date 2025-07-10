from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Date
from sqlalchemy.orm import relationship
from datetime import date,datetime
from app.db.base_class import Base

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    allocation_id = Column(Integer, ForeignKey("allocations.id"), nullable=False) 
    reason = Column(String(255), nullable=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    status = Column(String(20), default="Pending") 
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="leave_requests")
    allocation = relationship("Allocation", back_populates="leave_requests")