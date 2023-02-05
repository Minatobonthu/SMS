import schemas, models
import oauth2, passwordlogic
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

router = APIRouter()

#check later, so that you can complete all the db transaction in one go
#when creating password, they should be able to add role and organization they belongs to in one go rather that adding seperately
@router.post("/createuser/")
async def create_user(user: schemas.SignupIN, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    roles = ["system admin", "employee","school admin"]
    if current_user.role_name in roles:
        user_details = {
        "email_address":user.email_address,
        "first_name":user.first_name, 
        "last_name":user.last_name,
        "password":passwordlogic.hashing_password(user.password),
        "account_status": user.account_status
        }
        user_created = False
        new_user = models.User(**user_details, created_by = current_user.user_id, last_modified_by = current_user.user_id)
        db.add(new_user)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            assert isinstance(e.orig, UniqueViolation)
            user_created=False
            return {"error": e.orig.diag.message_detail} 
        else:
            db.refresh(new_user)
            user_created=True
    new_record = new_user
    if user_created:
        new_record_role = db.query(models.Role).filter(models.Role.role_name == user.role).first()
        role = models.RoleAccess(
            user_id= new_record.user_id,
            role_id= new_record_role.role_id,
            created_by= current_user.user_id,
            last_modified_by= current_user.user_id
        )

        organization_record = db.query(models.Organization).filter(models.Organization.school_name == user.organization).first()

        organization = models.Organization_access(
            organization_id= organization_record.organization_id,
            user_id=new_record.user_id,
            created_by= current_user.user_id,
            last_modified_by= current_user.user_id)

    try:
        db.add_all([ role, organization])
        db.commit()
    except IntegrityError as e:
        db.rollback()
        return {"error": str(e)}
    else: 
        return {"message": "Record has been created"}