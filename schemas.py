from pydantic import BaseModel

class Employee(BaseModel):
    id: str
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
    position:str
    role:str
    department:str

