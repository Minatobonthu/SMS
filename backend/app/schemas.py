
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class login(BaseModel):
    email_address: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    # token_type: str

class ForgotPassword(BaseModel):
    email_address: EmailStr

class PasswordReset(BaseModel):
    password: str

class CreateRole(BaseModel):
    role_name:str

class CreateSchool(BaseModel):
    school_name: str
    school_address: str
    unique_school_id:str
    principal_name:str
    head_master:str
    phone_number:str

class EditSchool(BaseModel):
    school_name: Optional[str] = None
    school_address: Optional[str] = None
    unique_school_id:Optional[str] = None
    principal_name:Optional[str] = None
    head_master:Optional[str] = None
    phone_number:Optional[str] = None

class SignupIN(BaseModel):
    email_address: EmailStr
    first_name:str
    last_name:str
    password:str
    account_status:str = "active"
    role:str
    organization:str

    class Config:
        orm_mode = True

class Signupout(BaseModel):
    id:int
    email_address: EmailStr
    first_name:str
    last_name:str

    class Config:
        orm_mode = True



class TokenData(BaseModel):
    id: Optional[str] = None
    # role: Optional[str] = None
    email_address: Optional[str] = None
