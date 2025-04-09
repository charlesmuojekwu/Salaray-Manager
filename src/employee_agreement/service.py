from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import EmployeeAgreementCreateModel, EmployeeAgreementUpdateModel
from sqlmodel import select, desc, func
from .models import EmployeeAgreement
from datetime import datetime
from typing import List, Tuple


class EmployeeAgreementService:
    async def get_all_employees(self, session:AsyncSession, page: int = 1, size: int = 10) -> Tuple[List[EmployeeAgreement], int]:

        offset = (page - 1) * size

        # 1. Get total count of employees
        total_stmt = select(func.count()).select_from(EmployeeAgreement)
        total = (await session.execute(total_stmt)).scalar()

        # 2. Get paginated employee records
        statement = select(EmployeeAgreement).order_by(desc(EmployeeAgreement.created_at)).offset(offset).limit(size)
        result = await session.exec(statement)
        employees = result.all() 

        return employees, total
    
    
    async def get_employee(self, employee_uid:str, session:AsyncSession):
        statement = select(EmployeeAgreement).where(EmployeeAgreement.uid == employee_uid)
        result = await session.exec(statement)
        employee = result.first()
        return employee if employee is not None else None
    
    
    async def create_employee(self, employee_data:EmployeeAgreementCreateModel, session:AsyncSession):
        employee_data_dict = employee_data.model_dump()
        new_employee = EmployeeAgreement(
            **employee_data_dict
        )
        new_employee.effective_date = datetime.strptime(employee_data_dict['effective_date'], "%Y-%m-%d")
        session.add(new_employee)
        await session.commit()
        return new_employee
    
    
    async def update_employee(self, employee_uid:str, update_data:EmployeeAgreementUpdateModel, session:AsyncSession):
        employee_to_update = await self.get_employee(employee_uid, session)
        if employee_to_update is not None:
            update_data_dict = update_data.model_dump()
            for key, value in update_data_dict.items():
                setattr(employee_to_update, key, value)
            await session.commit()
            return employee_to_update
        else:
            return None

    
    async def delete_employee(self, employee_uid:str, session:AsyncSession):
        employee_to_delete = await self.get_employee(employee_uid, session)
        if employee_to_delete is not None:
            await session.delete(employee_to_delete)
            await session.commit()
            return True
        else:
            return None