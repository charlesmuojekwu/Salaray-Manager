from pydantic import BaseModel
from datetime import datetime,date
import uuid

class EmployeeAgreement(BaseModel):
    uid: uuid.UUID
    user_uuid: str
    title: str
    description: str
    status: str
    effective_date: date
    document: str
    created_at:datetime
    updated_at:datetime
    
class EmployeeAgreementCreateModel(BaseModel):
    user_uuid: str
    title: str
    description: str
    status: str
    effective_date: str
    document: str
    
class EmployeeAgreementUpdateModel(BaseModel):
    user_uuid: str
    title: str
    description: str
    status: str
    effective_date: str
    document: str

