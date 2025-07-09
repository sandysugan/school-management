from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class StudentTransport(Base):
    __tablename__ = "student_transport"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    pickup_point = Column(String(100))
    drop_point = Column(String(100))

    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
    student = relationship("User", back_populates="student_transport")
    bus = relationship("Bus", back_populates="students")
