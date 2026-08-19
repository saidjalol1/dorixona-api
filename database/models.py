from database.config import Base
from sqlalchemy import String, ForeignKey, Boolean, Integer, Float, DateTime, Column
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String(length=50), nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="cashier")

    checks = relationship("Check", back_populates="cashier")


class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True)
    name = Column(String, default="")
    amount = Column(Integer, default=0)
    base_price = Column(Float, default=0)
    sell_price = Column(Float, default=0)
    date_created = Column(DateTime, nullable=False)


class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, nullable=False)
    check_number = Column(String, nullable=False)
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Boolean, default=False)

    cashier = relationship("Users", back_populates="checks")
    items = relationship("CheckItem", back_populates="check")


class CheckItem(Base):
    __tablename__ = "check_items"

    id = Column(Integer, primary_key=True)
    drug_name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    check_id = Column(Integer, ForeignKey("checks.id"), nullable=False)

    check = relationship("Check", back_populates="items")