from pydantic import BaseModel
from typing import Optional
from enum import Enum

ADMIN = "admin"
class UserRole(Enum):
    ADMIN = "admin"
    CASHIER = "cashier"

    
class UserData(BaseModel):
    username: str
    password: str
    full_name: str
    role: str = "cashier"

class UserUpdate(BaseModel):
    id : int
    username: str | None = None
    full_name : str | None = None
    password: str | None = None
    role : str | None = None


class DrugCreate(BaseModel):
    name : str
    amount: int
    base_price: float
    sell_price: float 


class DrugEnter(BaseModel):
    id : int
    amount : int

class DrugUpdateData(BaseModel):
    id : int
    name: str | None = None
    base_price : float | None = None
    sell_price : float | None = None