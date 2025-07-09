from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.models import *
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash,verify_password
from datetime import datetime
from app.utils import *
from sqlalchemy import or_
from app.email_utils import send_otp_email

import random

router = APIRouter()
dt = str(int(datetime.utcnow().timestamp()))

@router.post('/login/access_token')
async def login_user(db:Session=Depends(deps.get_db),user_name:str=Form(...),password:str=Form(...)):
    checkUser = db.query(User).filter(or_(User.user_name == user_name,
                                          User.email == user_name,
                                          User.phone_number == user_name),
                                      User.status ==1).first()
    
    if not checkUser:
        return {"status":0,"msg":"User not found."}
    password_verification = verify_password(password, checkUser.password)
    if not password_verification:
        return {"status":0,"msg":"Password might be worng."}
    else:
        token_deactivate=db.query(Apitoken).filter(Apitoken.user_id==checkUser.id,Apitoken.status==1).first()
        if token_deactivate:
            token_deactivate.status=-1
            db.commit()

        char1 = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
        char2 = 'QWERTYUIOPLKJHGFDSAZXCVBNM0123456789'
        reset_character = char1 + char2
        key = ''.join(random.choices(reset_character, k=30)) 
        
        token =f"{key}nTew20drhkl"
    
        create_token = Apitoken(
            user_id = checkUser.id,
            token = token,
            created_at = datetime.now(),
            status = 1
        )
        db.add(create_token)
        db.commit()
        
        return {"status":1,"msg":"Login successfully","token":token}
    

@router.post('/user_logout',description="This Route is for Logout User")
def log_out(token:str=Form(...),db:Session=Depends(deps.get_db)):
    check_token=deps.get_current_user(token,db)
    if isinstance(check_token,dict):
        return check_token
    log_out_status=db.query(Apitoken).filter(Apitoken.user_id==check_token.id,Apitoken.status==1)
    log_out_status.update({Apitoken.status:0})
    db.commit()
    return{"status":1,"msg":f"Log Out Successful {check_token.first_name}"}
    
@router.post("/forgot-password")
def forgot_password(email: str = Form(...), db: Session = Depends(deps.get_db)):
    user = db.query(User).filter(User.email == email, User.status == 1).first()
    if not user:
        return {"status":0,"detail":"User not found"}

    otp = ''.join(random.choices("0123456789", k=6))
    expires = datetime.utcnow() + timedelta(minutes=2)

    otp_entry = OTP(user_id=user.id, otp_code=otp, expires_at=expires)
    db.add(otp_entry)
    db.commit()

    if send_otp_email(email, otp):
        return {"status": 1, "msg": "OTP sent to your email"}
    else:
        return {"status":0,"detail":"Failed to send OTP"}
    

@router.post("/reset-password")
def reset_password(
    email: str = Form(...),
    otp: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(deps.get_db)
):
    user = db.query(User).filter(User.email == email, User.status == 1).first()
    if not user:
        return {"status":0,"detail":"User not found"}

    otp_entry = db.query(OTP).filter(
        OTP.user_id == user.id,
        OTP.otp_code == otp,
        OTP.status == 1,
        OTP.expires_at >= datetime.utcnow()
    ).first()

    if not otp_entry:
        return {"status":0,"detail":"Invalid or expired OTP"}

    otp_entry.status = 0
    user.password = get_password_hash(new_password)
    db.commit()

    return {"status": 1, "msg": "Password reset successfully"}  