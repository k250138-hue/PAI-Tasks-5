import csv
import json
import requests

URL = "https://api.agify.io"
NAMES = ["michael", "sara", "ahmed", "john", "fatima", "ali", "emma", "omar"]
JSON_FILE = "processed_data.json"
CSV_FILE = "processed_data.csv"


def fetch_data():
    params = {"name[]": NAMES}
    response = requests.get(URL, params=params, timeout=8)
    response.raise_for_status()
    return response.json()


def process(data):
    records = []
    for item in data:
        if item.get("age") is None:
            continue
        records.append({
            "name": item["name"],
            "predicted_age": item["age"],
            "sample_count": item["count"],
        })
    return records


def analyse(records):
    if not records:
        print("No valid records to analyse.")
        return
    average = sum(r["predicted_age"] for r in records) / len(records)
    highest = max(records, key=lambda r: r["sample_count"])
    categories = {"young": 0, "adult": 0, "senior": 0}
    for r in records:
        if r["predicted_age"] < 30:
            categories["young"] += 1
        elif r["predicted_age"] < 50:
            categories["adult"] += 1
        else:
            categories["senior"] += 1
    print(f"Average predicted age: {average:.2f}")
    print("Highest sample count:", highest["name"], highest["sample_count"])
    print("Category counts:", categories)


def save_files(records):
    with open(JSON_FILE, "w") as file:
        json.dump(records, file, indent=4)
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "predicted_age", "sample_count"])
        writer.writeheader()
        writer.writerows(records)


def verify_files(records):
    with open(JSON_FILE, "r") as file:
        json_data = json.load(file)
    with open(CSV_FILE, "r", newline="") as file:
        csv_data = list(csv.DictReader(file))
    print("JSON records stored:", len(json_data))
    print("CSV records stored:", len(csv_data))
    if len(json_data) == len(records) == len(csv_data):
        print("Verification successful: stored data matches processed data.")
    else:
        print("Verification failed: record counts do not match.")


def main():
    records = []
    try:
        data = fetch_data()
        records = process(data)
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Connection error.")
    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)
    except ValueError:
        print("Invalid JSON received from the API.")
    except (KeyError, TypeError):
        print("Unexpected data structure in the API response.")
    except requests.exceptions.RequestException as error:
        print("Request failed:", error)
    else:
        print("Data retrieved and parsed successfully.")
        analyse(records)
    finally:
        print("Fetch stage finished.")

    if not records:
        return

    try:
        save_files(records)
        verify_files(records)
    except FileNotFoundError:
        print("A required file is missing.")
    except json.JSONDecodeError:
        print("Saved JSON file contains invalid data.")
    except OSError as error:
        print("File error:", error)
    else:
        print("Files saved and verified.")
    finally:
        print("Program finished.")


main()
