from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(120), unique=True, index=True)
    phone_number = Column(String(20))
    user_community_type = Column(Integer) #1-Admin,2-Principal,3-Teacher,4-Student,5-Accountant,6-Librarian
    password = Column(String(255), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    dob = Column(Date)  
    address = Column(String(255))
    profile_image = Column(String(255))  
    guardian_name = Column(String(100))  
    roll_number = Column(String(20), nullable=True)
    status = Column(Integer, default=1)  
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    marks = relationship("Marks", back_populates="student")
    allocated_members = relationship("AllocatedMember", back_populates="user")
    student_fees = relationship("StudentFees", back_populates="student")
    student_transport = relationship("StudentTransport", back_populates="student")
    leave_requests = relationship("LeaveRequest", back_populates="user")
    exam_results = relationship("ExamResult", back_populates="student")
    student_scholarships = relationship("StudentScholarship", back_populates="student")
    timetables = relationship("TimeTable", back_populates="teacher")
    attendance_records = relationship("Attendance", back_populates="user")
    book_issues = relationship("BookIssue", back_populates="student")
    otps = relationship("OTP", back_populates="user")