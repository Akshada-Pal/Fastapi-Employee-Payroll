from pydantic import BaseModel, Field
from datetime import date


# Employee Schemas
class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: str
    salary: float = Field(..., gt=0)
    joining_date: date
    department_id: int | None = None


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    salary: float
    joining_date: date
    department_id: int | None = None

    class Config:
        from_attributes = True


# Department Schemas
class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=2)
    manager_name: str = Field(..., min_length=2)


class DepartmentResponse(BaseModel):
    id: int
    name: str
    manager_name: str

    class Config:
        from_attributes = True


# Payslip Schemas
class PayslipCreate(BaseModel):
    employee_id: int
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2100)
    deductions: float = Field(default=0.0, ge=0)


class PayslipResponse(BaseModel):
    id: int
    employee_id: int | None = None
    month: int
    year: int
    basic_salary: float
    deductions: float
    net_salary: float

    class Config:
        from_attributes = True