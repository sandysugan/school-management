from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Date,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String(20), nullable=False, unique=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    driver = relationship("Driver", back_populates="buses")
    students = relationship("StudentTransport", back_populates="bus")
