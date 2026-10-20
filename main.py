from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import engine, Base, SessionLocal
import models
import schemas

app = FastAPI(
    title="Employee & Payroll Management API",
    description="An API to manage employees, departments, and payroll.",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)


# Database Connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================================================
# HOME ENDPOINT
# ==================================================

@app.get("/")
def home():
    return {
        "message": "Employee & Payroll Management API is running!"
    }


# ==================================================
# EMPLOYEE ENDPOINTS
# ==================================================

@app.post(
    "/employees",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing_employee = db.query(models.Employee).filter(
        models.Employee.email == employee.email
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An employee with this email already exists."
        )

    if employee.department_id is not None:
        department = db.query(models.Department).filter(
            models.Department.id == employee.department_id
        ).first()

        if department is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found."
            )

    new_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        salary=employee.salary,
        joining_date=employee.joining_date,
        department_id=employee.department_id
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


@app.get(
    "/employees",
    response_model=list[schemas.EmployeeResponse]
)
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()


@app.get(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    return employee


@app.put(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse
)
def update_employee(
    employee_id: int,
    updated_data: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    existing_email = db.query(models.Employee).filter(
        models.Employee.email == updated_data.email,
        models.Employee.id != employee_id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already used by another employee."
        )

    if updated_data.department_id is not None:
        department = db.query(models.Department).filter(
            models.Department.id == updated_data.department_id
        ).first()

        if department is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found."
            )

    employee.name = updated_data.name
    employee.email = updated_data.email
    employee.salary = updated_data.salary
    employee.joining_date = updated_data.joining_date
    employee.department_id = updated_data.department_id

    db.commit()
    db.refresh(employee)

    return employee


@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    # Preserve historical payslips
    db.query(models.Payslip).filter(
        models.Payslip.employee_id == employee_id
    ).update(
        {models.Payslip.employee_id: None},
        synchronize_session=False
    )

    db.delete(employee)
    db.commit()

    return {
        "message": (
            "Employee deleted successfully. "
            "Historical payslips have been preserved."
        ),
        "employee_id": employee_id
    }




# ==================================================
# DEPARTMENT ENDPOINTS
# ==================================================

@app.post(
    "/departments",
    response_model=schemas.DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db)
):
    existing_department = db.query(models.Department).filter(
        models.Department.name == department.name
    ).first()

    if existing_department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This department already exists."
        )

    new_department = models.Department(
        name=department.name,
        manager_name=department.manager_name
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


@app.get(
    "/departments",
    response_model=list[schemas.DepartmentResponse]
)
def get_all_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()


@app.get(
    "/departments/{department_id}",
    response_model=schemas.DepartmentResponse
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = db.query(models.Department).filter(
        models.Department.id == department_id
    ).first()

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found."
        )

    return department


# ==================================================
# PAYROLL ENDPOINTS
# ==================================================

@app.post(
    "/payslips",
    response_model=schemas.PayslipResponse,
    status_code=status.HTTP_201_CREATED
)
def generate_payslip(
    payslip_data: schemas.PayslipCreate,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.id == payslip_data.employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    existing_payslip = db.query(models.Payslip).filter(
        models.Payslip.employee_id == payslip_data.employee_id,
        models.Payslip.month == payslip_data.month,
        models.Payslip.year == payslip_data.year
    ).first()

    # print("DEBUG: Existing payslip =", existing_payslip)

    if existing_payslip:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payslip already exists for this employee and month."
        )

    basic_salary = employee.salary
    deductions = payslip_data.deductions

    if deductions > basic_salary:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deductions cannot exceed the basic salary."
        )

    net_salary = basic_salary - deductions

    new_payslip = models.Payslip(
        employee_id=employee.id,
        month=payslip_data.month,
        year=payslip_data.year,
        basic_salary=basic_salary,
        deductions=deductions,
        net_salary=net_salary
    )

    db.add(new_payslip)

    try:
        db.commit()
        db.refresh(new_payslip)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payslip already exists for this employee and month."
        )

    return new_payslip

# ==================================================
# PAYSLIP QUERY ENDPOINTS
# ==================================================

# Get all payslips
@app.get(
    "/payslips",
    response_model=list[schemas.PayslipResponse]
)
def get_all_payslips(db: Session = Depends(get_db)):
    return db.query(models.Payslip).order_by(
        models.Payslip.year.desc(),
        models.Payslip.month.desc()
    ).all()


# Get payslip history for a specific employee
@app.get(
    "/employees/{employee_id}/payslips",
    response_model=list[schemas.PayslipResponse]
)
def get_employee_payslips(
    employee_id: int,
    db: Session = Depends(get_db)
):
    # Check whether the employee exists
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    # Get the employee's payslips
    payslips = db.query(models.Payslip).filter(
        models.Payslip.employee_id == employee_id
    ).order_by(
        models.Payslip.year.desc(),
        models.Payslip.month.desc()
    ).all()

    return payslips

# Get employees by department
@app.get(
    "/departments/{department_id}/employees",
    response_model=list[schemas.EmployeeResponse]
)
def get_employees_by_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    # Check whether the department exists
    department = db.query(models.Department).filter(
        models.Department.id == department_id
    ).first()

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found."
        )

    # Get employees belonging to the department
    employees = db.query(models.Employee).filter(
        models.Employee.department_id == department_id
    ).all()

    return employees

# Get yearly payroll report for an employee
@app.get("/employees/{employee_id}/payroll/{year}")
def get_yearly_payroll_report(
    employee_id: int,
    year: int,
    db: Session = Depends(get_db)
):
    # Check whether the employee exists
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    # Get payslips for the selected year
    payslips = db.query(models.Payslip).filter(
        models.Payslip.employee_id == employee_id,
        models.Payslip.year == year
    ).all()

    if not payslips:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No payslips found for this employee and year."
        )

    # Calculate yearly totals
    total_basic_salary = sum(
        payslip.basic_salary for payslip in payslips
    )

    total_deductions = sum(
        payslip.deductions for payslip in payslips
    )

    total_net_salary = sum(
        payslip.net_salary for payslip in payslips
    )

    return {
        "employee_id": employee_id,
        "employee_name": employee.name,
        "year": year,
        "total_payslips": len(payslips),
        "total_basic_salary": total_basic_salary,
        "total_deductions": total_deductions,
        "total_net_salary": total_net_salary
    }

# Filter employees by department and minimum salary
@app.get("/departments/{department_id}/bonus-eligible")
def get_bonus_eligible_employees(
    department_id: int,
    min_salary: float = 40000,
    db: Session = Depends(get_db)
):
    # Check whether the department exists
    department = db.query(models.Department).filter(
        models.Department.id == department_id
    ).first()

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found."
        )

    # Find employees who meet the salary requirement
    employees = db.query(models.Employee).filter(
        models.Employee.department_id == department_id,
        models.Employee.salary >= min_salary
    ).all()

    return {
        "department": department.name,
        "minimum_salary": min_salary,
        "eligible_employee_count": len(employees),
        "employees": [
            {
                "id": employee.id,
                "name": employee.name,
                "salary": employee.salary
            }
            for employee in employees
        ]
    }

