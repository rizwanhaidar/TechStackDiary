import pandas as pd
import uuid
from faker import Faker
import pyodbc
import random
from datetime import datetime

# Initialize Faker
fake = Faker()

# Define valid date range for SQL Server datetime
SQL_SERVER_MIN_DATE = datetime(1753, 1, 1)
SQL_SERVER_MAX_DATE = datetime(9999, 12, 31)

# Function to generate a valid date within SQL Server's range
def generate_valid_date(start_date="-5y", end_date="now"):
    """
    Generates a date within SQL Server's valid datetime range.
    """
    date = fake.date_time_between(start_date=start_date, end_date=end_date)
    return max(SQL_SERVER_MIN_DATE, min(SQL_SERVER_MAX_DATE, date))

# Constants
NUM_STORES = 300
NUM_STORE_MANAGERS = NUM_STORES
NUM_ASSOCIATE_MANAGERS = NUM_STORES * 2
NUM_DEPARTMENT_HEADS = NUM_STORES * 8
NUM_GENERAL_EMPLOYEES = 15000 - (NUM_STORE_MANAGERS + NUM_ASSOCIATE_MANAGERS + NUM_DEPARTMENT_HEADS)

# Generate Stores
def generate_stores(num_stores):
    """
    Generates store data with unique store_id, opening_date, and optional closing_date.
    """
    stores = []
    for _ in range(num_stores):
        opening_date = generate_valid_date(start_date="-5y", end_date="now")
        is_active = fake.boolean(chance_of_getting_true=80)  # 80% chance of being active
        closing_date = generate_valid_date(start_date=opening_date, end_date="now") if not is_active else None

        stores.append({
            "store_id": str(uuid.uuid4()),  # Unique UUID for each store
            "store_name": fake.company(),  # Random store name
            "address": fake.address().replace("\n", ", "),  # Random address
            "city": fake.city(),  # Random city
            "state": fake.state(),  # Random state
            "country": fake.country(),  # Random country
            "postal_code": fake.postcode(),  # Random postal code
            "manager_id": None,  # Will be assigned later
            "contact_email": fake.email(),  # Random contact email
            "contact_phone": fake.phone_number(),  # Random contact phone number
            "opening_date": opening_date,  # Random opening date
            "store_closing_date": closing_date,  # Closing date (NULL if active)
            "is_active": is_active
            # ,  # Active flag
            # "created_at": generate_valid_date(start_date="-5y", end_date="now"),  # Random creation date
            # "updated_at": generate_valid_date(start_date="-5y", end_date="now")  # Random update date
        })
    return pd.DataFrame(stores)

