import csv
import json
import requests

URL = "https://jsonplaceholder.typicode.com/comments"


def fetch_texts(post_id):
    try:
        response = requests.get(URL, params={"postId": post_id}, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return []
    except requests.exceptions.ConnectionError:
        print("Connection error.")
        return []
    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)
        return []
    except ValueError:
        print("Invalid JSON response received.")
        return []
    except requests.exceptions.RequestException as error:
        print("Request failed:", error)
        return []

    if not isinstance(data, list):
        print("Unexpected response format.")
        return []

    records = []
    for item in data:
        try:
            records.append({
                "id": item["id"],
                "text": item["body"].replace("\n", " "),
                "author": item["email"],
                "title": item["name"],
                "post_id": item["postId"],
            })
        except (KeyError, TypeError, AttributeError):
            continue
    return records


def display(records):
    for index, rec in enumerate(records, start=1):
        print(f"{index}. [{rec['author']}] {rec['title']}")
        print("   ", rec["text"])
        print()


def choose(records):
    choice = input("Enter numbers to save (comma-separated) or 'all': ").strip().lower()
    if choice == "all":
        return records
    selected = []
    for part in choice.split(","):
        part = part.strip()
        if part.isdigit() and 1 <= int(part) <= len(records):
            selected.append(records[int(part) - 1])
    return selected


def save_json(records, path="text_data.json"):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, ensure_ascii=False)
        print("Saved to", path)
    except OSError as error:
        print("Could not write JSON file:", error)


def save_csv(records, path="text_data.csv"):
    try:
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "text", "author", "title", "post_id"])
            writer.writeheader()
            writer.writerows(records)
        print("Saved to", path)
    except OSError as error:
        print("Could not write CSV file:", error)


def main():
    post_id = input("Enter a post ID (1-100): ").strip()
    if not post_id.isdigit():
        print("Post ID must be a number.")
        return

    records = fetch_texts(post_id)
    if not records:
        print("No text data retrieved.")
        return

    display(records)
    selected = choose(records)
    if not selected:
        print("Nothing selected.")
        return

    save_json(selected)
    save_csv(selected)


main()
