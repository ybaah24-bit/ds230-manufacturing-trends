import json
import re
import pandas as pd
import os

RAW_PATH = "data/raw/manufacturing.json"
OUTPUT_PATH = "data/processed/manufacturing_clean.csv"

def clean_manufacturing_data():
    # Load JSON
    with open(RAW_PATH, "r") as f:
        data = json.load(f)
    
    # Extract the series data
    series_data = data["Results"]["series"][0]["data"]
    
    cleaned_rows = []

    for entry in series_data:
        # Example entry keys: "year", "period", "value"
        year = entry["year"]
        month_code = entry["period"]   # Ex: "M01"
        value = entry["value"]

        # Skip annual summary "M13"
        if month_code == "M13":
            continue

        # Convert month code "M01" → 1
        month = int(month_code.replace("M", ""))

        # Clean the value using regex (remove commas, spaces, etc.)
        value_clean = re.sub(r"[^0-9.]", "", value)
        value_clean = float(value_clean)

        cleaned_rows.append({
            "year": int(year),
            "month": month,
            "value": value_clean
        })

    # Convert to DataFrame
    df = pd.DataFrame(cleaned_rows)

    # Sort chronologically
    df = df.sort_values(["year", "month"])

    # Create processed folder if missing
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Save CSV
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved cleaned CSV to {OUTPUT_PATH}")


if __name__ == "__main__":
    clean_manufacturing_data()