# Generate Employees with Hierarchy
def generate_employees(stores_df):
    """
    Generates employee data with a strict hierarchy:
    - Store Manager → Associate Managers → Department Heads → General Employees
    """
    store_managers = []
    associate_managers = []
    department_heads = []
    general_employees = []

    for _, store in stores_df.iterrows():
        store_id = store["store_id"]

        # Store Manager (1 per store)
        store_manager = {
            "employee_id": str(uuid.uuid4()),  # Unique UUID for each employee
            "store_id": store_id,
            "first_name": fake.first_name(),  # Random first name
            "last_name": fake.last_name(),  # Random last name
            "role": "Store Manager",  # Role as Store Manager
            "superior_id": None,  # No superior (top of the hierarchy)
            "hire_date": generate_valid_date(start_date="-5y", end_date="now"),  # Random hire date
            "salary": round(fake.random_number(digits=5) + fake.random_number(digits=2) / 100, 2)
            #,  # Random salary
            #"created_at": generate_valid_date(start_date="-5y", end_date="now"),  # Random creation date
            #"updated_at": generate_valid_date(start_date="-5y", end_date="now")  # Random update date
        }
        store_managers.append(store_manager)
        manager_id = store_manager["employee_id"]

        # Associate Managers (2 per store)
        for _ in range(2):
            assoc_manager = {
                "employee_id": str(uuid.uuid4()),
                "store_id": store_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "role": "Store Associate Manager",  # Role as Associate Manager
                "superior_id": manager_id,  # Reports to Store Manager
                "hire_date": generate_valid_date(start_date="-5y", end_date="now"),
                "salary": round(fake.random_number(digits=5) + fake.random_number(digits=2) / 100, 2)
                #,
                #"created_at": generate_valid_date(start_date="-5y", end_date="now"),
                #"updated_at": generate_valid_date(start_date="-5y", end_date="now")
            }
            associate_managers.append(assoc_manager)

        # Department Heads (4 per Associate Manager → 8 per store)
        for assoc_manager in associate_managers[-2:]:  # Last 2 Associate Managers
            for _ in range(4):
                dept_head = {
                    "employee_id": str(uuid.uuid4()),
                    "store_id": store_id,
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "role": "Department Head",  # Role as Department Head
                    "superior_id": assoc_manager["employee_id"],  # Reports to Associate Manager
                    "hire_date": generate_valid_date(start_date="-5y", end_date="now"),
                    "salary": round(fake.random_number(digits=5) + fake.random_number(digits=2) / 100, 2)
                    #,
                    #"created_at": generate_valid_date(start_date="-5y", end_date="now"),
                    #"updated_at": generate_valid_date(start_date="-5y", end_date="now")
                }
                department_heads.append(dept_head)

        # General Employees (Distributed across stores)
        num_employees_per_store = NUM_GENERAL_EMPLOYEES // NUM_STORES
        for _ in range(num_employees_per_store):
            general_employee = {
                "employee_id": str(uuid.uuid4()),
                "store_id": store_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "role": random.choice(["Cashier", "Stock Clerk", "Sales Associate"]),  # Random role
                "superior_id": random.choice([d["employee_id"] for d in department_heads[-8:]]),  # Reports to a Department Head
                "hire_date": generate_valid_date(start_date="-5y", end_date="now"),
                "salary": round(fake.random_number(digits=5) + fake.random_number(digits=2) / 100, 2)
                #,
                #"created_at": generate_valid_date(start_date="-5y", end_date="now"),
                #"updated_at": generate_valid_date(start_date="-5y", end_date="now")
            }
            general_employees.append(general_employee)

    return pd.DataFrame(store_managers), pd.DataFrame(associate_managers), pd.DataFrame(department_heads), pd.DataFrame(general_employees)

# Connect to SQL Server
def connect_to_sql_server():
    """
    Connects to SQL Server using pyodbc.
    """
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-Q2ON6J0;"  # Replace with your server name
        "DATABASE=store_management;"  # Replace with your database name
        "UID=mrk;"  # Replace with your username
        "PWD=mrk;"  # Replace with your password
    )
    return pyodbc.connect(connection_string)

# Insert Data into SQL Server
def insert_data_to_sql_server(df, table_name, connection):
    """
    Inserts data from a DataFrame into a SQL Server table.
    """
    cursor = connection.cursor()
    for _, row in df.iterrows():
        columns = ", ".join(row.index)
        values = ", ".join(["?"] * len(row))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(query, *row)
    connection.commit()

# Step 1: Generate Stores
stores_df = generate_stores(NUM_STORES)

# Step 2: Generate Employees with Hierarchy
store_managers_df, associate_managers_df, department_heads_df, general_employees_df = generate_employees(stores_df)

# Step 3: Assign Store Managers in Stores Table
# Create a mapping of store_id to manager_id from store_managers_df
store_manager_mapping = store_managers_df.set_index("store_id")["employee_id"].to_dict()

# Assign manager_id to stores_df based on the mapping
stores_df["manager_id"] = stores_df["store_id"].map(store_manager_mapping)

# Step 4: Combine All Employees into One DataFrame
all_employees_df = pd.concat([store_managers_df, associate_managers_df, department_heads_df, general_employees_df], ignore_index=True)

# Step 5: Connect to SQL Server
connection = connect_to_sql_server()

# Step 6: Insert Data into SQL Server
insert_data_to_sql_server(stores_df, "stores", connection)
insert_data_to_sql_server(all_employees_df, "employees", connection)

# Step 7: Close Connection
connection.close()

# Step 8: Data Saving to csv files
all_employees_df.to_csv("employees.csv", index =False)
stores_df.to_csv("stores.csv", index=False)

print("Data successfully inserted into SQL Server with strict store hierarchy!")