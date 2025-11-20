import os
import requests
from dotenv import load_dotenv
import json

# Load your API key from the .env file
load_dotenv()
API_KEY = os.getenv("BLS_API_KEY")

# BLS series ID for Manufacturing Employment
SERIES_ID = "CEU3000000001"

# Output file path
OUTPUT_PATH = "data/raw/manufacturing.json"

def fetch_manufacturing_data(start_year="2010", end_year="2024"):
    """
    Fetch manufacturing employment data from BLS API.
    Saves the raw JSON to data/raw/manufacturing.json
    """
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    payload = {
        "seriesid": [SERIES_ID],
        "startyear": start_year,
        "endyear": end_year,
        "registrationkey": API_KEY
    }

    # Make POST request
    response = requests.post(url, json=payload)

    # Check for errors
    if response.status_code != 200:
        raise Exception(f"Error: API returned status code {response.status_code}")

    data = response.json()

    # Create output folder if missing
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Save JSON file
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved raw data to {OUTPUT_PATH}")


if __name__ == "__main__":
    fetch_manufacturing_data()
