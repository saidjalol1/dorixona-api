from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from database.models import Users, Drug
from database.config import get_db
from database.schemas import DrugCreate , DrugEnter, DrugUpdateData

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


@drug_route.post("/drug-update-amount/")
def update_drug_amount(drug_data: DrugEnter,admin_id:int, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()

    if admin_user is None:
        raise  HTTPException(status_code=404, detail="Foydalanuvchi topilmadi ! Qayta login qiling!")

    if admin_user.role == "admin":
        drug = db.query(Drug).filter(Drug.id == drug_data.id).first()

        if drug is None:
            raise HTTPException(status_code=404, detail="Bu dori omborda mavjud emas !")
        
        drug.amount += drug_data.amount
        db.commit()
        db.refresh(drug)
        return {"message":"Dori malumoti yangilandi !", "success":True, "data":drug}
    else:
        raise HTTPException(status_code=401, detail="Siz uchun bu harakat taqiqlangan, Siz admin emassiz!")


@drug_route.get("/drugs/")
def drugs_get(user_id: int, db = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Login qilmagansiz!")

    drugs = db.query(Drug).all()
    return {"message":"Omborda mavjud bo'lgan dorilar ro'yxati", "success":True, "data":drugs}


@drug_route.put("/drug-update/")
def drug_update(admin_id:int, drug_data: DrugUpdateData, db=Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()

    if admin_user is None or admin_user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized user !")

    drug = db.query(Drug).filter(Drug.id == drug_data.id).first()
    if drug is None:
        raise HTTPException(status_code=404, detail="Not found !")

    new_drug_data = drug_data.model_dump(exclude_unset=True)

    for key, value in new_drug_data.items():
        setattr(drug, key, value)

    db.commit()
    db.refresh(drug)

    return {"message":"Updated Drug !", "success":True, "data":drug}


@drug_route.get("/drug/{drug_id}")
def get_drug(drug_id:int,user_id:int, db = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized access !")

    drug = db.query(Drug).filter(Drug.id == drug_id).first()

    if drug is None:
        raise HTTPException(status_code=404, detail="Data is not found !")

    return {"message":"Found the drug you requested !", "success":True, "data":drug}


@drug_route.get("/less-then/{amount}")
def get_less_drugs(amount:int,admin_id:int, db=Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()

    if admin_user is None or admin_user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized access !")

    drugs = db.query(Drug).filter(Drug.amount <= amount).all()
    return {"message":"Fetched all drugs !", "success":True, "data":drugs}
    