from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import User
from app.schemas import AcademicYearSchema,GroupSchema,ClassSchema,BulkClassSchema,SectionSchema,BulkSectionSchema,\
BulkSubjectSchema,SubjectSchema

from datetime import datetime
from app.api import deps
from crud import academic_crud

router = APIRouter()

@router.post("/create_academic_year")
def create_academic_year(
    data: AcademicYearSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
        return {"status":0, "detail":"Unauthorized User"}
    
    academic_data=academic_crud.create_academic_year(db, data)
    
    return {
        "status": 1,
        "msg": "Academic year created successfully",
        "academic_year_id": academic_data.id,
        "academic_year":academic_data.year,
        "created_by":academic_data.created_by
    }
    
@router.post("/list_academic_years")
def list_academic_years(skip:int,limit:int,
    db: Session = Depends(deps.get_db),
    current_user:User=Depends(deps.get_current_user)
):
        if current_user.user_community_type not in [1,2,3,5]:
            return {"status":0, "detail":"Unauthorized User"}
        
        result=academic_crud.get_academic_years(db)[skip: skip + limit]
        return [
            {
                "academic_year_id": item.id,
                "year": item.year,
                "created_by": item.created_by
            } for item in result
        ]
        
@router.post("/get_academic_year/{id}")
def get_academic_year(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,5]:
        return {"status":0, "detail":"Unauthorized User"}
    
    ay = academic_crud.get_academic_year_by_id(db, id)
    if not ay:
        return {"status":0, "detail":"Academic year not found"}
    return ay

@router.post("/update_academic_year/{id}")
def update_academic_year(
    id: int,
    data: AcademicYearSchema,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    data.updated_by = current_user.id
    updated = academic_crud.update_academic_year(db, id, data)
    if not updated:
        return {"status":0, "detail":"Academic year not found"}
    return {"msg":"Academic year updated successfully",
        "data":updated}
    
@router.post("/delete_academic_year/{iid}")
def delete_academic_year(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user)
):
    if current_user.user_community_type !=1:
         return {"status":0, "detail":"Unauthorized User"}
    
    success = academic_crud.soft_delete_academic_year(db, id, current_user.id)
    if not success:
        return {"status":0, "detail":"Academic year not found"}
    return {"msg": "Academic year deleted successfully"}

#------------------------------------api for groups------------------------------------------------#

@router.post("/create_group")
def create_group(
    data: GroupSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    data.created_by = current_user.id
    group_data = academic_crud.create_group(db, data)
    return {
        "status": 1,
        "msg": "Group created successfully",
        "group_id": group_data.id,
        "group_name": group_data.group_name,
        "created_by": group_data.created_by
    }

 
@router.post("/list_groups")
def list_groups(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,5]:
         return {"status":0, "detail":"Unauthorized User"}

    result = academic_crud.get_all_groups(db)[skip: skip + limit]
    return [
        {
            "group_id": item.id,
            "group_name": item.group_name,
            "created_by": item.created_by
        } for item in result
    ]

 
@router.post("/get_group/{id}")
def get_group(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,5]:
         return {"status":0, "detail":"Unauthorized User"}

    group =academic_crud.get_group_by_id(db, id)
    if not group or group.status != "active":
        return {"status":0,"detail":"Group not found"}

    return {
        "group_id": group.id,
        "group_name": group.group_name,
        "created_by": group.created_by
    }

 
@router.post("/update_group/{id}")
def update_group(
    id: int,
    data: GroupSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated = academic_crud.update_group(db, id, data)
    if not updated:
        return {"status":0,"detail":"Group not found"}

    return {
        "msg": "Group updated successfully",
        "data": {
            "group_id": updated.id,
            "group_name": updated.group_name,
            "updated_by": updated.updated_by
        }
    }


@router.post("/delete_group/{id}")
def delete_group(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type !=1:
         return {"status":0, "detail":"Unauthorized User"}

    success = academic_crud.soft_delete_group(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Group not found"}

    return {
        "msg": "Group deleted successfully"
    }
    
#---------------------------api for classes------------------------------#


@router.post("/bulk-create_classes")
def bulk_create_classes(
    data: BulkClassSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    for cls in data.classes:
        cls.created_by = current_user.id
        cls.updated_by = current_user.id

    created_classes = academic_crud.create_bulk_classes(db, data.classes)

    return {
        "status": 1,
        "msg": f"{len(created_classes)} classes created successfully",
        "data": [
            {
                "id": cls.id,
                "class_name": cls.class_name,
                "status": cls.status,
                "created_by": cls.created_by
            }
            for cls in created_classes
        ]
    }
    
    
@router.post("/list_classes")
def list_classes(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,5]:
         return {"status":0, "detail":"Unauthorized User"}
    
    classes = academic_crud.get_all_classes(db)[skip: skip + limit]
    return classes


@router.post("get_class/{id}")
def get_class(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4,5]:
         return {"status":0, "detail":"Unauthorized User"}
    
    class_obj = academic_crud.get_class_by_id(db, id)
    if not class_obj or class_obj.status != 1:
        return {"status":0,"detail":"Class not found"}
    return class_obj


@router.post("/update_class/{id}")
def update_class(
    id: int,
    data: ClassSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    data.updated_by = current_user.id
    updated = academic_crud.update_class(db, id, data)
    if not updated:
        return {"status":0,"detail":"Class not found"}
    return updated


@router.post("/delete_class/{id}")
def delete_class(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type!=1:
         return {"status":0, "detail":"Unauthorized User"}

    success = academic_crud.soft_delete_class(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Class not found"}
    return {"status": 1, "msg": "Class deleted successfully"}

#----------------------------------api for sections----------------------------------#


@router.post("/bulk-create_sections")
def bulk_create_sections(
    data: BulkSectionSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}

    for section in data.sections:
        section.created_by = current_user.id
        section.updated_by = current_user.id

    sections = academic_crud.create_bulk_sections(db, data.sections)

    return {
        "status": 1,
        "msg": f"{len(sections)} sections created successfully",
        "data": [
            {
                "id": s.id,
                "section_name": s.section_name,
                "class_id": s.class_id,
                "status": s.status
            } for s in sections
        ]
    }

@router.post("/list_sections")
def list_sections(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,5]:
         return {"status":0, "detail":"Unauthorized User"}
    
    return academic_crud.get_all_sections(db)

@router.post("get_section/{id}")
def get_section(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4,5]:
         return {"status":0, "detail":"Unauthorized User"}
    
    section = academic_crud.get_section_by_id(db, id)
    if not section or section.status != 1:
        return {"status":0,"detail":"Section not found"}
    return section

@router.post("/update_section/{id}")
def update_section(
    id: int,
    data: SectionSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    data.updated_by = current_user.id
    updated = academic_crud.update_section(db, id, data)
    if not updated:
        return {"status":0,"detail":"Section not found"}
    return updated

@router.post("/delete_section/{id}")
def delete_section(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type!=1:
         return {"status":0, "detail":"Unauthorized User"}

    success = academic_crud.soft_delete_section(db, id, current_user.id)
    if not success: 
        return {"status":0,"detail":"Section not found"}
    return {"status": 1, "msg": "Section deleted successfully"}

#---------------------------------------api for subjects-----------------------------------#

@router.post("/bulk_subject_create")
def bulk_create_subjects(
    data: BulkSubjectSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    for subject in data.subjects:
        subject.created_by = current_user.id
        subject.updated_by = current_user.id

    created_subjects = academic_crud.create_bulk_subjects(db, data.subjects)
    result = [
        {
            "subject_id": sub.id,
            "subject_name": sub.subject_name,
            "subject_code": sub.subject_code,
            "group_id": sub.group_id,
            "created_by": sub.created_by
        }
        for sub in created_subjects
    ]

    return {
        "status": 1,
        "msg": f"{len(result)} subjects created successfully",
        "data": result
    }

@router.post("/list_subjects")
def list_subjects(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}
    
    subjects = academic_crud.get_all_subjects(db)[skip: skip + limit]
    return [
        {
            "subject_id": sub.id,
            "subject_name": sub.subject_name,
            "subject_code": sub.subject_code,
            "group_id": sub.group_id,
            "created_by": sub.created_by
        }
        for sub in subjects
    ]

@router.post("/get_subject/{id}")
def get_subject(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}
    
    subject = academic_crud.get_subject_by_id(db, id)
    if not subject or subject.status != 1:
        return {"status":0,"detail":"Subject not found"}
    
    return {
        "subject_id": subject.id,
        "subject_name": subject.subject_name,
        "subject_code": subject.subject_code,
        "group_id": subject.group_id,
        "created_by": subject.created_by,
        "updated_by": subject.updated_by
    }

@router.post("/update_subject/{id}")
def update_subject(
    id: int,
    data: SubjectSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    data.updated_by = current_user.id
    updated = academic_crud.update_subject(db, id, data)
    if not updated:
        return {"status":0,"detail":"Subject not found"}

    return {
        "msg": "Subject updated successfully",
        "subject_id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete_subject/{id}")
def delete_subject(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type!=1:
         return {"status":0, "detail":"Unauthorized User"}
    
    success = academic_crud.soft_delete_subject(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Subject not found"}

    return {
        "status": 1,
        "msg": "Subject deleted successfully"
    }