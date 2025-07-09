from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Period(Base):
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)  
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    timetables = relationship("TimeTable", back_populates="period")