from sqlalchemy import inspect, text
from database import engine

inspector = inspect(engine)

columns = [
    column["name"]
    for column in inspector.get_columns("employees")
]

if "department_id" not in columns:
    with engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE employees "
                "ADD COLUMN department_id INTEGER "
                "REFERENCES departments(id)"
            )
        )

    print("department_id column added successfully!")

else:
    print("department_id column already exists!")

    