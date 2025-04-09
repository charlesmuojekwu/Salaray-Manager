from pydantic import BaseModel, Field
from datetime import datetime,date
import uuid

   
class UserCreateModel(BaseModel):
    name: str = Field(max_length=200)
    email: str = Field(max_length=100)
    position:str
    join_date:str
    password:str = Field(min_length=6)
    role:str
    department:str
    
class UserModel(BaseModel):
    uid: uuid.UUID
    name: str
    email: str
    position:str
    role:str
    department:str
    created_at:datetime
    updated_at:datetime
    
    
class UserLoginModel(BaseModel):
    email: str
    password:str = Field(min_length=6)
       
class UserAuthenticatedModel(BaseModel):
    access_token: str
    refresh_token: str
    user: UserModel
    