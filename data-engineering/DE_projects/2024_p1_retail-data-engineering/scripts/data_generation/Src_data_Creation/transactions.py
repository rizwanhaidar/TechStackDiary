import pandas as pd
import uuid
from faker import Faker
from sqlalchemy import create_engine
import fastavro
import zipfile
from datetime import datetime
import random

# Initialize Faker
fake = Faker()


# Function to generate transaction data
def generate_transactions(num_records, customer_ids, products_df):
    headers = []
    details = []

    for _ in range(num_records):
        # Generate header data
        transaction_id = str(uuid.uuid4())
        customer_id = random.choice(customer_ids)  # Random customer ID from the customers table
        transaction_date = fake.date_time_between(start_date="-2y", end_date="now")  # datetime object
        store_id = str(uuid.uuid4())  # Random store ID
        payment_method = fake.random_element(elements=("Credit Card", "Debit Card", "Cash", "Online Payment"))
        discount = round(fake.random.uniform(0.0, 0.5), 2)  # Random discount between 0% and 50%

        headers.append({
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "transaction_date": transaction_date,  # Keep it as a datetime object
            "store_id": store_id,
            "payment_method": payment_method,
            "discount": discount
        })
        if _ % 10000 == 0:
            print(datetime.now()," : " ,_)
        # Generate detail data (1-5 products per transaction)
        num_products = random.randint(1, 5)  # Random number of products per transaction
        for _ in range(num_products):
            # Randomly select a product and its price
            product = products_df.sample(1).iloc[0]  # Use sample once instead of in loop
            product_id = product["product_id"]
            unit_price = product["unit_price"]

            details.append({
                "transaction_id": transaction_id,  # Link to the header
                "product_id": product_id,  # Product ID from the products table
                "quantity": fake.random_int(min=1, max=10),  # Random quantity between 1 and 10
                "price": unit_price  # Price from the products table
            })

    return pd.DataFrame(headers), pd.DataFrame(details)


# Fetch customer_ids and products data from the database
engine = create_engine("mysql+pymysql://rizwanhaidar:qaws123@localhost/CRM_System")
customer_ids = pd.read_sql("SELECT customer_id FROM customers", engine)["customer_id"].tolist()
engine = create_engine("mysql+pymysql://rizwanhaidar:qaws123@localhost/Inventory_mgmt_sys")
products_df = pd.read_sql("SELECT product_id, unit_price FROM products", engine)

# Generate 1,000,000 transaction records
headers_df, details_df = generate_transactions(1000000, customer_ids, products_df)

# Save to CSV
header_csv_file = "transactions_header.csv"
details_csv_file = "transactions_details.csv"
headers_df.to_csv(header_csv_file, index=False)
details_df.to_csv(details_csv_file, index=False)

# Save to Avro
header_avro_file = "transactions_header.avro"
details_avro_file = "transactions_details.avro"

# Avro schema for header (matching DataFrame schema types)
header_avro_schema = {
    "type": "record",
    "name": "TransactionHeader",
    "fields": [
        {"name": "transaction_id", "type": "string"},
        {"name": "customer_id", "type": "string"},
        {"name": "transaction_date", "type": {"type": "string", "logicalType": "timestamp-millis"}},  # timestamp format
        {"name": "store_id", "type": "string"},
        {"name": "payment_method", "type": "string"},
        {"name": "discount", "type": "double"}
    ]
}

# Avro schema for details (matching DataFrame schema types)
details_avro_schema = {
    "type": "record",
    "name": "TransactionDetail",
    "fields": [
        {"name": "transaction_id", "type": "string"},
        {"name": "product_id", "type": "string"},
        {"name": "quantity", "type": "int"},
        {"name": "price", "type": "double"}
    ]
}

# Convert transaction_date to ISO string format for Avro compatibility
headers_df['transaction_date'] = headers_df['transaction_date'].apply(lambda x: x.isoformat())

# Write header data to Avro
header_records = headers_df.to_dict("records")
with open(header_avro_file, "wb") as f:
    fastavro.writer(f, header_avro_schema, header_records)

# Write detail data to Avro
detail_records = details_df.to_dict("records")
with open(details_avro_file, "wb") as f:
    fastavro.writer(f, details_avro_schema, detail_records)

# Zip the files
date_range = f"{datetime.now().strftime('%Y%m%d')}"  # Current date as the date range
zip_file = f"BULK_transactions_extract_{date_range}.zip"
with zipfile.ZipFile(zip_file, "w") as zipf:
    zipf.write(header_csv_file)
    zipf.write(details_csv_file)
    zipf.write(header_avro_file)
    zipf.write(details_avro_file)

print(f"Transaction files generated and zipped as {zip_file}!")
