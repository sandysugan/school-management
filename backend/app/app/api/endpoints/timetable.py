from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models import User
from app.schemas.timetable import TimeTableSchema, BulkTimeTableSchema
from app.crud import timetable_crud

router = APIRouter()

@router.post("/bulk_timetable_create")
def bulk_create_timetables(
    data: BulkTimeTableSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,6]:
         return {"status":0, "detail":"Unauthorized User"}

    for obj in data.timetables:
        obj.created_by = current_user.id
        obj.updated_by = current_user.id

    created = timetable_crud.create_bulk_timetables(db, data.timetables)
    return {
        "status": 1,
        "msg": f"{len(created)} timetables created successfully",
        "data": [t.id for t in created]
    }

@router.post("/list_timetables")
def list_timetables(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}

    records = timetable_crud.get_all_timetables(db)[skip: skip + limit]
    return records

@router.post("/get_timetable/{id}")
def get_timetable(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}

    timetable = timetable_crud.get_timetable_by_id(db, id)
    if not timetable or timetable.status != 1:
        return {"status":0,"detail":"Timetable not found"}

    return timetable

@router.post("/update_timetable/{id}")
def update_timetable(
    id: int,
    data: TimeTableSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated = timetable_crud.update_timetable(db, id, data)
    if not updated:
        return {"status":0,"detail":"Timetable not found"}

    return {
        "msg": "Timetable updated successfully",
        "id": updated.id
    }

@router.post("/delete_timetable/{id}")
def delete_timetable(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type !=1:
         return {"status":0, "detail":"Unauthorized User"}

    success = timetable_crud.soft_delete_timetable(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Timetable not found"}

    return {
        "status": 1,
        "msg": "Timetable deleted successfully"
    }
