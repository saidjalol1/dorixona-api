from fastapi import APIRouter, Depends
from datetime import datetime
from database.models import Users, Drug
from database.config import get_db
from database.schemas import DrugCreate 

drug_route = APIRouter(tags=["Drug apis"])

@drug_route.post("/drug-create/")
def drug_create(admin_id: int, drug_data:DrugCreate, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()
    if admin_user.role == "admin":
        new_drug = Drug(**drug_data.model_dump())
        new_drug.date_created = datetime.now()
        db.add(new_drug)
        db.commit()
        db.refresh(new_drug)
        return {"message":"Product added successfully !", "success":True, "data":new_drug}
    else:
        return {"message":"Bir aylanib keling !"}
