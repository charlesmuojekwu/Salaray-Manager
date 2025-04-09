from sqlmodel import SQLModel, Field, Column, Text,String
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime,date
import uuid

class EmployeeAgreement(SQLModel, table=True):
    __tablename__ = "employee_agreements"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    user_uuid:str   
    title: str  
    description: str = Field(default=None, sa_column=Column(Text, nullable=True))
    status:str = Field( default=None, sa_column=Column(String, nullable=True))
    effective_date:date
    document:str = Field( default=None, sa_column=Column(String, nullable=True))
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    
    def __str__(self):
        return f"<Employee_agreement {self.name}>"