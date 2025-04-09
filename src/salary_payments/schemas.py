from pydantic import BaseModel
from datetime import datetime,date
import uuid

class Employee(BaseModel):
    uid: uuid.UUID
    name: str
    email: str
    position:str
    join_date:date
    password:str
    role:str
    department:str
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
    name: str
    email: str
    join_date:date
    position:str
    role:str
    department:str

