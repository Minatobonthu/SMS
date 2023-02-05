from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models
from config import settings
from sqlalchemy.orm import joinedload

oauth2_schema = OAuth2PasswordBearer(tokenUrl="forgotpasswordreset")

#secret_key
#algorith
#expiration date

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES= settings.access_token_expire_minutes



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")
        # role: str = payload.get("role")
        email_address: Optional [str] = payload.get("email_address")

        # if id is None or role is None:
        if id is None :
            raise credentials_exception
        # token_data = schemas.TokenData(id=id, role=role, email_address=email_address)
        token_data = schemas.TokenData(id=id, email_address=email_address)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="could not validate credentails", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token=token, credentials_exception=credentials_exception)
    # current_user = db.query(model.User).filter(model.User.user_id == token.id).first()

    #just added testing joins
    current_user = db.query(models.User.user_id, models.User.email_address, model.RoleAccess.role_id, model.Role.role_name, model.Organization_access.organization_id, model.Organization.school_name).join(model.RoleAccess, model.RoleAccess.user_id == model.User.user_id).join(model.Role, model.RoleAccess.role_id==model.Role.role_id).join(model.Organization_access, model.User.user_id == model.Organization_access.user_id).join(model.Organization, model.Organization_access.organization_id == model.Organization.organization_id).all()
    for user_details in current_user:
        return user_details
        # print(row.User.email_address, row.RoleAccess.role_id, row.Role.role_name, row.Organization_access.organization_id, row.Organization.school_name)