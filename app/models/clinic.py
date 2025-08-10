from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Clinic(Base):
    __tablename__ = "clinic"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), unique=True)
    
    # AI Customization
    ai_tone = Column(String, default="professional and friendly")
    ai_language = Column(String, default="English")
    
    owner = relationship("User", back_populates="clinic")
    services = relationship("Service", back_populates="clinic", cascade="all, delete-orphan")
    chat_histories = relationship("ChatHistory", back_populates="clinic", cascade="all, delete-orphan")

class Service(Base):
    __tablename__ = "service"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(String) # Using string to accommodate various formats like "$50" or "Contact for quote"
    clinic_id = Column(Integer, ForeignKey("clinic.id"))
    
    clinic = relationship("Clinic", back_populates="services")
