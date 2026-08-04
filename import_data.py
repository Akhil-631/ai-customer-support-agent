import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

USERNAME = "postgres"
PASSWORD = "Data@Analytics"
HOST = "localhost"
PORT = "5432"
DATABASE = "enterprise_ai_agent"

# Encode special characters like @, #, %, etc.
encoded_password = quote_plus(PASSWORD)

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{encoded_password}@{HOST}:{PORT}/{DATABASE}"
)

print("✅ Connected to PostgreSQL")


# Read CSV

df = pd.read_csv("data/superstore_cleaned.csv",
                 parse_dates=["Order Date", "Ship Date"])
print(df.dtypes)

print("\nDataset Loaded Successfully")
print(df.head())
print(f"\nShape: {df.shape}")


# Import into PostgreSQL

df.to_sql(
    "superstore_raw",
    con=engine,
    if_exists="replace",
    index=False
)

print("\n✅ CSV Imported Successfully into PostgreSQL")