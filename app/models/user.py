from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True)
    clinic = relationship("Clinic", back_populates="owner", uselist=False)