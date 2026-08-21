from fastapi import FastAPI, Depends, HTTPException
from database.models import Base, Users
from database.config import engine, get_db
from database.schemas import UserData, UserUpdate

from routes.drugs_route import drug_route

app = FastAPI()

app.include_router(drug_route)

Base.metadata.create_all(engine)


@app.get("/")
def welcome():
    return {"message": "Welcome to our app"}


@app.post("/register/")
def user_register(user_data: UserData, db=Depends(get_db)):
    try:
        new_user = Users(**user_data.model_dump())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Created User!",
            "data": new_user,
            "success": True
        }

    except Exception as error:
        db.rollback()
        return {
            "message": "Error occurred!",
            "success": False,
            "error": str(error)
        }


@app.get("/users/")
def get_all_users(user_id: int, db = Depends(get_db)):
    reqeusting_user = db.query(Users).filter(Users.id == user_id).first()
    if reqeusting_user.role == "admin":
        users = db.query(Users).all()
        return {"message":"User accounts fetched successfully !", "success":True, "data":users}
    else:
        return {"message":"You have no access to this route ! becouse you have not admin rights !", "success":False, "data":{}}


@app.delete("/user-delete/")
def delete_user(delete_user_id: int,admin_user_id: int,  db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_user_id).first()
    if admin_user.role == "admin":
        delete_user = db.query(Users).filter(Users.id == delete_user_id).first()
        db.delete(delete_user)
        db.commit()
        return {"message":"User deleted Successfully !", "success":True}
    else:
        return {"message":"You have no access to this route !, you are not admin"}

@app.put("/user-account-update/")
def account_update(admin_id:int,user_data: UserUpdate, db = Depends(get_db)):
    admin_user = db.query(Users).filter(Users.id == admin_id).first()
    if admin_user.role == "admin":
        user = db.query(Users).filter(Users.id == user_data.id).first()

        new_user = user_data.model_dump(exclude_unset=True)
        
        for key, value in new_user.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        
        return {"message":"User updated!", "success":True, "data":user}
    else:
        return {"message":"You have no access to this route !"}