from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import AllocationSchema,BulkAllocationSchema,AllocatedMemberSchema,BulkAllocatedMember,ClassGroupSchema,BulkClassGroupSchema
from app.crud import allocation_crud
from app.api import deps
from app.models import User

router = APIRouter()

#-----------------------------------api for allocations-------------------------------#

@router.post("/bulk-create")
def bulk_create_allocations(
    data: BulkAllocationSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    for alloc in data.allocations:
        alloc.created_by = current_user.id
        alloc.updated_by = current_user.id

    created_allocs = allocation_crud.create_bulk_allocations(db, data.allocations)


    result = []
    for allocation in created_allocs:
        result.append({
            "allocation_id": allocation.id,
            "academic_year_id": allocation.academic_year_id,
            "class_id": allocation.class_id,
            "section_id": allocation.section_id,
            "group_id": allocation.group_id,
            "status": allocation.status,
            "created_by": allocation.created_by
        })

    return {
        "status": 1,
        "msg": f"{len(result)} allocations created successfully",
        "data": result
    }

@router.post("/list")
def list_allocations(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    
    if current_user.user_community_type not in [1,2,3,5]:
         return {"status":0, "detail":"Unauthorized User"}
    
    allocations = allocation_crud.get_all_allocations(db)[skip: skip + limit]
    return [
        {
            "allocation_id": alloc.id,
            "academic_year_id": alloc.academic_year_id,
            "class_id": alloc.class_id,
            "section_id": alloc.section_id,
            "group_id": alloc.group_id,
            "status": alloc.status,
            "created_by": alloc.created_by
        }
        for alloc in allocations
    ]

@router.post("/{id}")
def get_allocation(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4,5]:
         return {"status":0, "detail":"Unauthorized User"}
    
    alloc = allocation_crud.get_allocation_by_id(db, id)
    if not alloc or alloc.status != 1:
        return {"status":0,"detail":"Allocation not found"}
    return {
        "allocation_id": alloc.id,
        "academic_year_id": alloc.academic_year_id,
        "class_id": alloc.class_id,
        "section_id": alloc.section_id,
        "group_id": alloc.group_id,
        "status": alloc.status,
        "created_by": alloc.created_by,
        "updated_by": alloc.updated_by
    }

@router.post("/update/{id}")
def update_allocation(
    id: int,
    data: AllocationSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    data.updated_by = current_user.id
    updated = allocation_crud.update_allocation(db, id, data)
    if not updated:
        return {"status":0,"detail":"Allocation not found"}
    return {
        "msg": "Allocation updated successfully",
        "allocation_id": updated.id,
        "updated_by": updated.updated_by
    }

@router.post("/delete/{id}")
def delete_allocation(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type!=1:
         return {"status":0, "detail":"Unauthorized User"}
    
    success = allocation_crud.soft_delete_allocation(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Allocation not found"}
    return {
        "status": 1,
        "msg": "Allocation deleted successfully"
    }
    
#--------------------------------------api for allocated_members----------------------------------#


@router.post("/create_allocated_member")
def create_allocated_member_api(
    data: BulkAllocatedMember,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    for member in data.allocated_member:
        member.created_by = current_user.id
        member.updated_by = current_user.id
    
    allocated_member = allocation_crud.create_allocated_member(db, data.allocated_member)
    return {
        "status": 1,
        "msg": "Allocated member created successfully",
        "id": [{"allocated_member_id": m.id,
                "allocation_id": m.allocation_id,
                "user_id": m.user_id,
                "subject_id": m.subject_id,
                "is_subject_teacher": m.is_subject_teacher,
                "role":m.role
                }
                for m in allocated_member]
    }


@router.post("/list_allocated_members")
def list_allocated_members(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3]:
         return {"status":0, "detail":"Unauthorized User"}
    
    result = allocation_crud.get_all_allocated_members(db)
    return [
        {
            "id": item.id,
            "allocation_id": item.allocation_id,
            "user_id": item.user_id,
            "subject_id": item.subject_id,
        } for item in result
    ]


@router.post("/get_allocated_member/{id}")
def get_allocated_member( 
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}
    
    item = allocation_crud.get_allocated_member_by_id(db, id)
    if not item or item.status != 1:
        return {"status":0,"detail":"Allocated member not found"}
    return {
        "id": item.id,
        "allocation_id": item.allocation_id,
        "user_id": item.user_id,
        "subject_id": item.subject_id,
    }


@router.post("/update_allocated_member/{id}")
def update_allocated_member(
    id: int,
    data: AllocatedMemberSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
    
    data.updated_by = current_user.id
    updated = allocation_crud.update_allocated_member(db, id, data)
    if not updated:
        return {"status":0,"detail":"Allocated member not found"}
    return {
        "msg": "Allocated member updated successfully",
        "data": {
            "id": updated.id,
            "allocation_id": updated.allocation_id,
            "user_id": updated.user_id,
            "subject_id": updated.subject_id,
        }
    }


@router.post("/delete_allocated_member/{id}")
def delete_allocated_member(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type !=1:
         return {"status":0, "detail":"Unauthorized User"}
    
    success = allocation_crud.soft_delete_allocated_member(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Allocated member not found"}
    return {"msg": "Allocated member deleted successfully"}

#------------------------------------------api for class_group---------------------------------------------------#


@router.post("/bulk_class_group_create")
def bulk_create_class_groups(
    data: BulkClassGroupSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
     
    for cg in data.class_groups:
        cg.created_by = current_user.id
        cg.updated_by = current_user.id

    created = allocation_crud.create_bulk_class_groups(db, data.class_groups)
    return {
        "status": 1,
        "msg": f"{len(created)} class-group mappings created successfully"
    }

@router.post("/list_class_group")
def list_class_groups(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}

    return allocation_crud.get_all_class_groups(db)

@router.post("/get_class_group/{id}")
def get_class_group_by_id(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2,3,4]:
         return {"status":0, "detail":"Unauthorized User"}
     
    result = allocation_crud.get_class_group_by_id(db, id)
    if not result:
        return {"status":0,"detail":"Class group not found"}
    return result

@router.post("/update_class_group/{id}")
def update_class_group(
    id: int,
    data: ClassGroupSchema,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type not in [1,2]:
         return {"status":0, "detail":"Unauthorized User"}
     
    data.updated_by = current_user.id
    updated = allocation_crud.update_class_group(db, id, data)
    if not updated:
        return {"status":0,"detail":"Class group not found"}
    return {
        "msg": "ClassGroup updated successfully",
        "id": updated.id
    }

@router.post("/delete_class_group/{id}")
def delete_class_group(
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if current_user.user_community_type !=1:
         return {"status":0, "detail":"Unauthorized User"}
     
    success = allocation_crud.soft_delete_class_group(db, id, current_user.id)
    if not success:
        return {"status":0,"detail":"Class group not found"}
    return {
        "status": 1,
        "msg": "ClassGroup deleted successfully"
    }