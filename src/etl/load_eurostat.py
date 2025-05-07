import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

CSV = sorted(Path("data/raw").glob("eurostat_grad_emp_*.csv"))[-1]
df  = pd.read_csv(CSV)

eng = create_engine("postgresql+psycopg://graduser:gradpass@localhost:5432/grads")
df.to_sql("stg_eu_grad_emp", eng, if_exists="append", index=False)
print(f"Loaded {len(df)} rows from {CSV.name} into stg_eu_grad_emp")
