from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)  # Only for 11th, 12th

    status = Column(Integer, default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    academic_year = relationship("AcademicYear", back_populates="allocations")
    class_ = relationship("Class", back_populates="allocations")
    section = relationship("Section", back_populates="allocations")
    group = relationship("Group", back_populates="allocations")

    allocated_members = relationship("AllocatedMember", back_populates="allocation")
    exams = relationship("Exam", back_populates="allocation")
    exam_results = relationship("ExamResult", back_populates="allocation")
    timetables = relationship("TimeTable", back_populates="allocation")
    attendance_records = relationship("Attendance", back_populates="allocation")
    leave_requests = relationship("LeaveRequest", back_populates="allocation")
