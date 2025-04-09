from fastapi import APIRouter, status, Depends, Query
from fastapi.exceptions import HTTPException
from typing import Optional, List
from src.employee.service import EmployeeService
from src.employee.schemas import Employee, EmployeeUpdateModel,EmployeeCreateModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from ..utils.responses import success, error, paginated_response
from ..utils.base_response import SuccessResponse, PaginatedResponse
from src.auth.dependencies import AccessTokenBearer

employee_router = APIRouter()
employee_service = EmployeeService()
access_token_bearer = AccessTokenBearer()


@employee_router.get('/', summary="List employees", response_model=PaginatedResponse[Employee], status_code=status.HTTP_200_OK)
async def get_all_employee(
    employee_list= Depends(access_token_bearer),
    session:AsyncSession = Depends(get_session), 
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1)
):
    employees, total = await employee_service.get_all_employees(session, page, size)
    return paginated_response(data=employees, total=total, page=page, size=size)



@employee_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=SuccessResponse[Employee]) 
async def create_employee(employee_data: EmployeeCreateModel, session:AsyncSession = Depends(get_session)):
    new_employee = await employee_service.create_employee(employee_data, session)
    return success(data=new_employee, message="Employee Created successfully", status_code=status.HTTP_201_CREATED)

    
    
@employee_router.get("/{employee_uid}", status_code=status.HTTP_200_OK, response_model=SuccessResponse[Employee])
async def get_employee(employee_uid:UUID, session:AsyncSession = Depends(get_session)) -> dict:
    employee = await employee_service.get_employee(employee_uid, session)
    if employee is not None:
        return success(data=employee, message="Employee retrieved successfully")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")


@employee_router.patch("/{employee_uid}", status_code=status.HTTP_200_OK, response_model=SuccessResponse[EmployeeUpdateModel])
async def update_employee(employee_uid:UUID, employee_update_data:EmployeeUpdateModel, session:AsyncSession = Depends(get_session)) -> dict:
    updated_employee = await employee_service.update_employee(employee_uid, employee_update_data, session)
    if updated_employee:
        return success(data=updated_employee, message="Employee Updated successfully")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")


@employee_router.delete("/{employee_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_uid:UUID, session:AsyncSession = Depends(get_session)):
    delete_employee = await employee_service.delete_employee(employee_uid, session)
    if delete_employee:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")