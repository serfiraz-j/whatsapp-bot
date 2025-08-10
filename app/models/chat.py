import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True)
    customer_phone = Column(String, index=True)
    clinic_id = Column(Integer, ForeignKey("clinic.id"))
    
    clinic = relationship("Clinic", back_populates="chat_histories")
    messages = relationship("Message", back_populates="chat_history", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False) # 'user' or 'assistant'
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    chat_history_id = Column(Integer, ForeignKey("chat_history.id"))
    
    chat_history = relationship("ChatHistory", back_populates="messages")
