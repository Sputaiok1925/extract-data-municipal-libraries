import requests
import pandas as pd
import json
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
import datetime

# URL и ключ API
API_URL = "https://api.golemio.cz/v2/municipallibraries"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MzU0OCwiaWF0IjoxNzQ2MDM4ODY4LCJleHAiOjExNzQ2MDM4ODY4LCJpc3MiOiJnb2xlbWlvIiwianRpIjoiNTlmNWVmODAtY2JlZC00YjU2LThkMTYtNjZlYmYzNjk2MDQ4In0.dyEPutgPtxqCSZ21mfj9ZhpwX2oXOAdbdGQj3IzOYgw"
headers = {"X-Access-Token": API_KEY}

OUTPUT_FILE = "municipal_libraries.csv"

# Функция для получения данных
def fetch_libraries():
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    try:
        data = response.json()
        return data.get('features', [])
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON.")
        return []

# Функция для извлечения и сохранения данных
def extract_and_save():
    print(f"\n=== Запуск обновления данных: {datetime.datetime.now()} ===")
    libraries = fetch_libraries()
    records = []
    for lib in libraries:
        properties = lib.get("properties", {})
        address = properties.get("address", {})
        #location = properties.get("geometry", {}).get("coordinates", [])
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
    print(f"Данные успешно обновлены и сохранены в '{OUTPUT_FILE}'")

# Основная функция с планировщиком
def main():
    # Первый запуск сразу (если файл не существует)
    if not os.path.exists(OUTPUT_FILE):
        print("Файл не найден, выполняем первый сбор данных...")
        extract_and_save()
    else:
        print("Файл найден, пропускаем начальный сбор.")

    # Настройка планировщика
    scheduler = BlockingScheduler(timezone=timezone('Europe/Prague'))
    scheduler.add_job(extract_and_save, 'cron', hour=7, minute=0)
    print("Планировщик запущен. Данные будут обновляться ежедневно в 7:00 (по Праге).")
    scheduler.start()

if __name__ == "__main__":
    main()
