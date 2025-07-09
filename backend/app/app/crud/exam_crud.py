from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Exam,Marks,ExamResult,QuestionPaper,AllocatedMember,Allocation,User
from app.schemas import ExamSchema,MarksSchema,ExamResultSchema,QuestionPaperSchema

#-----------------------------------CRUD for exams---------------------------------------------------------#

def create_bulk_exams(db: Session, exam_data: list[ExamSchema]):
    now = datetime.utcnow()
    exam_objs = []

    for data in exam_data:
        exam = Exam(
            allocation_id=data.allocation_id,
            exam_name=data.exam_name,
            exam_code=data.exam_code,
            total_marks=data.total_marks,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        exam_objs.append(exam)

    db.add_all(exam_objs)
    db.commit()
    return exam_objs

def get_all_exams(db: Session):
    return db.query(Exam).filter(Exam.status == 1).all()

def get_exam_by_id(db: Session, id: int):
    return db.query(Exam).filter(Exam.id == id).first()

def update_exam(db: Session, id: int, data: ExamSchema):
    db_obj = db.query(Exam).filter(Exam.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_exam(db: Session, id: int, updated_by: int):
    db_obj = db.query(Exam).filter(Exam.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#------------------------------------------CRUD for marks-----------------------------------------------------#

def create_bulk_marks(db: Session, marks_data: list[MarksSchema]):
    now = datetime.utcnow()
    marks_objs = []

    for data in marks_data:
        mark = Marks(
            student_id=data.student_id,
            exam_id=data.exam_id,
            subject_id=data.subject_id,
            obtained_marks=data.obtained_marks,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        marks_objs.append(mark)

    db.add_all(marks_objs)
    db.commit()
    return marks_objs

def get_all_marks(db: Session):
    return db.query(Marks).filter(Marks.status == 1).all()

def get_mark_by_id(db: Session, id: int):
    return db.query(Marks).filter(Marks.id == id).first()

def update_mark(db: Session, id: int, data: MarksSchema):
    db_obj = db.query(Marks).filter(Marks.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def soft_delete_mark(db: Session, id: int, updated_by: int):
    db_obj = db.query(Marks).filter(Marks.id == id).first()
    if db_obj:
        db_obj.status = -1
        db_obj.updated_by = updated_by
        db_obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False

#--------------------------------------CRUD for exam_result-------------------------------------------#

def create_bulk_exam_results(db: Session, results_data: list[ExamResultSchema]):
    now = datetime.utcnow()
    result_objs = []

    for data in results_data:
        result = ExamResult(
            student_id=data.student_id,
            exam_id=data.exam_id,
            allocation_id=data.allocation_id,
            total_obtained=data.total_obtained,
            status=data.status,
            created_by=data.created_by,
            updated_by=data.updated_by,
            created_at=now,
            updated_at=now
        )
        result_objs.append(result)

    db.add_all(result_objs)
    db.commit()
    return result_objs

def get_all_exam_results(db: Session):
    return db.query(ExamResult).all()

def get_exam_result_by_student(db: Session, id: int):
    return db.query(ExamResult).filter(ExamResult.student_id == id).first()

def get_results_by_class_teacher(db: Session, teacher_id: int):
    allocation_ids = (
        db.query(AllocatedMember.allocation_id)
        .filter(
            AllocatedMember.user_id == teacher_id,
            AllocatedMember.role == "class_teacher"
        )
        .all()
    )

    allocation_ids = [row[0] for row in allocation_ids]
    if not allocation_ids:
        return []

    results = (
        db.query(ExamResult)
        .join(User, ExamResult.student_id == User.id)
        .join(Exam, ExamResult.exam_id == Exam.id)
        .filter(ExamResult.allocation_id.in_(allocation_ids))
        .order_by(ExamResult.student_id)
        .all()
    )

    return results


def update_exam_result(db: Session, id: int, data: ExamResultSchema):
    db_obj = db.query(ExamResult).filter(ExamResult.id == id).first()
    if not db_obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_exam_result(db: Session, id: int):
    db_obj = db.query(ExamResult).filter(ExamResult.id == id).first()
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False

#------------------------------------CRUD for question paper-----------------------------------------------------------#

def create_bulk_question_papers(db: Session, data: list[QuestionPaperSchema]):
    now = datetime.utcnow()
    objs = [
        QuestionPaper(
            exam_id=item.exam_id,
            allocation_id=item.allocation_id,
            subject_id=item.subject_id,
            uploaded_by=item.uploaded_by,
            file_path=item.file_path,
            status=item.status,
            created_at=now,
            updated_at=now
        ) for item in data
    ]
    db.add_all(objs)
    db.commit()
    return objs

def get_all_question_papers(db: Session):
    return db.query(QuestionPaper).filter(QuestionPaper.status == 1).all()

def get_question_paper_by_id(db: Session, id: int):
    return db.query(QuestionPaper).filter(QuestionPaper.id == id).first()

def update_question_paper(db: Session, id: int, data: QuestionPaperSchema):
    obj = db.query(QuestionPaper).filter(QuestionPaper.id == id).first()
    if not obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    obj.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(obj)
    return obj

def soft_delete_question_paper(db: Session, id: int, updated_by: int):
    obj = db.query(QuestionPaper).filter(QuestionPaper.id == id).first()
    if obj:
        obj.status = -1
        obj.updated_at = datetime.utcnow()
        db.commit()
        return True
    return False