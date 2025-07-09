from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models import User
from app.schemas import StudentFeesSchema, BulkStudentFeesSchema,StudentScholarshipSchema,BulkStudentScholarshipSchema,\
    SchoolFeesSchema,BulkSchoolFeesSchema
from app.crud import fees_crud

router = APIRouter()

#---------------------------------api for student_scholarship-----------------------------------#


@router.post("/bulk_scholarship_create")
def bulk_create_scholarships(
    data: BulkStudentScholarshipSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,5]:
         return {"status":0, "detail":"Unauthorized User"}
    
    for sch in data.scholarships:
        sch.created_by = current_user.id
        sch.updated_by = current_user.id

    created_scholarships = fees_crud.create_bulk_scholarships(db, data.scholarships)
    result = [
        {
            "id": s.id,
            "user_id": s.user_id,
            "academic_year_id": s.academic_year_id,
            "scholarship_name": s.scholarship_name,
            "discount_value": s.discount_value,
            "status": s.status
        }
        for s in created_scholarships
    ]
    return {
        "status": 1,
        "msg": f"{len(result)} scholarships created successfully",
        "data": result
    }

@router.post("/list_scholarship")
def list_scholarships(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,5]:
         return {"status":0, "detail":"Unauthorized User"}

    scholarships = fees_crud.get_all_scholarships(db)[skip: skip + limit]
    return [
        {
            "id": s.id,
            "user_id": s.user_id,
            "academic_year_id": s.academic_year_id,
            "scholarship_name": s.scholarship_name,
            "discount_value": s.discount_value,
            "status": s.status
        }
        for s in scholarships
    ]

@router.post("/get_scholarship/{id}")
def get_scholarship(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,4,5]:
         return {"status":0, "detail":"Unauthorized User"}

    s = fees_crud.get_scholarship_by_id(db, id)
    if not s or s.status != 1:
        return {"status":0,"detail":"Scholarship not found"}

    return {
        "id": s.id,
        "user_id": s.user_id,
        "academic_year_id": s.academic_year_id,
        "scholarship_name": s.scholarship_name,
        "discount_value": s.discount_value,
        "status": s.status
    }

@router.post("/update_scholarship/{id}")
def update_scholarship(
    id: int,
    data: StudentScholarshipSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated = fees_crud.update_scholarship(db, id, data)
    if not updated:
        return {"status":0,"detail":"Scholarship not found"}

    return {
        "msg": "Scholarship updated successfully",
        "id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete_scholarship/{id}")
def delete_scholarship(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type!=1:
         return {"status":0, "detail":"Unauthorized User"}

    success = fees_crud.soft_delete_scholarship(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Scholarship not found"}

    return {
        "status": 1,
        "msg": "Scholarship deleted successfully"
    }
    
#----------------------------------api for school_fees----------------------------------------#

@router.post("/bulk_schoolfees_create")
def bulk_create_school_fees(
    data: BulkSchoolFeesSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    for fee in data.fees:
        fee.created_by = current_user.id
        fee.updated_by = current_user.id

    created_fees = fees_crud.create_bulk_school_fees(db, data.fees)
    result = [
        {
            "id": f.id,
            "academic_year_id": f.academic_year_id,
            "class_id": f.class_id,
            "group_id": f.group_id,
            "fee_type": f.fee_type,
            "amount": f.amount
        }
        for f in created_fees
    ]
    return {
        "status": 1,
        "msg": f"{len(result)} school fees created successfully",
        "data": result
    }

@router.post("/list_school_fees")
def list_school_fees(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,5]:
         return {"status":0, "detail":"Unauthorized User"}

    fees = fees_crud.get_all_school_fees(db)[skip: skip + limit]
    return [
        {
            "id": f.id,
            "academic_year_id": f.academic_year_id,
            "class_id": f.class_id,
            "group_id": f.group_id,
            "fee_type": f.fee_type,
            "amount": f.amount
        }
        for f in fees
    ]

@router.post("/get_schoolfees/{id}")
def get_school_fee(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,5]:
         return {"status":0, "detail":"Unauthorized User"}

    fee = fees_crud.get_school_fee_by_id(db, id)
    if not fee or fee.status != 1:
        return {"status":0,"detail":"Fees record not found"}

    return {
        "id": fee.id,
        "academic_year_id": fee.academic_year_id,
        "class_id": fee.class_id,
        "group_id": fee.group_id,
        "fee_type": fee.fee_type,
        "amount": fee.amount
    }

@router.post("/update_schoolfees/{id}")
def update_school_fee(
    id: int,
    data: SchoolFeesSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated =fees_crud.update_school_fee(db, id, data)
    if not updated:
        return {"status":0,"detail":"Fees record not found"}

    return {
        "msg": "School fee record updated successfully",
        "id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete_schoolfees/{id}")
def delete_school_fee(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    success = fees_crud.soft_delete_school_fee(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Fees record not found"}

    return {
        "status": 1,
        "msg": "School fee record deleted successfully"
    }


#-------------------------------api for student_fees-----------------------------------------#

@router.post("/bulk_student_fees_create")
def bulk_create_student_fees(
    data: BulkStudentFeesSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,5]:
         return {"status":0, "detail":"Unauthorized User"}

    for fee in data.fees:
        fee.created_by = current_user.id
        fee.updated_by = current_user.id

    created_fees = fees_crud.create_bulk_student_fees(db, data.fees)
    result = [
        {
            "id": f.id,
            "student_id": f.student_id,
            "scl_fee_id": f.scl_fee_id,
            "paid_amount": f.paid_amount,
            "status": f.status,
            "receipt_no": f.receipt_no
        }
        for f in created_fees
    ]
    return {
        "status": 1,
        "msg": f"{len(result)} student fees records created successfully",
        "data": result
    }

@router.post("/list_all_student_fees")
def list_student_fees(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,5]:
         return {"status":0, "detail":"Unauthorized User"}

    fees = fees_crud.get_all_student_fees(db)[skip: skip + limit]
    return [
        {
            "id": f.id,
            "student_id": f.student_id,
            "scl_fee_id": f.scl_fee_id,
            "scholarship_id": f.scholarship_id,
            "paid_amount": f.paid_amount,
            "status": f.status,
            "receipt_no": f.receipt_no
        }
        for f in fees
    ]

@router.post("/get_student_fees/{id}")
def get_student_fee(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,4,5]:
         return {"status":0, "detail":"Unauthorized User"}

    fee = fees_crud.get_student_fee_by_id(db, id)
    if not fee or fee.status == "deleted":
        return {"status":0,"detail":"Fees record not found"}

    return {
        "id": fee.id,
        "student_id": fee.student_id,
        "scl_fee_id": fee.scl_fee_id,
        "scholarship_id": fee.scholarship_id,
        "paid_amount": fee.paid_amount,
        "due_date": fee.due_date,
        "payment_date": fee.payment_date,
        "payment_mode": fee.payment_mode,
        "status": fee.status,
        "receipt_no": fee.receipt_no
    }

@router.post("/update_student_fees/{id}")
def update_student_fee(
    id: int,
    data: StudentFeesSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,5]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated = fees_crud.update_student_fee(db, id, data)
    if not updated:
        return {"status":0,"detail":"Fees record not found"}

    return {
        "msg": "Student fee record updated successfully",
        "id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete_student_fees/{id}")
def delete_student_fee(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
        return {"status":0, "detail":"Unauthorized User"}

    success = fees_crud.soft_delete_student_fee(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Fees record not found"}

    return {
        "status": 1,
        "msg": "Student fee record deleted successfully"
    }
