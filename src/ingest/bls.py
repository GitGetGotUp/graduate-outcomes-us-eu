"""
Download monthly unemployment rates for recent graduates from the BLS API.
Series IDs:
  - LNS14027660  # 20–24 y, Bachelor's or higher
  - LNS14027689  # 25–34 y, Bachelor's or higher
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
SERIES = ["LNS14027660", "LNS14027689"]
RAW_DIR = Path(__file__).parents[2] / "data" / "raw"


def fetch(series_id: str) -> pd.DataFrame:
    res = requests.post(API_URL, json={"seriesid": [series_id]})
    res.raise_for_status()
    df = pd.DataFrame(res.json()["Results"]["series"][0]["data"])
    df["series_id"] = series_id
    return df


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.concat([fetch(s) for s in SERIES])
    df["date"] = pd.to_datetime(df["year"] + "-" + df["period"].str[1:] + "-01")
    df["value"] = df["value"].astype(float)
    out = RAW_DIR / f"bls_unemployment_{datetime.utcnow():%Y%m%d}.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows → {out}")


if __name__ == "__main__":
    main()
