from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.users import User
from app.schemas.users import BulkUserCreate,UserCreate
from datetime import datetime
from app.api import deps
from crud import user_crud

router = APIRouter()
@router.post("/create_user")
def create_user(
    data: BulkUserCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    
    permission = user_crud.check_create_permission(current_user.user_community_type, data.user_community_type)
    
    if permission["status"] == 0:
        return permission 

    created_users = user_crud.create_bulk_users(
        db=db,
        users=data.users,
        created_by_id=current_user.id,
        creator_type=current_user.user_community_type
    )

    return {
        "status": 1,
        "msg": "User(s) created successfully",
        "users": [
            {
                "user_id": user.id,
                "user_type": user.user_community_type,
                "user_name": user.user_name
            }
            for user in created_users
        ]
    }
    
@router.post("/list_users")
def get_all_users(skip: int = 0,limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if current_user.user_community_type not in [1, 2]:
        return {"status":0,"detail":"Unauthorized"}

    users = db.query(User).filter(User.status == 1).all()[skip:skip + limit]
    return users
 
@router.post("/get_user/{user_id}")
def get_user_by_id(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    user = db.query(User).filter(User.id == user_id, User.status == 1).first()
    if not user:
        return {"status":0,"detail":"User not found"}
    return user

 
@router.post("/update_user/{user_id}")
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    user = db.query(User).filter(User.id == user_id, User.status == 1).first()
    if not user:
        return {"status":0,"detail":"User not found"}

    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    user.updated_by = current_user.id
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)
    return {"status": 1, "msg": "User updated successfully", "user": user}

 
@router.post("/delete_user/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    user = db.query(User).filter(User.id == user_id, User.status == 1).first()
    if not user:
        return {"status":0,"detail":"User not found"}

    user.status = 0
    user.updated_by = current_user.id
    user.updated_at = datetime.utcnow()

    db.commit()
    return {"status": 1, "msg": "User deleted (soft) successfully"}
