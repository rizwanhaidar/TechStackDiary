import pandas as pd
import uuid
from faker import Faker
from sqlalchemy import create_engine
from datetime import datetime

# Initialize Faker
fake = Faker()

# Function to generate product data
def generate_products(num_records):
    products = []
    for _ in range(num_records):
        product_id = str(uuid.uuid4())
        product_name = fake.word().capitalize() + " " + fake.word().capitalize()
        category = fake.random_element(elements=("Electronics", "Clothing", "Home & Kitchen", "Books", "Toys"))
        brand = fake.company()
        unit_price = round(fake.random_number(digits=3) + fake.random_number(digits=2) / 100, 2)
        cost_price = round(unit_price * fake.random.uniform(0.5, 0.8), 2)  # Cost price is 50-80% of unit price
        supplier_id = str(uuid.uuid4())
        sku = fake.bothify(text="SKU-####-????")  # Example: SKU-1234-ABCD
        description = fake.sentence(nb_words=10)
        manufacturer = fake.company()
        weight = round(fake.random.uniform(0.1, 10.0), 2)  # Weight in kg
        dimensions = f"{fake.random_int(min=1, max=100)}x{fake.random_int(min=1, max=100)}x{fake.random_int(min=1, max=100)} cm"
        is_active = fake.boolean(chance_of_getting_true=90)  # 90% chance of being active


        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "category": category,
            "brand": brand,
            "unit_price": unit_price,
            "cost_price": cost_price,
            "supplier_id": supplier_id,
            "sku": sku,
            "description": description,
            "manufacturer": manufacturer,
            "weight": weight,
            "dimensions": dimensions,
            "is_active": is_active
        })
    return pd.DataFrame(products)

# Generate 10,000 product records
products_df = generate_products(2000)

# Save to CSV (optional)
products_df.to_csv("products.csv", index=False)

# Insert into MySQL
# Replace with your MySQL credentials
# engine = create_engine("mysql+pymysql://user:password@localhost/retail_db")
# products_df.to_sql("products", con=engine, if_exists="replace", index=False)

print("Product data generated and inserted into MySQL!")