from fastapi import APIRouter, status, Depends, Query
from fastapi.exceptions import HTTPException
from typing import Optional, List
from src.employee.service import EmployeeService
from src.employee.schemas import Employee, EmployeeUpdateModel,EmployeeCreateModel
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel, UserAuthenticatedModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from ..utils.responses import success, error, paginated_response
from ..utils.base_response import SuccessResponse, PaginatedResponse
from src.auth.dependencies import AccessTokenBearer
from fastapi.responses import JSONResponse
from src.employee_agreement.schemas import EmployeeAgreement

employee_router = APIRouter()
employee_service = EmployeeService()
access_token_bearer = AccessTokenBearer()




## Employee
@employee_router.get('/dashboard', summary="dashboard", status_code=status.HTTP_200_OK)
async def employee_dashboard():
    data = {
        "current_salary":0,
        "next_payment":None,
        "tasks":0
    }
    return success(data=data, message="Employee dashboard")


@employee_router.get('/profile', summary="profile", status_code=status.HTTP_200_OK, response_model=SuccessResponse[Employee])
async def employee_profile(session:AsyncSession = Depends(get_session)):
    return await get_employee("4f030934-4657-442e-9a9c-df07b8c3e721", session)


@employee_router.get('/salary', summary="salary", status_code=status.HTTP_200_OK)
async def employee_dashboard():
    data = {
        "current_salary":0,
        "monthly_salary":0,
        "base_salary":0,
        "annual_salary":0,
        "payment_history":[]
    }
    return success(data=data, message="Employee salary")
    
@employee_router.get('/agreement', summary="agreement", status_code=status.HTTP_200_OK, response_model=SuccessResponse[List[EmployeeAgreement]])
async def employee_agreement(session:AsyncSession = Depends(get_session)):
    employee_agreement = await employee_service.get_employee_agreement("John Doe", session)
    if employee_agreement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee Agreement not found")
    else:
        return success(data=employee_agreement, message="Employee Agreement")






@employee_router.get('/', summary="List employees", response_model=PaginatedResponse[UserModel], status_code=status.HTTP_200_OK)
async def get_all_employee(
    #employee_list= Depends(access_token_bearer),
    session:AsyncSession = Depends(get_session), 
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1)
):
    employees, total = await employee_service.get_all_employees(session, page, size)
    return paginated_response(data=employees, total=total, page=page, size=size)


@employee_router.get("/{user_uid}", status_code=status.HTTP_200_OK, response_model=SuccessResponse[Employee])
async def get_employee(user_uid:UUID, session:AsyncSession = Depends(get_session)):
    employee = await employee_service.get_employee(user_uid, session)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    else:
        data = {
            **employee.model_dump(),
            'current_salary':employee.monthly_salary,
            'address' :{
                "street_address": employee.street_address,
                "city": employee.city,
                "state": employee.state,
                "zip_code": employee.zip_code,
                "country": employee.country,
            },
            'passport':{
                "id_image":employee.id_image,
                "id_number": employee.id_number,
                "id_issue_country": employee.id_issue_country,
                "id_issue_date": employee.id_issue_date,
                "id_expiry_date": employee.id_expiry_date,
            }
        }
        return success(data=data, message="Employee retrieved successfully")


@employee_router.patch("/{user_uid}", status_code=status.HTTP_200_OK, response_model=SuccessResponse[EmployeeUpdateModel])
async def update_employee(user_uid:UUID, employee_update_data:EmployeeUpdateModel, session:AsyncSession = Depends(get_session)) -> dict:
    updated_employee = await employee_service.update_employee(user_uid, employee_update_data, session)
    if updated_employee:
        return success(data=updated_employee, message="Employee Updated successfully")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")


@employee_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(user_uid:UUID, session:AsyncSession = Depends(get_session)):
    delete_employee = await employee_service.delete_employee(user_uid, session)
    if delete_employee:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")