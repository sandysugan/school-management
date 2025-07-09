from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Allocation,AllocatedMember,ClassGroup
from app.schemas import AllocationSchema,AllocatedMemberSchema,ClassGroupSchema
from typing import List

#---------------------------CRUD fro allocations--------------------------------------#

def create_bulk_allocations(db: Session, allocations_data: List[AllocationSchema]):
    allocation_objs = []
    now = datetime.utcnow()
    for data in allocations_data:
        allocation = Allocation(
            academic_year_id=data.academic_year_id,
            class_id=data.class_id,
            section_id=data.section_id,
            group_id=data.group_id,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        allocation_objs.append(allocation)
    
    db.add_all(allocation_objs)
    db.commit()
    return allocation_objs


def get_all_allocations(db: Session):
    return db.query(Allocation).filter(Allocation.status == 1).all()

def get_allocation_by_id(db: Session, id: int):
    return db.query(Allocation).filter(Allocation.id == id).first()

def update_allocation(db: Session, id: int, data: AllocationSchema):
    db_obj = db.query(Allocation).filter(Allocation.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_allocation(db: Session, id: int, updated_by: int):
    db_obj = db.query(Allocation).filter(Allocation.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#-----------------------------------------------CRUD for allocated_members-------------------------------#


def create_allocated_member(db: Session, allocated_data: List[AllocatedMemberSchema]):
    allocated_member_obj=[]
    for data in allocated_data:
        db_obj = AllocatedMember(
        allocation_id=data.allocation_id,
        user_id=data.user_id,
        subject_id=data.subject_id,
        is_subject_teacher=data.is_subject_teacher,
        role=data.role,
        status=data.status,
        created_by=data.created_by,
        updated_by=data.updated_by,
        created_at=data.created_at,
        updated_at=data.updated_at,
    )
        allocated_member_obj.append(db_obj)
    db.add_all(allocated_member_obj)
    db.commit()
    for obj in allocated_member_obj:
        db.refresh(obj)
    return allocated_member_obj


def get_all_allocated_members(db: Session):
    return db.query(AllocatedMember).filter(AllocatedMember.status == 1).all()


def get_allocated_member_by_id(db: Session, id: int):
    return db.query(AllocatedMember).filter(AllocatedMember.id == id).first()


def update_allocated_member(db: Session, id: int, data: AllocatedMemberSchema):
    db_obj = db.query(AllocatedMember).filter(AllocatedMember.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj


def soft_delete_allocated_member(db: Session, id: int, updated_by: int):
    db_obj = db.query(AllocatedMember).filter(AllocatedMember.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#--------------------------------------CRUD for class_group--------------------------------------------------------#


def create_bulk_class_groups(db: Session, data: list[ClassGroupSchema]):
    now = datetime.utcnow()
    records = [
        ClassGroup(
            class_id=item.class_id,
            group_id=item.group_id,
            status=item.status,
            created_by=item.created_by,
            updated_by=item.updated_by,
            created_at=now,
            updated_at=now,
        )
        for item in data
    ]
    db.add_all(records)
    db.commit()
    return records

def get_all_class_groups(db: Session):
    return db.query(ClassGroup).filter(ClassGroup.status == 1).all()

def get_class_group_by_id(db: Session, id: int):
    return db.query(ClassGroup).filter(ClassGroup.id == id).first()

def update_class_group(db: Session, id: int, data: ClassGroupSchema):
    db_obj = db.query(ClassGroup).filter(ClassGroup.id == id).first()
    if not db_obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, key, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_class_group(db: Session, id: int, updated_by: int):
    db_obj = db.query(ClassGroup).filter(ClassGroup.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False