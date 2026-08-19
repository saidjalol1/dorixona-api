from fastapi import FastAPI, Depends, HTTPException
from database.models import Base, Users
from database.config import engine, get_db
from database.schemas import UserData

app = FastAPI()

Base.metadata.create_all(engine)


@app.get("/")
def welcome():
    return {"message": "Welcome to our app"}


#
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

@app.get("/users")
def get_users(db=Depends(get_db)):
    users = db.query(Users).all()

    return {
        "message": "Fetched Users!",
        "data": users,
        "success": True
    }


@app.get("/users/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Fetched User!",
        "data": user,
        "success": True
    }


@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserData,
    db=Depends(get_db)
):
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.username = user_data.username
    user.password = user_data.password
    user.full_name = user_data.full_name
    user.role = user_data.role

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated!",
        "data": user,
        "success": True
    }


#
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db=Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted!",
        "success": True
    }



