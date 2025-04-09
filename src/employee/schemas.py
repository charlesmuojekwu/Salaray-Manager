from pydantic import BaseModel
from datetime import datetime,date
import uuid
from typing import Optional



class EmployeeAddress(BaseModel):
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    
class EmployeeIdInfo(BaseModel):
    id_image: Optional[str] = None
    id_number: Optional[str] = None
    id_issue_country: Optional[str] = None
    id_issue_date: Optional[str] = None
    id_expiry_date: Optional[str] = None

class Employee(BaseModel):
    uid: uuid.UUID
    name: str
    email: str
    position:str
    join_date:date
    role:str
    department:str
    monthly_salary: Optional[str] = None
    annual_salary: Optional[str] = None
    current_salary: Optional[str] = None
    address: Optional[EmployeeAddress] = None
    passport: Optional[EmployeeIdInfo] = None
    created_at:datetime
    updated_at:datetime
    
class EmployeeCreateModel(BaseModel):
    name: str
    email: str
    position:str
    join_date:str
    password:str
    role:str
    department:str
    
class EmployeeUpdateModel(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    join_date:Optional[date] = None
    position:Optional[str] = None
    role:Optional[str] = None
    department:Optional[str] = None
    monthly_salary: Optional[str] = None
    annual_salary: Optional[str] = None
    current_salary: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    id_image: Optional[str] = None
    id_number: Optional[str] = None
    id_issue_country: Optional[str] = None
    id_issue_date: Optional[str] = None
    id_expiry_date: Optional[str] = None
    


