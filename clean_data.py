import pandas as pd

# 1. Load the raw data
df = pd.read_csv("raw_sales_data.csv")
print("--- RAW DATA SUMMARY ---")
print(f"Total Rows: {len(df)}")
print("\nMissing Values per Column:")
print(df.isnull().sum())

# 2. Duplicate rows check aur remove karna
initial_count = len(df)
df = df.drop_duplicates()
print(f"\nDuplicates Removed: {initial_count - len(df)}")

# 3. Missing values Handle karna
# Region me missing ko 'Unknown' se fill karna
df["Region"] = df["Region"].fillna("Unknown")

# Unit_Price me missing ko Product_Name ke pricing rule se fill karna
product_price_map = {
    "Basic Plan": 29.99,
    "Pro Plan": 99.99,
    "Enterprise Plan": 299.99,
    "Custom Addon": 49.99,
}
df["Unit_Price"] = df["Unit_Price"].fillna(
    df["Product_Name"].map(product_price_map)
)

# 4. Filter only Completed transactions for Revenue analysis
df_completed = df[df["Status"] == "Completed"].copy()

# Total Amount calculation
df_completed["Total_Revenue"] = df_completed["Unit_Price"]

print("\n--- CLEANED DATA SUMMARY ---")
print(f"Cleaned Total Rows: {len(df_completed)}")
print("Remaining Missing Values:")
print(df_completed.isnull().sum())

# 5. Cleaned File Save karna
df_completed.to_csv("cleaned_sales_data.csv", index=False)
print("\nSuccess: 'cleaned_sales_data.csv' file has been saved!")