import pandas as pd
import uuid
from faker import Faker
from sqlalchemy import create_engine

# Initialize Faker
fake = Faker()

# Function to generate customer data
def generate_customers(num_records):
    customers = []
    for _ in range(num_records):
        customers.append({
            "customer_id": str(uuid.uuid4()),  # Unique UUID for each customer
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address().replace("\n", ", "),
            "loyalty_points": fake.random_int(min=0, max=1000)  # Random loyalty points
        })
    return pd.DataFrame(customers)

# Generate 100,000 customer records
customers_df = generate_customers(100000)

# Save to CSV (optional)
customers_df.to_csv("customers.csv", index=False)

# Insert into MySQL
# Replace with your MySQL credentials
engine = create_engine("mysql+pymysql://rizwanhaidar:qaws123@localhost/CRM_System")
customers_df.to_sql("customers", con=engine, if_exists="replace", index=False)

print("Customer data generated and inserted into MySQL!")