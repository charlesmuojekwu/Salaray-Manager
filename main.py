from fastapi import FastAPI, Header, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from employee_data import employees
from schemas import Employee, EmployeeUpdateModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/employees', response_description=list[Employee])
async def get_all_employee():
    return employees


@app.post('/create_employee', status_code=status.HTTP_201_CREATED, response_model=Employee) 
async def create_employee(employee_data: Employee):
    new_employee = employee_data.model_dump()
    employees.append(new_employee)
    return new_employee
    
    
@app.get("/employee/{employee_id}", status_code=status.HTTP_200_OK, response_model=Employee)
async def get_employee(employee_id:int) -> dict:
    for employee in employees:
        if employee['id'] == employee_id:
            return employee
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")


@app.patch("/employee/{employee_id}", status_code=status.HTTP_200_OK)
async def update_employee(employee_id:int,  employee_update_data:EmployeeUpdateModel) -> dict:
    for employee in employees:
        if employee['id'] == employee_id:
            employee['name'] = employee_update_data.name
            employee['email'] = employee_update_data.email
            employee['position'] =  employee_update_data.position
            employee['role'] =  employee_update_data.role
            employee['department'] =    employee_update_data.department
            return employee
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")


@app.delete("/employee/{employee_id}", status_code=status.HTTP_200_OK)
async def delet_employee(employee_id:int):
    for employee in employees:
        if employee['id'] == employee_id:
            employees.remove(employee) 
            return {}
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Employee not found")