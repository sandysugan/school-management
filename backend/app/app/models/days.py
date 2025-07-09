from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)   
    
    timetables = relationship("TimeTable", back_populates="day")
