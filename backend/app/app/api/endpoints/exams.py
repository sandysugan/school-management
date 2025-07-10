import datetime
from fastapi import APIRouter, Depends, File, Form,UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.api import deps
from app.models import User,AllocatedMember,QuestionPaper,Allocation,ExamResult
from app.schemas import ExamSchema, BulkExamSchema,MarksSchema,BulkMarksSchema,ExamResultSchema,BulkExamResultSchema
from app.crud import exam_crud
from app.utils import file_storage
from datetime import datetime

router=APIRouter()

#-----------------------------------api for exam-----------------------------------------------#

@router.post("/bulk_exam_create")
def bulk_create_exams(
    data: BulkExamSchema,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    for exam in data.exams:
        exam.created_by=current_user.id
        exam.updated_by=current_user.id

    created_exams=exam_crud.create_bulk_exams(db, data.exams)
    result=[
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
    skip: int=0,
    limit: int=10,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type in [1, 2]: 
        exams=exam_crud.get_exams_by_allocation_ids(db)[skip: skip + limit]

    elif current_user.user_community_type in [3, 4]:  
        allocation_ids=[
            a.id for a in current_user.allocated_members
        ]   

        if not allocation_ids:
            return {"status": 0, "detail": "No class allocations found"}

        exams=exam_crud.get_exams_by_allocation_ids(db, allocation_ids)[skip: skip + limit]

    else:
        return {"status": 0, "detail": "Unauthorized"}

    return {
        "status": 1,
        "data": [
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
    }

@router.post("/get_exam/{id}")
def get_exam(
    id: int,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    exam=exam_crud.get_exam_by_id(db, id)
    if not exam or exam.status != 1:
        return {"status": 0, "detail": "Exam not found"}


    if current_user.user_community_type not in [1,2]:
        allocation_ids=[a.id for a in current_user.allocated_members]
        if exam.allocation_id not in allocation_ids:
            return {"status": 0, "detail": "Not authorized to view this exam"}
    else:
        return {"status": 0, "detail": "Unauthorized"}

    return {
        "status": 1,
        "data": {
            "id": exam.id,
            "allocation_id": exam.allocation_id,
            "exam_name": exam.exam_name,
            "exam_code": exam.exam_code,
            "total_marks": exam.total_marks,
            "start_date": exam.start_date,
            "end_date": exam.end_date,
            "status": exam.status
        }
    }

@router.post("/update_exam/{id}")
def update_exam( 
    id: int,
    data: ExamSchema,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by=current_user.id
    updated=exam_crud.update_exam(db, id, data)
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
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    success=exam_crud.soft_delete_exam(db, id, current_user.id)
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
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type!=3:
         return {"status":0, "detail":"Unauthorized User"}

    for mark in data.marks:
        allocated=db.query(AllocatedMember).filter(
            AllocatedMember.user_id == current_user.id,
            AllocatedMember.allocation_id == mark.allocation_id,
            AllocatedMember.subject_id == mark.subject_id,
            AllocatedMember.role == "subject_teacher"
        ).first()
        if not allocated:
            return {"status":0, "detail":f"Unauthorized to mark subject {mark.subject_id} in allocation {mark.allocation_id}"}

        mark.created_by=current_user.id
        mark.updated_by=current_user.id


    created_marks=exam_crud.create_bulk_marks(db, data.marks)
    return {
        "status": 1,
        "msg": f"{len(created_marks)} marks created successfully",
        "data": [m.id for m in created_marks]
    }

@router.post("/list_marks")
def list_marks(
    skip: int=0,
    limit: int=10,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}

    marks=exam_crud.get_all_marks(db)[skip: skip + limit]
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
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}

    mark=exam_crud.get_mark_by_id(db, id)
    if not mark or mark.status != 1:
        return {"status":0,"detail":"Marks not found"}

    return {
        "id": mark.id,
        "student_id": mark.student_id,
        "exam_id": mark.exam_id,
        "subject_id": mark.subject_id,
        "obtained_marks": mark.obtained_marks
    }
    

@router.post("/student/{student_id}/marksheet")
def student_marksheet(
    student_id: int,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
 
    if current_user.user_community_type == 4 and current_user.id != student_id:
        return {"status":0, "detail":"Access denied"}
 
    if current_user.user_community_type not in [1, 2, 3, 4]:
        return {"status":0, "detail":"Unauthorized User"}

    return exam_crud.generate_student_marksheet(student_id, db)

@router.post("/progresscard/class/{class_id}/section/{section_id}")
def progress_report_excel(
    class_id: int,
    section_id: int,
    exam_name: str,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    return exam_crud.generate_class_progress_excel(
        class_id=class_id,
        section_id=section_id,
        exam_name=exam_name,
        current_user=current_user,
        db=db
    )


@router.post("/update_mark/{id}")
def update_mark(
    id: int,
    data: MarksSchema,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type!=3:
         return {"status":0, "detail":"Unauthorized User"}

    existing=exam_crud.get_mark_by_id(db, id)
    if not existing:
        return {"status_code":0,"detail":"Mark not found"}

    allocated=db.query(AllocatedMember).filter(
        AllocatedMember.user_id == current_user.id,
        AllocatedMember.allocation_id == existing.allocation_id,
        AllocatedMember.subject_id == existing.subject_id,
        AllocatedMember.is_subject_teacher ==1
    ).first()

    if not allocated:
        return {"status":0, "detail":"Unauthorized to update this marks"}

    data.updated_by=current_user.id
    updated=exam_crud.update_mark(db, id, data)
    if not updated:
        return {"status":0,"detail":"Marks not found"}

    return {
        "msg": "Mark updated successfully",
        "id": updated.id
    }

@router.post("/delete_mark/{id}")
def delete_mark(
    id: int,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type!=1:
         return {"status":0, "detail":"Unauthorized User"}

    success=exam_crud.soft_delete_mark(db, id, current_user.id)
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
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}

    for result in data.results:
        
        if current_user.user_community_type == 3:
            is_subject_teacher=db.query(AllocatedMember).filter(
                AllocatedMember.user_id == current_user.id,
                AllocatedMember.allocation_id == result.allocation_id,
                AllocatedMember.role == "subject_teacher"
            ).first()
            if not is_subject_teacher:
                return {"status":0, "detail":f"Unauthorized to create exam result for allocation {result.allocation_id}"}
                        
        result.created_by=current_user.id
        result.updated_by=current_user.id


    created=exam_crud.create_bulk_exam_results(db, data.results)
    return {
        "status": 1,
        "msg": f"{len(created)} exam results created successfully",
        "data": [r.id for r in created]
    }

@router.post("/list_exam_results")
def list_exam_results(
    skip: int=0,
    limit: int=10,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}

    results=exam_crud.get_all_exam_results(db)[skip: skip + limit]
    return results

@router.post("/student_marks_with_rank/{student_id}/{exam_id}")
def student_marks_with_rank(
    student_id: int,
    exam_id: int,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
  
    if current_user.user_community_type == 4 and current_user.id != student_id:
        return {"status": 0, "detail": "Access denied"}

    result=exam_crud.get_student_marks_with_rank(db, student_id, exam_id)

    if result["status"] == 0:
        return result  

    return result


@router.post("/get_exam_result/{id}")
def get_exam_result_per_class(
    id: int,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1, 2, 3]:
        return {"status": 0, "detail": "Unauthorized User"}
    
    if current_user.user_community_type in [1,2,3]:
        results=exam_crud.get_results_by_class_teacher(db, id)
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
    # ✅ Check role
    if current_user.user_community_type not in [1, 2, 3, 4]:
        return {"status": 0, "detail": "Unauthorized User"}

    # 🔒 If student, ensure they are viewing their own result
    if current_user.user_community_type == 4 and current_user.id != id:
        return {"status": 0, "detail": "Unauthorized to view others' result"}

    # ✅ Get result
    result = exam_crud.get_exam_result_by_student(db, id)
    return result


@router.post("/update_exam_result/{id}")
def update_exam_result(
    id: int,
    data: ExamResultSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1, 2, 3]:
        return {"status": 0, "detail": "Unauthorized User"}

    # 🔍 Fetch existing result to validate allocation
    existing = db.query(ExamResult).filter(ExamResult.id == id).first()
    if not existing:
        return {"status": 0, "detail": "Result not found"}

    # 🔒 If subject teacher, check if they are allocated to this allocation_id
    if current_user.user_community_type == 3:
        is_subject_teacher = db.query(AllocatedMember).filter(
            AllocatedMember.user_id == current_user.id,
            AllocatedMember.allocation_id == existing.allocation_id,
            AllocatedMember.role == "subject_teacher"
        ).first()

        if not is_subject_teacher:
            return {"status": 0, "detail": "Unauthorized to update this result"}

    data.updated_by = current_user.id
    updated = exam_crud.update_exam_result(db, id, data)

    return {
        "msg": "Exam result updated successfully",
        "id": updated.id
    }


@router.post("/delete_exam_result/{id}")
def delete_exam_result(
    id: int,
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    success=exam_crud.delete_exam_result(db, id)
    if not success:
        return {"status":0,"detail":"Result not found"}

    return {
        "status": 1,
        "msg": "Exam result deleted successfully"
    }

#-----------------------------------api for question paper-------------------------------------------------------#

@router.post("/teacher/upload_question_paper")
async def upload_question_paper(
    exam_id: int=Form(...),
    allocation_id: int=Form(...),
    subject_id: int=Form(...),
    file1: UploadFile=File(...),
    db: Session=Depends(deps.get_db),
    current_user: User=Depends(deps.get_current_user)
):
    allocated=db.query(AllocatedMember).filter(
        AllocatedMember.user_id == current_user.id,
        AllocatedMember.allocation_id == allocation_id,
        AllocatedMember.subject_id == subject_id,
        AllocatedMember.is_subject_teacher == 1
    ).first()

    if not allocated:
        return {"status":0, "detail":"Unauthorized to upload for this subject/allocation"}

    file_name=f"exam_{exam_id}_subject_{subject_id}_allocation_{allocation_id}.pdf"
    save_path, db_file_path =file_storage(file1,file_name)
     

    new_qp=QuestionPaper(
        exam_id=exam_id,
        allocation_id=allocation_id,
        subject_id=subject_id,
        uploaded_by=current_user.id,
        file_path=db_file_path,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_qp)
    db.commit()
    db.refresh(new_qp)

    return {
        "message": "Question paper uploaded successfully.",
        "question_paper_id": new_qp.id,
        "file_url": db_file_path
    }
