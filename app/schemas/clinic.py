from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ClinicBase(BaseModel):
    name: str
    ai_tone: Optional[str] = "professional and friendly"
    ai_language: Optional[str] = "English"

class ClinicCreate(ClinicBase):
    pass

class Clinic(ClinicBase):
    id: int
    owner_id: int
    services: List[Service] = []
    model_config = ConfigDict(from_attributes=True)