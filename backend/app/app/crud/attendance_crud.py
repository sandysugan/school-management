from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime,date
from app.models import Attendance,LeaveRequest,User,Allocation
from app.schemas import AttendanceSchema,LeaveRequestSchema 

#---------------------------------CRUD for attendance-----------------------------------------#

def is_authorized(current_user: User, target_user_type: int):

    if current_user.user_community_type == 2 and target_user_type == 3:
        return True
    if current_user.user_community_type == 3 and target_user_type == 4:
        return True
    return False


def create_bulk_attendance(db: Session, records_data: list[AttendanceSchema]):
    now = datetime.utcnow()
    attendance_objs = []

    for data in records_data:
        record = Attendance(
            user_id=data.user_id,
            allocation_id=data.allocation_id,
            date=data.date,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        attendance_objs.append(record)

    db.add_all(attendance_objs)
    db.commit()
    return attendance_objs

def get_all_attendance(db: Session):
    return db.query(Attendance).all()

def get_attendance_by_id(db: Session, id: int):
    return db.query(Attendance).filter(Attendance.id == id).first()

def get_student_attendance(
    db: Session,
    student_id: int | None = None,
    allocation_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None):
 
    q = (
        db.query(Attendance).join(User).filter(User.user_community_type == 4)    
    )

    if student_id:
        q = q.filter(Attendance.user_id == student_id)

    if allocation_id:
        q = q.filter(Attendance.allocation_id == allocation_id)

    if from_date and to_date:
        q = q.filter(Attendance.date.between(from_date, to_date))

    return q.all()


def update_attendance(db: Session, id: int, data: AttendanceSchema):
    db_obj = db.query(Attendance).filter(Attendance.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_attendance(db: Session, id: int):
    db_obj = db.query(Attendance).filter(Attendance.id == id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False

#------------------------------------------CRUD for leave request--------------------------------------------------#


def create_leave_request(db: Session, data: LeaveRequestSchema):
    now = datetime.utcnow()
    leave = LeaveRequest(
        user_id=data.user_id,
        allocation_id=data.allocation_id,
        reason=data.reason,
        from_date=data.from_date,
        to_date=data.to_date,
        status=data.status,
        created_by=data.created_by,
        updated_by=data.updated_by,
        created_at=now,
        updated_at=now
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave

def get_all_leave_requests(db: Session):
    return db.query(LeaveRequest).all()

def get_leave_request_by_id(db: Session, id: int):
    return db.query(LeaveRequest).filter(LeaveRequest.id == id).first()

def update_leave_request(db: Session, id: int, data: LeaveRequestSchema):
    db_obj = db.query(LeaveRequest).filter(LeaveRequest.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_leave_request(db: Session, id: int):
    db_obj = db.query(LeaveRequest).filter(LeaveRequest.id == id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False
