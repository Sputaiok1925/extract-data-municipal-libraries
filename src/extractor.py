import requests
import pandas as pd
import json
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
from dotenv import load_dotenv
import datetime

# API URL and key
API_URL = "https://api.golemio.cz/v2/municipallibraries"
API_KEY = os.getenv("API_KEY")
headers = {"X-Access-Token": API_KEY}

OUTPUT_FILE = "municipal_libraries.csv"

# Function to fetch data
def fetch_libraries():
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    try:
        data = response.json()
        return data.get('features', [])
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return []

# Function to extract and save data
def extract_and_save():
    print(f"\n=== Data update started: {datetime.datetime.now()} ===")
    libraries = fetch_libraries()
    records = []
    for lib in libraries:
        properties = lib.get("properties", {})
        address = properties.get("address", {})
        # location = properties.get("geometry", {}).get("coordinates", [])
        location = lib.get("geometry", {}).get("coordinates", [])
        records.append({
            "ID knižnice": properties.get("id", ""),
            "Názov knižnice": properties.get("name", ""),
            "Ulica": address.get("street_address", ""),
            "PSČ": address.get("postal_code", ""),
            "Mesto": address.get("address_locality", "").split()[0],
            "Kraj": properties.get("district", ""),
            "Krajina": address.get("address_country", ""),
            "Zemepisná šírka": location[1] if len(location) > 1 else "",
            "Zemepisná dĺžka": location[0] if len(location) > 0 else "",
            "Čas otvorenia": ', '.join(
                [f"{entry['day_of_week']} {entry['opens']}-{entry['closes']}"
                 for entry in properties.get('opening_hours', [])]),
        })
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"Data successfully updated and saved to '{OUTPUT_FILE}'")

# Main function with scheduler
def main():
    # Run immediately if file does not exist
    if not os.path.exists(OUTPUT_FILE):
        print("File not found, performing initial data collection...")
        extract_and_save()
    else:
        print("File found, skipping initial data collection.")

    # Scheduler setup
    scheduler = BlockingScheduler(timezone=timezone('Europe/Prague'))
    scheduler.add_job(extract_and_save, 'cron', hour=7, minute=0)
    print("Scheduler started. Data will be updated daily at 7:00 AM (Prague time).")
    scheduler.start()

if __name__ == "__main__":
    main()
