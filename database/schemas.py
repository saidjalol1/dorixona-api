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
    