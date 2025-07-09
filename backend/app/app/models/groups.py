from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(100), nullable=False, unique=True)

    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    class_groups = relationship("ClassGroup", back_populates="group")
    subjects = relationship("Subject", back_populates="group")
    allocations = relationship("Allocation", back_populates="group")
    school_fees = relationship("SchoolFees", back_populates="group")
