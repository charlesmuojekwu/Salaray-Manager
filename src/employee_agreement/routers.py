from fastapi import APIRouter, status, Depends, Query
from fastapi.exceptions import HTTPException
from typing import Optional, List
from src.employee_agreement.service import EmployeeAgreementService
from src.employee_agreement.schemas import EmployeeAgreement, EmployeeAgreementCreateModel, EmployeeAgreementUpdateModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from ..utils.responses import success, error, paginated_response
from ..utils.base_response import SuccessResponse, PaginatedResponse
from src.auth.dependencies import AccessTokenBearer

employee_agreement_router = APIRouter()
employee_agreement_service = EmployeeAgreementService()
access_token_bearer = AccessTokenBearer()


@employee_agreement_router.get('/', summary="List employees Agreement", response_model=PaginatedResponse[EmployeeAgreement], status_code=status.HTTP_200_OK)
async def get_all_employee(
    #employee_list= Depends(access_token_bearer),
    session:AsyncSession = Depends(get_session), 
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1)
):
    employees, total = await employee_agreement_service.get_all_employees(session, page, size)
    return paginated_response(data=employees, total=total, page=page, size=size)



@employee_agreement_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=SuccessResponse[EmployeeAgreement]) 
async def create_employee(employee_data: EmployeeAgreementCreateModel, session:AsyncSession = Depends(get_session)):
    new_employee = await employee_agreement_service.create_employee(employee_data, session)
    return success(data=new_employee, message="Employee Agreement Created successfully", status_code=status.HTTP_201_CREATED)

    
    
@employee_agreement_router.get("/{employee_uid}", status_code=status.HTTP_200_OK, response_model=SuccessResponse[EmployeeAgreement])
async def get_employee(employee_uid:UUID, session:AsyncSession = Depends(get_session)) -> dict:
    employee = await employee_agreement_service.get_employee(employee_uid, session)
    if employee is not None:
        return success(data=employee, message="Employee Agreement retrieved successfully")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee Agreement not found")


@employee_agreement_router.patch("/{employee_uid}", status_code=status.HTTP_200_OK, response_model=SuccessResponse[EmployeeAgreementUpdateModel])
async def update_employee(employee_uid:UUID, employee_update_data:EmployeeAgreementUpdateModel, session:AsyncSession = Depends(get_session)) -> dict:
    updated_employee = await employee_agreement_service.update_employee(employee_uid, employee_update_data, session)
    if updated_employee:
        return success(data=updated_employee, message="Employee Agreement Updated successfully")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee Agreement not found")


@employee_agreement_router.delete("/{employee_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_uid:UUID, session:AsyncSession = Depends(get_session)):
    delete_employee = await employee_agreement_service.delete_employee(employee_uid, session)
    if delete_employee:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee Agreement not found")