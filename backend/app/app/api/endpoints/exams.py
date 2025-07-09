from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models import User
from app.schemas import ExamSchema, BulkExamSchema,MarksSchema,BulkMarksSchema,ExamResultSchema,BulkExamResultSchema
from app.crud import exam_crud

router = APIRouter()

#-----------------------------------api for exam-----------------------------------------------#

@router.post("/bulk_exam_create")
def bulk_create_exams(
    data: BulkExamSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    for exam in data.exams:
        exam.created_by = current_user.id
        exam.updated_by = current_user.id

    created_exams = exam_crud.create_bulk_exams(db, data.exams)
    result = [
        {
            "id": e.id,
            "exam_name": e.exam_name,
            "exam_code": e.exam_code,
            "allocation_id": e.allocation_id
        }
        for e in created_exams
    ]
    return {
        "status": 1,
        "msg": f"{len(result)} exams created successfully",
        "data": result
    }

@router.post("/list_exams")
def list_exams(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
        return {"status":0,"detail":"Unauthorized"}

    exams = exam_crud.get_all_exams(db)[skip: skip + limit]
    return [
        {
            "id": e.id,
            "exam_name": e.exam_name,
            "exam_code": e.exam_code,
            "allocation_id": e.allocation_id,
            "start_date": e.start_date,
            "end_date": e.end_date
        }
        for e in exams
    ]

@router.post("/get_exam/{id}")
def get_exam(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}

    exam = exam_crud.get_exam_by_id(db, id)
    if not exam or exam.status != 1:
        return {"status":0,"detail":"Exam not found"}

    return {
        "id": exam.id,
        "allocation_id": exam.allocation_id,
        "exam_name": exam.exam_name,
        "exam_code": exam.exam_code,
        "total_marks": exam.total_marks,
        "start_date": exam.start_date,
        "end_date": exam.end_date,
        "status": exam.status
    }

@router.post("/update_exam/{id}")
def update_exam( 
    id: int,
    data: ExamSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated = exam_crud.update_exam(db, id, data)
    if not updated:
        return {"status":0,"detail":"Exam not found"}

    return {
        "msg": "Exam updated successfully",
        "id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete_exam/{id}")
def delete_exam(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    success = exam_crud.soft_delete_exam(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Exam not found"}

    return {
        "status": 1,
        "msg": "Exam deleted successfully"
    }

#--------------------------------------api for marks--------------------------------------------------#


@router.post("/bulk_marks_create")
def bulk_create_marks(
    data: BulkMarksSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type!=3:
         return {"status":0, "detail":"Unauthorized User"}

    for mark in data.marks:
        mark.created_by = current_user.id
        mark.updated_by = current_user.id

    created_marks = exam_crud.create_bulk_marks(db, data.marks)
    return {
        "status": 1,
        "msg": f"{len(created_marks)} marks created successfully",
        "data": [m.id for m in created_marks]
    }

@router.post("/list_marks")
def list_marks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}

    marks = exam_crud.get_all_marks(db)[skip: skip + limit]
    return [
        {
            "id": m.id,
            "student_id": m.student_id,
            "exam_id": m.exam_id,
            "subject_id": m.subject_id,
            "obtained_marks": m.obtained_marks
        }
        for m in marks
    ]

@router.post("/get_mark/{id}")
def get_mark(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}

    mark = exam_crud.get_mark_by_id(db, id)
    if not mark or mark.status != 1:
        return {"status":0,"detail":"Marks not found"}

    return {
        "id": mark.id,
        "student_id": mark.student_id,
        "exam_id": mark.exam_id,
        "subject_id": mark.subject_id,
        "obtained_marks": mark.obtained_marks
    }

@router.post("/update_mark/{id}")
def update_mark(
    id: int,
    data: MarksSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type!=3:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated = exam_crud.update_mark(db, id, data)
    if not updated:
        return {"status":0,"detail":"Marks not found"}

    return {
        "msg": "Mark updated successfully",
        "id": updated.id
    }

@router.post("/delete_mark/{id}")
def delete_mark(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type!=1:
         return {"status":0, "detail":"Unauthorized User"}

    success = exam_crud.soft_delete_mark(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Marks not found"}

    return {
        "status": 1,
        "msg": "Mark deleted successfully"
    }
    
#---------------------------------------api for exam_result------------------------------------------------------#

@router.post("/bulk_exam_result_create")
def bulk_create_exam_results(
    data: BulkExamResultSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}

    for result in data.results:
        result.created_by = current_user.id
        result.updated_by = current_user.id

    created = exam_crud.create_bulk_exam_results(db, data.results)
    return {
        "status": 1,
        "msg": f"{len(created)} exam results created successfully",
        "data": [r.id for r in created]
    }

@router.post("/list_exam_results")
def list_exam_results(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}

    results = exam_crud.get_all_exam_results(db)[skip: skip + limit]
    return results

@router.post("/get_exam_result/{id}")
def get_exam_result(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1, 2, 3]:
        return {"status": 0, "detail": "Unauthorized User"}
    
    if current_user.user_community_type in [1,2,3]:
        results = exam_crud.get_results_by_class_teacher(db, id)
        if not results:
            return {"status": 0, "detail": "Result not found"}

        return {
            "status": 1,
            "results": [
                {
                    "exam_id": r.exam_id,
                    "student_id": r.student_id,
                    "allocation_id": r.allocation_id,
                    "total_obtained": r.total_obtained,
                    "status": r.status
                }
                for r in results
            ]
        }
@router.post("/get_student_exam_result/{id}")
def get_student_exam_result(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):

    if current_user.user_community_type in [1,2,3,4]:
        result=exam_crud.get_exam_result_by_student(db,id)
    return result

@router.post("/update_exam_result/{id}")
def update_exam_result(
    id: int,
    data: ExamResultSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated = exam_crud.update_exam_result(db, id, data)
    if not updated:
        return {"status":0,"detail":"Result not found"}

    return {
        "msg": "Exam result updated successfully",
        "id": updated.id
    }

@router.post("/delete_exam_result/{id}")
def delete_exam_result(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    success = exam_crud.delete_exam_result(db, id)
    if not success:
        return {"status":0,"detail":"Result not found"}

    return {
        "status": 1,
        "msg": "Exam result deleted successfully"
    }