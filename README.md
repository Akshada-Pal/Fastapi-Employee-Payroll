# Employee & Payroll Management API

A RESTful API built using **Python, FastAPI, SQLAlchemy, and PostgreSQL** to manage employee records, departments, and payroll operations.

## Project Overview

The Employee & Payroll Management API simplifies employee administration and payroll management. It supports employee CRUD operations, department management, monthly payslip generation, salary calculations, and yearly payroll summaries.

## Features

* Employee CRUD operations (Create, Read, Update, Delete).
* Create and retrieve departments.
* Assign employees to departments.
* Retrieve employees by department.
* Identify bonus-eligible employees based on salary.
* Generate monthly employee payslips.
* Calculate net salary after deductions.
* Prevent duplicate payslips for the same employee, month, and year.
* Preserve historical payslips when an employee is deleted.
* Generate yearly payroll summaries.
* Validate requests and handle errors using HTTP status codes.
* Interactive API documentation using Swagger UI.

## Technologies Used

* **Python** — Programming language.
* **FastAPI** — REST API framework.
* **SQLAlchemy** — ORM for database operations.
* **PostgreSQL** — Relational database.
* **Pydantic** — Data validation and serialization.
* **Uvicorn** — ASGI server.
* **python-dotenv** — Environment variable management.
* **Swagger UI** — Interactive API documentation.

## Project Structure

```text
fastapi-employee-payroll/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── update_database.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

> Note: This structure assumes `update_database.py` still exists in your project. Adjust the tree to match your actual files before publishing.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd fastapi-employee-payroll
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your PostgreSQL connection string:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/employee_payroll_db
```

Replace `USERNAME` and `PASSWORD` with your PostgreSQL credentials.

**Important:** Never commit your `.env` file or expose your database password on GitHub.

### 6. Prepare the PostgreSQL Database

Make sure PostgreSQL is installed and running.

Create a database named:

```text
employee_payroll_db
```

Ensure the application's database tables have been created before starting to use the API. Follow the database initialization method implemented in your project.

### 7. Run the Application

```bash
uvicorn main:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

### 8. Open Swagger UI

Visit:

http://127.0.0.1:8000/docs

Use Swagger UI to interactively test the API endpoints.

## API Endpoints

| Method | Endpoint                                      | Description                                         |
| ------ | --------------------------------------------- | --------------------------------------------------- |
| GET    | `/`                                           | Display the welcome message                         |
| POST   | `/employees`                                  | Create an employee                                  |
| GET    | `/employees`                                  | Retrieve all employees                              |
| GET    | `/employees/{employee_id}`                    | Retrieve an employee by ID                          |
| PUT    | `/employees/{employee_id}`                    | Update employee details                             |
| DELETE | `/employees/{employee_id}`                    | Delete an employee while preserving payslip history |
| POST   | `/departments`                                | Create a department                                 |
| GET    | `/departments`                                | Retrieve all departments                            |
| GET    | `/departments/{department_id}`                | Retrieve a department by ID                         |
| GET    | `/departments/{department_id}/employees`      | Retrieve employees in a department                  |
| GET    | `/departments/{department_id}/bonus-eligible` | Retrieve bonus-eligible employees                   |
| POST   | `/payslips`                                   | Generate a monthly payslip                          |
| GET    | `/payslips`                                   | Retrieve all payslips                               |
| GET    | `/employees/{employee_id}/payslips`           | Retrieve an employee's payslips                     |
| GET    | `/employees/{employee_id}/payroll/{year}`     | Generate a yearly payroll summary                   |

## Payroll Calculation

Net salary is calculated using the following formula:

**Net Salary = Basic Salary − Deductions**

### Example

| Component      |      Amount |
| -------------- | ----------: |
| Basic Salary   |     ₹30,000 |
| Deductions     |      ₹3,000 |
| **Net Salary** | **₹27,000** |

## Database

The project uses **PostgreSQL** for persistent data storage and **SQLAlchemy** for database operations.

The database stores:

* Employee records.
* Department records.
* Monthly payslips.
* Salary and deduction information.

The application preserves historical payslip records when an employee is deleted by setting the associated employee reference to `NULL`, as configured in the database relationship.

## Testing

The API has been tested through Swagger UI.

The following functionality has been verified:

* Employee creation, retrieval, updating, and deletion.
* Department management.
* Payslip generation and salary calculation.
* Duplicate payslip prevention.
* Yearly payroll summaries.
* Bonus-eligible employee retrieval.
* Historical payslip preservation after employee deletion.
* Error handling for nonexistent employees and departments.

## Future Improvements

* User authentication and role-based access control.
* Automated monthly payroll processing.
* PDF payslip generation.
* Advanced payroll reports.
* Automated unit and integration tests.
* Cloud deployment.

## Author

**Akshada Vijay Pal**

Developed as a Python and FastAPI project to demonstrate REST API development, relational database integration, CRUD operations, and payroll management.




