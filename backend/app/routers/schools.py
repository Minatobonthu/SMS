import schemas, models
import oauth2
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/createschool")
async def get_school_details(data: schemas.CreateSchool, db:Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    roles = ["system admin", "employee"]
    if current_user.role_name in roles:
        school = {
        "school_name": data.school_name.lower(),
        "school_address": data.school_address.lower(),
        "unique_school_id": data.unique_school_id.upper(),
        "principal_name": data.principal_name.lower(),
        "head_master":data.head_master.lower(),
        "phone_number": data.phone_number
    }
        new_school = model.Organization(**school, created_by=current_user.user_id, last_modified_by=current_user.user_id)
        db.add(new_school)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            assert isinstance(e.orig, UniqueViolation)
            return {"error": e.orig.diag.message_detail} 
        else:
            db.refresh(new_school)  
            return{"School created"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized to create")

# need to add few things, thinking of creating all the db queries as functions for getting roles and user_ids
@router.put("/editschool/{id}")
async def edit_school_details(id:int ,school_details: schemas.EditSchool, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    roles = ["system admin", "employee"]
    if current_user.role_name in roles:
        changed_values = {}
        for key, value in school_details.dict().items():
            if value is not None:
                changed_values[key] = value
        #querying the school details with the id provided
        current_school_values = db.query(model.Organization).filter(model.Organization.organization_id == id).first()
        print(current_school_values.school_name)

#need to add the access once adding teachers and students are completed
# so that they can only have access to the schools which belongs to them
@router.get("/searchschools/")
async def get_all_school_details(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    schools = db.query(model.Organization).all()
    all_organization_data = []
    for school in schools:
        one_data =  {"organization_id": school.organization_id,
        "unique_school_id": school.unique_school_id,
        "school_name": school.school_name,
        "school_address": school.school_address,
        "principal_name": school.principal_name,
        "head_master": school.head_master,
        "phone_number": school.phone_number,
        "created_at":school.created_at, 
        "created_by":school.created_by}
        all_organization_data.append(one_data)
    return all_organization_data


#need to add the access once adding teachers and students are completed
# so that they can only have access to the schools which belongs to them
@router.get("/searchschool/{school_name}")
async def get_school_by_name(school_name: str, db:Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    print(school_name)
    schools = db.query(model.Organization).filter(model.Organization.school_name.like(f"%{school_name.lower()}%")).all()
    all_organization_data = []
    for school in schools:
        one_data =  {"organization_id": school.organization_id,
        "unique_school_id": school.unique_school_id,
        "school_name": school.school_name,
        "school_address": school.school_address,
        "principal_name": school.principal_name,
        "head_master": school.head_master,
        "phone_number": school.phone_number,
        "created_at":school.created_at,
        "created_by":school.created_by}
        all_organization_data.append(one_data)
    return all_organization_data