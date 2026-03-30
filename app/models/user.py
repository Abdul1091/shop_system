from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    OWNER = "owner"
    CASHIER = "cashier"
    STAFF = "staff"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STAFF)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)