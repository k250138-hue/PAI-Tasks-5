import requests

URL = "https://api.genderize.io"


def get_prediction(name):
    try:
        response = requests.get(URL, params={"name": name}, timeout=5)
        print("Status code:", response.status_code)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print("The request timed out. The API did not respond in time.")
        return
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your internet connection.")
        return
    except requests.exceptions.HTTPError as error:
        print("HTTP error occurred:", error)
        return
    except ValueError:
        print("The API returned an invalid JSON response.")
        return
    except requests.exceptions.RequestException as error:
        print("Request failed:", error)
        return

    prediction = data.get("gender")
    confidence = data.get("probability")
    input_name = data.get("name")
    samples = data.get("count")

    if prediction is None:
        print("The API could not provide a prediction for this input.")
        return

    print("Input name:", input_name)
    print("Prediction:", prediction)
    print("Confidence score:", confidence)
    print("Samples used:", samples)


def main():
    name = input("Enter a first name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    get_prediction(name)


main()
