from typing import List,Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime,date
from app.models import Attendance,LeaveRequest,User,Allocation
from app.schemas import AttendanceSchema,LeaveRequestSchema,AttendanceReportResponse,AttendanceReportRecord

#---------------------------------CRUD for attendance-----------------------------------------#
def is_authorized_bulk(current_user: User, target_user: User, db: Session, allocation_id: int):
    
    if current_user.user_community_type == 2 and target_user.user_community_type == 3:
        return True
 
    if current_user.user_community_type == 3 and target_user.user_community_type == 4:
        allocated = db.query(Allocation).filter(
            Allocation.id == allocation_id,
            Allocation.allocated_members.any(user_id=current_user.id)
        ).first()
        return allocated is not None

    return False


def create_bulk_attendance(db: Session, records_data: list[AttendanceSchema]):
    now = datetime.utcnow()
    attendance_objs = []

    for data in records_data:
        existing=db.query(Attendance).filter(
            Attendance.user_id==data.user_id,
            Attendance.date==data.date
        ).first()
        if existing:
            continue
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

def get_attendance_report(
    db: Session,
    current_user: User,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    user_id: Optional[int] = None,
    allocation_id: Optional[int] = None
):
    query = db.query(Attendance, User).join(User, User.id == Attendance.user_id)

    # ---------------------- Filter by Role ---------------------- #
    if current_user.user_community_type == 3:  # Class Teacher
        if allocation_id:
            allocation = db.query(Allocation).filter(
                Allocation.id == allocation_id,
                Allocation.allocated_members.any(user_id=current_user.id)
            ).first()
            if not allocation:
                return {
                    "status": 0,
                    "detail": "Access denied: allocation not assigned to you"
                }
            query = query.filter(Attendance.allocation_id == allocation_id)
            query = query.filter(User.user_community_type == 4)  # students only

        elif user_id:
            if user_id != current_user.id:
                return {
                    "status": 0,
                    "detail": "Access denied: cannot view other users"
                }
            query = query.filter(Attendance.user_id == current_user.id)

        else:
            query = query.filter(Attendance.user_id == current_user.id)

    elif current_user.user_community_type in [2, 4]:  # Teacher or Student
        query = query.filter(Attendance.user_id == current_user.id)

    elif current_user.user_community_type in [1, 5]:  # Admin or Principal
        if user_id:
            query = query.filter(Attendance.user_id == user_id)
        if allocation_id:
            query = query.filter(Attendance.allocation_id == allocation_id)

    else:
        return {"status": 0, "detail": "Unauthorized user type"}

    # ---------------------- Date Filters ---------------------- #
    if from_date:
        query = query.filter(Attendance.date >= from_date)
    if to_date:
        query = query.filter(Attendance.date <= to_date)

    results = query.all()

    # ---------------------- Calculate Summary ---------------------- #
    total_days = len(results)
    present = sum(1 for a, _ in results if a.status.lower() == "present")
    absent = sum(1 for a, _ in results if a.status.lower() == "absent")
    half_day = sum(1 for a, _ in results if a.status.lower() == "half day")
    percentage = round(((present + 0.5 * half_day) / total_days) * 100, 2) if total_days else 0

    records = []
    for a, u in results:
        records.append({
            "user_id": u.id,
            "name": u.first_name + " " + (u.last_name or ""),
            "date": str(a.date),
            "status": a.status
        })

    return {
        "status": 1,
        "total_days": total_days,
        "present": present,
        "absent": absent,
        "half_day": half_day,
        "percentage": percentage,
        "records": records
    }

def update_attendance(
    db: Session,
    current_user: User,
    attendance_id: int,
    new_status: str
):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()

    if not attendance:
        return {"status": 0, "detail": "Attendance record not found"}

    if current_user.user_community_type == 3:   
        is_allowed = db.query(Allocation).filter(
            Allocation.id == attendance.allocation_id,
            Allocation.allocated_members.any(user_id=current_user.id)
        ).first()
        if not is_allowed:
            return {"status": 0, "detail": "Not authorized to update this record"}

    elif current_user.user_community_type in [2, 4]:   
        if attendance.user_id != current_user.id:
            return {"status": 0, "detail": "Cannot update others' attendance"}
 
    attendance.status = new_status
    attendance.updated_by = current_user.id
    db.commit()
    db.refresh(attendance)

    return {
        "status": 1,
        "msg": "Attendance updated successfully",
        "attendance_id": attendance.id,
        "new_status": attendance.status
    }

def delete_attendance(db: Session, id: int):
    db_obj = db.query(Attendance).filter(Attendance.id == id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False

#------------------------------------------CRUD for leave request--------------------------------------------------#

def create_leave_request(db: Session, current_user: User, data: dict):
    if current_user.user_community_type not in [3, 4]:   
        return {"status": 0, "detail": "Only teachers and students can request leave"}

    leave = LeaveRequest(
        user_id=current_user.id,
        allocation_id=data["allocation_id"],
        reason=data.get("reason"),
        from_date=data["from_date"],
        to_date=data["to_date"],
        status="Pending",
        created_by=current_user.id,
        updated_by=current_user.id
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)

    return {"status": 1, "msg": "Leave request submitted", "leave_id": leave.id}


def update_leave_status(db: Session, current_user: User, leave_id: int, status: str):
    if current_user.user_community_type != 1:  
        return {"status": 0, "detail": "Only principal can approve or reject leave"}

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        return {"status": 0, "detail": "Leave request not found"}

    leave.status = status
    leave.updated_by = current_user.id
    leave.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(leave)

    return {"status": 1, "msg": f"Leave {status.lower()} successfully", "leave_id": leave.id}


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
