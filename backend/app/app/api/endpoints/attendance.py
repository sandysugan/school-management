from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from app.api import deps
from app.models import User
from app.schemas import AttendanceSchema, BulkAttendanceSchema,LeaveRequestSchema,AttendanceReportResponse
from app.crud import attendance_crud
from typing import List,Optional
from datetime import date

router = APIRouter()

#------------------------------api for attendance--------------------------------------#

@router.post("/bulk_attendance_create")
def bulk_create_attendance(
    data: BulkAttendanceSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
): 
    if current_user.user_community_type not in [2, 3]:
        return {"status": 0, "detail": "Unauthorized user"}

    validated_records = []

    for record in data.records:
        target_user = db.query(User).filter(User.id == record.user_id).first()
        if not target_user:
            return {"status": 0, "detail": f"User ID {record.user_id} not found"}

        if not attendance_crud.is_authorized_bulk(current_user, target_user, db, record.allocation_id):
            return {"status": 0, "detail": f"Not allowed to mark attendance for user ID {record.user_id}"}

        record.created_by = current_user.id
        record.updated_by = current_user.id
        validated_records.append(record)

    created = attendance_crud.create_bulk_attendance(db, validated_records)

    return {
        "status": 1,
        "msg": f"{len(created)} attendance records created successfully",
        "data": [{"attendance_id": a.id, "marked_by": a.created_by} for a in created]
    }
#-----------------------------------------------------------------------------------------------------------------------

@router.post("/report")
def attendance_report(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    user_id: Optional[int] = Query(None),
    allocation_id: Optional[int] = Query(None)
):
    return attendance_crud.get_attendance_report(
        db=db,
        current_user=current_user,
        from_date=from_date,
        to_date=to_date,
        user_id=user_id,
        allocation_id=allocation_id
    )
#------------------------------------------------------------------------------------------------------------------------


@router.post("/update")
def update_attendance_record(
    attendance_id: int,
    status: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return attendance_crud.update_attendance(
        db=db,
        current_user=current_user,
        attendance_id=attendance_id,
        new_status=status
    )

#----------------------------------api for leave request------------------------------------------------#


@router.post("/request")
def request_leave(
    allocation_id: int,
    from_date: date,
    to_date: date,
    reason: str = "",
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    data = {
        "allocation_id": allocation_id,
        "from_date": from_date,
        "to_date": to_date,
        "reason": reason
    }
    return attendance_crud.create_leave_request(db, current_user, data)


@router.post("/approve_or_reject")
def approve_or_reject_leave(
    leave_id: int,
    status: str,   
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if status not in ["Approved", "Rejected"]:
        return {"status": 0, "detail": "Status must be 'Approved' or 'Rejected'"}

    return attendance_crud.update_leave_status(db, current_user, leave_id, status)


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