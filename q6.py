import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def show(response):
    print("Status code:", response.status_code)
    try:
        print("Response:", response.json())
    except ValueError:
        print("Response has no valid JSON body.")


def run_operation(title, func):
    print(f"\n--- {title} ---")
    try:
        response = func()
        response.raise_for_status()
        show(response)
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Connection error.")
    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)
    except requests.exceptions.RequestException as error:
        print("Request failed:", error)


def main():
    run_operation(
        "GET - retrieve prediction record",
        lambda: requests.get(f"{BASE_URL}/1", timeout=5),
    )

    new_record = {
        "title": "image_001.jpg",
        "body": "label: cat, confidence: 0.97",
        "userId": 1,
    }
    run_operation(
        "POST - send input data",
        lambda: requests.post(BASE_URL, json=new_record, timeout=5),
    )

    updated_record = {
        "id": 1,
        "title": "image_001.jpg",
        "body": "label: dog, confidence: 0.91",
        "userId": 1,
    }
    run_operation(
        "PUT - replace prediction record",
        lambda: requests.put(f"{BASE_URL}/1", json=updated_record, timeout=5),
    )

    run_operation(
        "PATCH - modify part of prediction record",
        lambda: requests.patch(f"{BASE_URL}/1", json={"body": "label: dog, confidence: 0.95"}, timeout=5),
    )

    run_operation(
        "DELETE - remove prediction record",
        lambda: requests.delete(f"{BASE_URL}/1", timeout=5),
    )


main()
