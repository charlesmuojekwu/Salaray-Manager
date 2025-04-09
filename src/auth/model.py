from sqlmodel import SQLModel, Field,Column,String,Integer
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime,date
import uuid

class User(SQLModel, table=True):
    __tablename__ = 'users'
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    name: str
    email: str
    position:str
    join_date:date
    password_hash:str = Field(exclude=True)
    role:str
    department:str = Field( default=None, sa_column=Column(String, nullable=True))
    monthly_salary:int = Field( default=None, sa_column=Column(Integer, nullable=True))
    annual_salary:int = Field( default=None, sa_column=Column(Integer, nullable=True))
    photo_passport:str = Field( default=None, sa_column=Column(String, nullable=True))
    street_address:str = Field( default=None, sa_column=Column(String, nullable=True))
    city:str = Field( default=None, sa_column=Column(String, nullable=True))
    state:str = Field( default=None, sa_column=Column(String, nullable=True))
    zip_code:str = Field( default=None, sa_column=Column(String, nullable=True))
    country:str = Field( default=None, sa_column=Column(String, nullable=True))
    id_type:str = Field( default=None, sa_column=Column(String, nullable=True))
    id_image:str = Field( default=None, sa_column=Column(String, nullable=True))
    id_number:str = Field( default=None, sa_column=Column(String, nullable=True))
    id_issue_country:str = Field( default=None, sa_column=Column(String, nullable=True))
    id_issue_date:str = Field( default=None, sa_column=Column(String, nullable=True))
    id_expiry_date:str = Field( default=None, sa_column=Column(String, nullable=True))
    is_verified: bool = Field(default=False)
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    
    def __str__(self):
        return f"<User {self.name}>"