from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from database import Base


# ==================================================
# DEPARTMENT MODEL
# ==================================================

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    manager_name = Column(String, nullable=False)

    employees = relationship(
        "Employee",
        back_populates="department"
    )


# ==================================================
# EMPLOYEE MODEL
# ==================================================

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    salary = Column(Float, nullable=False)
    joining_date = Column(Date, nullable=False)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True
    )

    department = relationship(
        "Department",
        back_populates="employees"
    )

    payslips = relationship(
        "Payslip",
        back_populates="employee"
    )


# ==================================================
# PAYSLIP MODEL
# ==================================================

class Payslip(Base):
    __tablename__ = "payslips"

    # Prevent duplicate payslips for the same employee,
    # month, and year.
    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "month",
            "year",
            name="unique_employee_month_year"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey(
            "employees.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    basic_salary = Column(Float, nullable=False)

    deductions = Column(
        Float,
        default=0.0,
        nullable=False
    )

    net_salary = Column(Float, nullable=False)

    employee = relationship(
        "Employee",
        back_populates="payslips"
    )