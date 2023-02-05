import schemas, models
import oauth2, passwordlogic
from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
async def user_login(login_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email_address == login_credentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                                detail="Invalid credentials!")
    if user.account_status == "locked":
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
        detail="Your account is locked. Please contact the administrator.")

    if not passwordlogic.check_password(password = login_credentials.password, hashed_password=user.password):
        user.failed_attempts+=1
        if user.failed_attempts >=3:
            user.account_status = "locked"
        db.commit()
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                                detail="Invalid credentials")
    user.failed_attempts = 0
    db.commit()
    access_token = oauth2.create_access_token(data = {"user_id": user.user_id})
    return {"access_token" : access_token, "token_type": "bearer"}

@router.post("/forgotpassword")
async def password_reset_link(user_details: schemas.ForgotPassword, request: Request, db:Session = Depends(get_db)):
    user_details = db.query(models.User).filter(user_details.email_address == models.User.email_address).first()
    if not user_details: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Email address doesnot exist")
    access_token = oauth2.create_access_token(data={"user_id": user_details.user_id, "email_address": user_details.email_address})
    return {"url": request.url._url+"/"+access_token}


@router.post("/resetpassword")
async def password_reset(data: schemas.PasswordReset, db:Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    user_details = db.query(models.User).filter(current_user.email_address == models.User.email_address).first()

    user_details.password = passwordlogic.hashing_password(data.password)
    db.commit()
    db.refresh(user_details)
    return {"status": "password reset sucessful"}