import pandas as pd
from eurostat import get_data_df
from pathlib import Path
from datetime import datetime

RAW_DIR    = Path(__file__).parents[2] / "data" / "raw"
COUNTRIES  = ["DE", "FR", "IT", "ES", "NL"]
SERIES_ID  = "tps00053"   # Employment rate of recent tertiary graduates

def _find_col(df, needle):
    """
    Return the column name that contains `needle` (case‑insensitive).
    Raises KeyError if none found.
    """
    matches = [c for c in df.columns if needle.lower() in str(c).lower()]
    if not matches:
        raise KeyError(f"Could not find a column containing '{needle}'")
    return matches[0]

def main() -> None:
    df_wide = get_data_df(SERIES_ID, flags=False).reset_index()

    # Detect column names instead of assuming 'geo' and 'sex'
    geo_col  = _find_col(df_wide, "geo")
    sex_col  = _find_col(df_wide, "sex")

    df_wide = df_wide[df_wide[geo_col].isin(COUNTRIES) & (df_wide[sex_col] == "T")]

    # Melt year columns into tidy rows (year columns are all‑numeric strings)
    year_cols = [c for c in df_wide.columns if str(c).isnumeric()]
    df = df_wide.melt(
        id_vars=[geo_col],
        value_vars=year_cols,
        var_name="year",
        value_name="emp_rate",
    )

    df = df.rename(columns={geo_col: "country"})
    df["year"] = df["year"].astype(int)
    df["emp_rate"] = df["emp_rate"].astype(float)

    # Simple EU‑5 average
    eu5 = (
        df.groupby("year", as_index=False)
          .agg(emp_rate=("emp_rate", "mean"))
          .assign(country="EU5")
    )
    df = pd.concat([df, eu5], ignore_index=True)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / f"eurostat_grad_emp_{datetime.utcnow():%Y%m%d}.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows to {out}")

if __name__ == "__main__":
    main()
