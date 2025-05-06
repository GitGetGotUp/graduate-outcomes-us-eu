import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

CSV = sorted(Path("data/raw").glob("bls_unemployment_*.csv"))[-1]
df  = pd.read_csv(CSV)

# keep only the columns we created in the table
cols = ["series_id", "year", "period", "value", "footnotes", "date"]
df = df[cols]

# ---- NEW LINE: cast to true date ------- #
df["date"] = pd.to_datetime(df["date"]).dt.date
# ---------------------------------------- #

eng = create_engine(
    "postgresql+psycopg://graduser:gradpass@localhost:5432/grads",
    future=True,
)

df.to_sql("stg_bls_unemp", eng, if_exists="append", index=False)
print(f"Loaded {len(df)} rows from {CSV.name} into stg_bls_unemp")
