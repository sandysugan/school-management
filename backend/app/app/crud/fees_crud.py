from sqlalchemy.orm import Session
from datetime import datetime
from app.models import StudentFees,StudentScholarship,SchoolFees
from app.schemas import StudentFeesSchema,StudentScholarshipSchema,SchoolFeesSchema

#----------------------------------CRUD for student_scholarship-----------------------------------------#

def create_bulk_scholarships(db: Session, scholarship_data: list[StudentScholarshipSchema]):
    now = datetime.utcnow()
    scholarship_objs = []

    for data in scholarship_data:
        scholarship = StudentScholarship(
            user_id=data.user_id,
            academic_year_id=data.academic_year_id,
            scholarship_name=data.scholarship_name,
            discount_value=data.discount_value,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        scholarship_objs.append(scholarship)

    db.add_all(scholarship_objs)
    db.commit()
    return scholarship_objs

def get_all_scholarships(db: Session):
    return db.query(StudentScholarship).filter(StudentScholarship.status == 1).all()

def get_scholarship_by_id(db: Session, id: int):
    return db.query(StudentScholarship).filter(StudentScholarship.id == id).first()

def update_scholarship(db: Session, id: int, data: StudentScholarshipSchema):
    db_obj = db.query(StudentScholarship).filter(StudentScholarship.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_scholarship(db: Session, id: int, updated_by: int):
    db_obj = db.query(StudentScholarship).filter(StudentScholarship.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#---------------------------------CRUD for school_fees-------------------------------------------#

def create_bulk_school_fees(db: Session, fees_data: list[SchoolFeesSchema]):
    now = datetime.utcnow()
    fee_objs = []

    for data in fees_data:
        fee = SchoolFees(
            academic_year_id=data.academic_year_id,
            class_id=data.class_id,
            group_id=data.group_id,
            fee_type=data.fee_type,
            amount=data.amount,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        fee_objs.append(fee)

    db.add_all(fee_objs)
    db.commit()
    return fee_objs

def get_all_school_fees(db: Session):
    return db.query(SchoolFees).filter(SchoolFees.status == 1).all()

def get_school_fee_by_id(db: Session, id: int):
    return db.query(SchoolFees).filter(SchoolFees.id == id).first()

def update_school_fee(db: Session, id: int, data: SchoolFeesSchema):
    db_obj = db.query(SchoolFees).filter(SchoolFees.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_school_fee(db: Session, id: int, updated_by: int):
    db_obj = db.query(SchoolFees).filter(SchoolFees.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#----------------------------------CRUD for student_fees-----------------------------------------#

def create_bulk_student_fees(db: Session, fees_data: list[StudentFeesSchema]):
    now = datetime.utcnow()
    fee_objs = []

    for data in fees_data:
        fee = StudentFees(
            student_id=data.student_id,
            scl_fee_id=data.scl_fee_id,
            scholarship_id=data.scholarship_id,
            paid_amount=data.paid_amount,
            due_date=data.due_date,
            payment_mode=data.payment_mode,
            payment_date=data.payment_date,
            receipt_no=data.receipt_no,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        fee_objs.append(fee)

    db.add_all(fee_objs)
    db.commit()
    return fee_objs

def get_all_student_fees(db: Session):
    return db.query(StudentFees).filter(StudentFees.status != "deleted").all()

def get_student_fee_by_id(db: Session, id: int):
    return db.query(StudentFees).filter(StudentFees.id == id).first()

def update_student_fee(db: Session, id: int, data: StudentFeesSchema):
    db_obj = db.query(StudentFees).filter(StudentFees.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_student_fee(db: Session, id: int, updated_by: int):
    db_obj = db.query(StudentFees).filter(StudentFees.id == id).first()
    if db_obj:
        db_obj.status = "deleted"
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False