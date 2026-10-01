import json
import os

FILE_NAME = "model_results.json"


def create_sample():
    if not os.path.exists(FILE_NAME):
        data = [
            {"model": "Logistic Regression", "accuracy": 0.86, "precision": 0.84, "recall": 0.82, "f1_score": 0.83},
            {"model": "Random Forest", "accuracy": 0.91, "precision": 0.90, "recall": 0.88, "f1_score": 0.89},
            {"model": "SVM", "accuracy": 0.89, "precision": 0.91, "recall": 0.87, "f1_score": 0.89},
            {"model": "Neural Network", "accuracy": 0.93, "precision": 0.92, "recall": 0.94, "f1_score": 0.93},
        ]
        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)
        print("Sample JSON file created.")


def load_results():
    with open(FILE_NAME, "r") as file:
        return json.load(file)


def save_results(results):
    with open(FILE_NAME, "w") as file:
        json.dump(results, file, indent=4)


def display_results():
    for item in load_results():
        print(item)


def best_models():
    results = load_results()
    if not results:
        print("No results available.")
        return
    best_acc = max(results, key=lambda r: r["accuracy"])
    best_f1 = max(results, key=lambda r: r["f1_score"])
    print("Highest accuracy:", best_acc["model"], best_acc["accuracy"])
    print("Highest F1-score:", best_f1["model"], best_f1["f1_score"])


def add_result():
    results = load_results()
    name = input("Model name: ").strip()
    if any(r["model"].lower() == name.lower() for r in results):
        print("Model already exists.")
        return
    record = {
        "model": name,
        "accuracy": float(input("Accuracy: ")),
        "precision": float(input("Precision: ")),
        "recall": float(input("Recall: ")),
        "f1_score": float(input("F1-score: ")),
    }
    results.append(record)
    save_results(results)
    print("Model result added successfully.")


def update_result():
    results = load_results()
    name = input("Model name to update: ").strip()
    for item in results:
        if item["model"].lower() == name.lower():
            for key in ["accuracy", "precision", "recall", "f1_score"]:
                value = input(f"{key} [{item[key]}]: ").strip()
                if value:
                    item[key] = float(value)
            save_results(results)
            print("Model result updated successfully.")
            return
    print("Model not found.")


def remove_result():
    results = load_results()
    name = input("Model name to remove: ").strip()
    remaining = [r for r in results if r["model"].lower() != name.lower()]
    if len(remaining) == len(results):
        print("Model not found.")
        return
    save_results(remaining)
    print("Model result removed successfully.")


def main():
    try:
        create_sample()
    except OSError as error:
        print("Could not create file:", error)
        return

    while True:
        print("\n1. Display results")
        print("2. Best accuracy and F1-score")
        print("3. Add model result")
        print("4. Update model result")
        print("5. Remove model result")
        print("6. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                display_results()
            elif choice == "2":
                best_models()
            elif choice == "3":
                add_result()
            elif choice == "4":
                update_result()
            elif choice == "5":
                remove_result()
            elif choice == "6":
                break
            else:
                print("Invalid option.")
        except ValueError:
            print("Invalid numeric input.")
        except KeyError as error:
            print("Missing key in JSON record:", error)
        except json.JSONDecodeError:
            print("The JSON file is invalid.")
        except FileNotFoundError:
            print("JSON file not found.")
        except OSError as error:
            print("File error:", error)


main()
