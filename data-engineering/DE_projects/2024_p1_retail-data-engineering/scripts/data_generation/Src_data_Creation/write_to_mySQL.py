from sqlalchemy import create_engine
import pandas as pd

# Load your CSV data into a DataFrame
customers_df = pd.read_csv("customers.csv")
products_df = pd.read_csv("products.csv")

# Define your MySQL database credentials
username = 'rizwanhaidar'
password = 'qaws123'
host = 'localhost'
database = 'CRM_System'

# Create a SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

# Write the DataFrame to a MySQL table named 'customers'
customers_df.to_sql('customers', con=engine, if_exists='replace', index=False)

# Define your MySQL database credentials
username = 'rizwanhaidar'
password = 'qaws123'
host = 'localhost'
database = 'Inventory_mgmt_sys'

# Create a SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")


products_df.to_sql('products', con=engine, if_exists='replace', index=False)

print("Customer data inserted into MySQL successfully!")
