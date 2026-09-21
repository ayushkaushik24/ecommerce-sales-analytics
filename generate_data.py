import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
np.random.seed(42)

n_rows = 50000

products = {
    "Basic Plan": 29.99,
    "Pro Plan": 99.99,
    "Enterprise Plan": 299.99,
    "Custom Addon": 49.99,
}

prod_names = list(products.keys())

data = {
    "Transaction_ID": [f"TXN-{100000 + i}" for i in range(n_rows)],
    "Customer_ID": [
        f"CUST-{np.random.randint(1000, 2500)}" for _ in range(n_rows)
    ],
    "Product_Name": np.random.choice(
        prod_names, size=n_rows, p=[0.4, 0.35, 0.15, 0.1]
    ),
    "Region": np.random.choice(
        ["North America", "Europe", "Asia-Pacific", "LATAM"], size=n_rows
    ),
    "Transaction_Date": [
        fake.date_between(start_date="-1y", end_date="today")
        for _ in range(n_rows)
    ],
    "Payment_Method": np.random.choice(
        ["Credit Card", "PayPal", "Bank Transfer"], size=n_rows
    ),
    "Status": np.random.choice(
        ["Completed", "Cancelled", "Refunded"], size=n_rows, p=[0.85, 0.1, 0.05]
    ),
}

df = pd.DataFrame(data)
df["Unit_Price"] = df["Product_Name"].map(products)

# Deliberately adding missing values
nan_mask_region = np.random.rand(len(df)) < 0.03
df.loc[nan_mask_region, "Region"] = np.nan

nan_mask_price = np.random.rand(len(df)) < 0.02
df.loc[nan_mask_price, "Unit_Price"] = np.nan

# Deliberately adding duplicate rows (~1000 duplicates)
duplicates = df.sample(n=1000, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

df.to_csv("raw_sales_data.csv", index=False)
print(f"Dataset generated successfully! Total rows: {len(df)}")