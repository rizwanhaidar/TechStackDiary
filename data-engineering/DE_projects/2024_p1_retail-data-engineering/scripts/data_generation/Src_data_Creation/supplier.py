import pandas as pd
import uuid
from faker import Faker

# Initialize Faker
fake = Faker()

# Function to generate supplier data
def generate_suppliers(num_records):
    suppliers = []
    for _ in range(num_records):
        supplier_id = str(uuid.uuid4())
        supplier_name = fake.company()
        contact_name = fake.name()
        contact_email = fake.email()
        contact_phone = fake.phone_number()
        address = fake.address().replace("\n", ", ")
        city = fake.city()
        state = fake.state()
        country = fake.country()
        postal_code = fake.postcode()
        website = fake.url()
        payment_terms = fake.random_element(elements=("Net 30", "Net 60", "Net 90"))
        lead_time = fake.random_int(min=1, max=30)  # Lead time in days

        suppliers.append({
            "supplier_id": supplier_id,
            "supplier_name": supplier_name,
            "contact_name": contact_name,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "postal_code": postal_code,
            "website": website,
            "payment_terms": payment_terms,
            "lead_time": lead_time
        })
    return pd.DataFrame(suppliers)

# Generate 1,000 supplier records
suppliers_df = generate_suppliers(1000)

# Save to CSV
suppliers_df.to_csv("suppliers.csv", index=False)


print("Supplier data generated and inserted into MySQL!")