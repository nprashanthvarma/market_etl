"""
extract_fred.py

Pulls economic time series (CPI, Fed Funds Rate, 10Y Treasury, PCE, Unemployment)
from the FRED API and writes a clean CSV ready for loading into Snowflake.
"""

import requests
import time
import csv
import os
from dotenv import load_dotenv
from series import SERIES, START_DATE


load_dotenv(dotenv_path="../.env")

API_KEY = os.environ.get("FRED_API_KEY")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
OUTPUT_FILE = "../data_raw.csv"


def fetch_series(series_id: str) -> list[dict]:
    """Fetch all observations for one FRED series ID."""
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": START_DATE,
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("observations", [])


def main():
    
    if not API_KEY:
        print("ERROR: FRED_API_KEY not found.")
        print("Check that .env exists at ../.env relative to this script,")
        print("and that it contains a line like: FRED_API_KEY=abc123")
        return

    print(f"Key loaded: {API_KEY[:4]}... (showing first 4 characters only)")

    all_rows = []

    for series_id, friendly_name in SERIES.items():
        print(f"Fetching {series_id} ({friendly_name})...")
        try:
            observations = fetch_series(series_id)
        except requests.exceptions.RequestException as e:
            print(f"  FAILED for {series_id}: {e}")
            continue

        row_count = 0
        for obs in observations:
            if obs["value"] == ".":
                continue
            all_rows.append({
                "series_id": series_id,
                "metric": friendly_name,
                "obs_date": obs["date"],
                "value": float(obs["value"]),
            })
            row_count += 1

        print(f"  Got {row_count} observations")
        time.sleep(0.3)

    if not all_rows:
        print("No data extracted - check your API key and series IDs.")
        return

    fieldnames = ["series_id", "metric", "obs_date", "value"]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nDone. Wrote {len(all_rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()












