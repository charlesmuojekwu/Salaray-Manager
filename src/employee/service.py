from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import EmployeeCreateModel, EmployeeUpdateModel
from sqlmodel import select, desc, func
from ..auth.model import User
from ..employee_agreement.models import EmployeeAgreement
from datetime import datetime
from typing import List, Tuple


class EmployeeService:
    async def get_all_employees(self, session:AsyncSession, page: int = 1, size: int = 10) -> Tuple[List[User], int]:

        offset = (page - 1) * size

        # 1. Get total count of employees
        total_stmt = select(func.count()).select_from(User)
        total = (await session.execute(total_stmt)).scalar()

        # 2. Get paginated employee records
        statement = select(User).order_by(desc(User.created_at)).offset(offset).limit(size)
        result = await session.exec(statement)
        employees = result.all() 

        return employees, total
    
    
    async def get_employee(self, user_uid:str, session:AsyncSession):
        statement = select(User).where(User.uid == user_uid)
        result = await session.exec(statement)
        employee = result.first()
        return employee if employee is not None else None
    
    
    
    async def update_employee(self, user_uid:str, update_data:EmployeeUpdateModel, session:AsyncSession):
        employee_to_update = await self.get_employee(user_uid, session)
        if employee_to_update is not None:
            update_data_dict = update_data.model_dump()
            for key, value in update_data_dict.items():
                setattr(employee_to_update, key, value)
            await session.commit()
            return employee_to_update
        else:
            return None

    
    async def delete_employee(self, user_uid:str, session:AsyncSession):
        employee_to_delete = await self.get_employee(user_uid, session)
        if employee_to_delete is not None:
            await session.delete(employee_to_delete)
            await session.commit()
            return True
        else:
            return None
        
     # Agreement   
    async def get_employee_agreement(self, user_uid:str, session:AsyncSession):
        statement = select(EmployeeAgreement).where(EmployeeAgreement.user_uuid == user_uid)
        result = await session.exec(statement)
        employee = result.all()
        return employee if employee is not None else None
    