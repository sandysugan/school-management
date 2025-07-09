from sqlalchemy.orm import Session
from datetime import datetime
from app.models import AcademicYear,Group,Class,Section,Subject
from app.schemas import AcademicYearSchema,GroupSchema,ClassSchema,SectionSchema,SubjectSchema
from typing import List

#------------------CRUD fro academics---------------------------------------------------------#

def create_academic_year(db: Session, data: AcademicYearSchema):
    db_obj = AcademicYear(
        year=data.year,
        start_date=data.start_date,
        end_date=data.end_date,
        is_current=data.is_current,
        status=data.status,
        created_by=data.created_by,
        created_at=datetime.utcnow(),
        updated_by=data.updated_by,
        updated_at=datetime.utcnow()
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_academic_years(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AcademicYear).offset(skip).limit(limit).all()


def get_academic_year_by_id(db: Session, id: int):
    return db.query(AcademicYear).filter(AcademicYear.id == id).first()


def update_academic_year(db: Session, id: int, data: AcademicYearSchema):
    db_obj = db.query(AcademicYear).filter(AcademicYear.id == id).first()
    if not db_obj:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)

    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj


def soft_delete_academic_year(db: Session, id: int, updated_by: int):
    db_obj = db.query(AcademicYear).filter(AcademicYear.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#-------------------------------------CRUD for groups-----------------------------------------------#

def create_group(db: Session, data: GroupSchema):
    db_obj = Group(
        group_name=data.group_name,
        status=data.status,
        created_by=data.created_by,
        updated_by=data.updated_by,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_all_groups(db: Session):
    return db.query(Group).filter(Group.status == 1).all()

def get_group_by_id(db: Session, id: int):
    return db.query(Group).filter(Group.id == id).first()

def update_group(db: Session, id: int, data: GroupSchema):
    db_obj = db.query(Group).filter(Group.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_group(db: Session, id: int, updated_by: int):
    db_obj = db.query(Group).filter(Group.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#----------------------------------CRUD for class-------------------------------------------#

def create_bulk_classes(db: Session, class_data: List[ClassSchema]):
    now = datetime.utcnow()
    class_objs = []
    for data in class_data:
        cls = Class(
            class_name=data.class_name,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        class_objs.append(cls)

    db.add_all(class_objs)
    db.commit()
    return class_objs

def get_all_classes(db: Session):
    return db.query(Class).filter(Class.status == 1).all()

def get_class_by_id(db: Session, id: int):
    return db.query(Class).filter(Class.id == id).first()

def update_class(db: Session, id: int, data: ClassSchema):
    db_obj = db.query(Class).filter(Class.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_class(db: Session, id: int, updated_by: int):
    db_obj = db.query(Class).filter(Class.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False
#---------------------------------CRUD for sections-------------------------------------------#

def create_bulk_sections(db: Session, section_data: List[SectionSchema]):
    now = datetime.utcnow()
    section_objs = []
    for data in section_data:
        section = Section(
            section_name=data.section_name,
            class_id=data.class_id,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        section_objs.append(section)

    db.add_all(section_objs)
    db.commit()
    return section_objs

def get_all_sections(db: Session):
    return db.query(Section).filter(Section.status == 1).all()

def get_section_by_id(db: Session, id: int):
    return db.query(Section).filter(Section.id == id).first()

def update_section(db: Session, id: int, data: SectionSchema):
    db_obj = db.query(Section).filter(Section.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_section(db: Session, id: int, updated_by: int):
    db_obj = db.query(Section).filter(Section.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False
 
 #--------------------------------------CRUD for subjects----------------------------------------------#
 
def create_bulk_subjects(db: Session, subjects_data: list[SubjectSchema]):
    now = datetime.utcnow()
    subject_objs = []

    for data in subjects_data:
        subject = Subject(
            subject_name=data.subject_name,
            subject_code=data.subject_code,
            group_id=data.group_id,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now,
        )
        subject_objs.append(subject)

    db.add_all(subject_objs)
    db.commit()
    return subject_objs

def get_all_subjects(db: Session):
    return db.query(Subject).filter(Subject.status == 1).all()

def get_subject_by_id(db: Session, id: int):
    return db.query(Subject).filter(Subject.id == id).first()

def update_subject(db: Session, id: int, data: SubjectSchema):
    db_obj = db.query(Subject).filter(Subject.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_subject(db: Session, id: int, updated_by: int):
    db_obj = db.query(Subject).filter(Subject.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False