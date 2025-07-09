from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models import User,AllocatedMember
from app.schemas import AttendanceSchema, BulkAttendanceSchema,LeaveRequestSchema,StudentAttendanceFilterSchema
from app.crud import attendance_crud

router = APIRouter()

#------------------------------api for attendance--------------------------------------#

@router.post("/bulk_attendance_create")
def bulk_create_attendance(
    data: BulkAttendanceSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    for record in data.records:
        target_user = db.query(User).filter(User.id == record.user_id).first()
        if not target_user:
            return {"status": 0, "detail": f"User ID {record.user_id} not found"}

        if not attendance_crud.is_authorized(current_user, target_user.user_community_type):
            return {"status": 0, "detail": f"Unauthorized to mark user ID {record.user_id}"}
        
        record.created_by = current_user.id
        record.updated_by = current_user.id

    created = attendance_crud.create_bulk_attendance(db, data.records)
    return {
        "status": 1,
        "msg": f"{len(created)} attendance records created successfully",
        "data": [{"attendance_id":a.id,"marked_by":a.created_by} for a in created]
    }


@router.post("/view_attendance")
def list_attendance(
    filters: StudentAttendanceFilterSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    from_date = filters.from_date
    to_date = filters.to_date
    allocation_id = filters.allocation_id

    if current_user.user_community_type in [1, 2]:
        records = attendance_crud.get_attendance_filtered(
            db=db,
            allocation_id=allocation_id,
            from_date=from_date,
            to_date=to_date
        )

    elif current_user.user_community_type == 3:
        if not allocation_id:
            return {"status": 0, "detail": "allocation_id required for teachers"}

        allocation_check = db.query(AllocatedMember).filter(
            AllocatedMember.allocation_id == allocation_id,
            AllocatedMember.user_id == current_user.id
        ).first()

        if not allocation_check:
            return {"status": 0, "detail": "Unauthorized for this class"}

        records = attendance_crud.get_student_attendance(
            db=db,
            allocation_id=allocation_id,
            from_date=from_date,
            to_date=to_date)
    elif current_user.user_community_type == 4:
        records = attendance_crud.get_student_attendance(
            db=db,
            student_id=current_user.id,
            from_date=from_date,
            to_date=to_date
        )

    else:
        return {"status": 0, "detail": "Unauthorized User"}

    return {
        "status": 1,
        "count": len(records),
        "data": records
    }


@router.post("/get_attendance/{id}")
def get_attendance(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}

    record = attendance_crud.get_attendance_by_id(db, id)
    if not record:
        return {"status":0,"detail":"Attendance record not found"}

    return record

@router.post("/update_attendance/{id}")
def update_attendance(
    id: int,
    data: AttendanceSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    for record in data.records:
        target_user = db.query(User).filter(User.id == record.user_id).first()
        if not target_user:
            return {"status": 0, "detail": f"User ID {record.user_id} not found"}

        if not attendance_crud.is_authorized_to_mark(current_user, target_user.user_community_type):
            return {"status": 0, "detail": f"Unauthorized to mark user ID {record.user_id}"}

    data.updated_by = current_user.id
    updated = attendance_crud.update_attendance(db, id, data)
    if not updated:
        return {"status":0,"detail":"Attendance record not found"}

    return {
        "msg": "Attendance record updated successfully",
        "id": updated.id
    }

@router.post("/delete_attendance/{id}")
def delete_attendance(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    success = attendance_crud.delete_attendance(db, id)
    if not success:
        return {"status":0,"detail":"Attendance record not found"}

    return {
        "status": 1,
        "msg": "Attendance record deleted successfully"
    }

#----------------------------------api for leave request------------------------------------------------#


@router.post("/create")
def create_leave_request(
    data: LeaveRequestSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [3,4]:
         return {"status":0, "detail":"Unauthorized User"}
     
    data.created_by = current_user.id
    data.updated_by = current_user.id

    leave = attendance_crud.create_leave_request(db, data)
    return {
        "status": 1,
        "msg": "Leave request submitted successfully",
        "leave_id": leave.id
    }

@router.post("/list_leave_request")
def list_leave_requests(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}
     
    if current_user.user_community_type not in [1, 2]:
        return {"status":0,"detail":"Unauthorized"}
    
    records = attendance_crud.get_all_leave_requests(db)[skip: skip + limit]
    return records

@router.post("/get_leave_request/{id}")
def get_leave_request(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}
     
    record = attendance_crud.get_leave_request_by_id(db, id)
    if not record:
        return {"status":0,"detail":"Leave request not found"}
    return record

@router.post("/update_leave_request/{id}")
def update_leave_request(
    id: int,
    data: LeaveRequestSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}
     
    data.updated_by = current_user.id
    updated = attendance_crud.update_leave_request(db, id, data)
    if not updated:
        return {"status":0,"detail":"Leave request not found"}
    return {
        "msg": "Leave request updated successfully",
        "leave_id": updated.id
    }

@router.post("/delete_leave_request/{id}")
def delete_leave_request(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    success = attendance_crud.delete_leave_request(db, id)
    if not success:
        return {"status":0,"detail":"Leave request not found"}
    return {
        "status": 1,
        "msg": "Leave request deleted successfully"
    }