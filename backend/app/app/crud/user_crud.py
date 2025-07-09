from sqlalchemy.orm import Session
from datetime import datetime
from app.models import User
from app.core.security import get_password_hash
from app.schemas.users import UserCreate
from typing import List
from fastapi import HTTPException

def check_create_permission(current_user_role: int, new_user_role: int):
    if current_user_role == 1:
        return {"status": 1, "msg": "Permission granted"}

    if current_user_role == 2:
        if new_user_role in [3, 4]:
            return {"status": 1, "msg": "Permission granted"}
        return {"status": 0, "detail": "Principal can only create Teacher or Student"}

    if current_user_role == 3:
        if new_user_role == 4:
            return {"status": 1, "msg": "Permission granted"}
        return {"status": 0, "detail": "Teacher can only create Student"}

    return {"status": 0, "detail": "You are not authorized to create users."}


def create_bulk_users(
    db: Session,
    users: List[UserCreate],
    created_by_id: int,
    creator_type: int
):
    user_objs = []

    for user in users:
        if creator_type == 3 and user.user_community_type != 4:
            raise HTTPException(status_code=403, detail="Staff can only create students")
        elif creator_type==2 and user.user_community_type==1:
            raise HTTPException(status_code=403,detail="You are not allowed to create admin")

        existing = db.query(User).filter(User.status == 1)

        if existing.filter(User.user_name == user.user_name).first():
            raise HTTPException(status_code=400, detail="Username already exists")

        if existing.filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")

        if existing.filter(User.phone_number == user.phone_number).first():
            raise HTTPException(status_code=400, detail="Phone number already exists")

        user_obj = User(
            user_name=user.user_name,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email, 
            phone_number=user.phone_number,
            user_community_type=user.user_community_type,
            password=get_password_hash(user.password),
            age=user.age,
            gender=user.gender,
            dob=user.dob,
            address=user.address,
            profile_image=user.profile_image,
            guardian_name=user.guardian_name,
            roll_number=user.roll_number,
            status=user.status,
            created_by=created_by_id,
            created_at=datetime.utcnow(),
            updated_by=created_by_id,
            updated_at=datetime.utcnow()
        )
        user_objs.append(user_obj)

    db.add_all(user_objs)
    db.commit()
    return user_objs

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id, User.status == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).filter(User.status == 1).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, data: UserCreate, updated_by: int):
    user = db.query(User).filter(User.id == user_id, User.status == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in data.dict(exclude_unset=True).items():
        if field == "password":
            setattr(user, field, get_password_hash(value))
        else:
            setattr(user, field, value)

    user.updated_by = updated_by
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int, updated_by: int):
    user = db.query(User).filter(User.id == user_id, User.status == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.status = 0
    user.updated_by = updated_by
    user.updated_at = datetime.utcnow()

    db.commit()
    return {"status": 1, "msg": "User deleted successfully"}
