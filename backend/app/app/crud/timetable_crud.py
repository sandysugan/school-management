from sqlalchemy.orm import Session
from datetime import datetime
from app.models import TimeTable
from app.schemas import TimeTableSchema

def create_bulk_timetables(db: Session, timetable_data: list[TimeTableSchema]):
    now = datetime.utcnow()
    timetable_objs = []

    for data in timetable_data:
        obj = TimeTable(
            allocation_id=data.allocation_id,
            subject_id=data.subject_id,
            teacher_id=data.teacher_id,
            period_id=data.period_id,
            day_id=data.day_id,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        timetable_objs.append(obj)

    db.add_all(timetable_objs)
    db.commit()
    return timetable_objs

def get_all_timetables(db: Session):
    return db.query(TimeTable).filter(TimeTable.status == 1).all()

def get_timetable_by_id(db: Session, id: int):
    return db.query(TimeTable).filter(TimeTable.id == id).first()

def update_timetable(db: Session, id: int, data: TimeTableSchema):
    db_obj = db.query(TimeTable).filter(TimeTable.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_timetable(db: Session, id: int, updated_by: int):
    db_obj = db.query(TimeTable).filter(TimeTable.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False