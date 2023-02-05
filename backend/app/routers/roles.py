import schemas, models
import oauth2
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/createrole")
async def create_role(role_details: schemas.CreateRole, current_user: str = Depends(oauth2.get_current_user), db:Session = Depends(get_db)):
    roles = ["system admin", "employee"]
    if current_user.role_name in roles:
        new_role = model.Role(**role_details.dict(), created_by= current_user.user_id, last_modified_by= current_user.user_id)
        db.add(new_role)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            assert isinstance(e.orig, UniqueViolation)
            return {"error": e.orig.diag.message_detail} 
        else:
            db.refresh(new_role)
            return{"role created sucessfully"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized to view")



