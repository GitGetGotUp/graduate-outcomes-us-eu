import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

CSV = sorted(Path("data/raw").glob("bls_unemployment_*.csv"))[-1]
df  = pd.read_csv(CSV)

# --- keep only columns the table has ---
cols = ["series_id", "year", "period", "value", "footnotes", "date"]
df = df[cols]

engine = create_engine("postgresql+psycopg://graduser:gradpass@localhost:5432/grads")
df.to_sql("stg_bls_unemp", engine, if_exists="append", index=False)

print(f"Loaded {len(df)} rows from {CSV.name} into stg_bls_unemp")
