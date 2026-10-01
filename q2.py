import csv
import os

FILE_NAME = "patients.csv"
FIELDS = ["ID", "Age", "BMI", "BloodPressure", "Glucose", "Outcome"]


def create_sample():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDS)
            writer.writerow([1, 50, 33.6, 72, 148, 1])
            writer.writerow([2, 31, 26.6, 66, 85, 0])
            writer.writerow([3, 32, 23.3, 64, 183, 1])
            writer.writerow([4, 21, 28.1, 66, 89, 0])
            writer.writerow([5, 33, 43.1, 40, 137, 1])
            writer.writerow([6, 30, 25.6, 74, 116, 0])
        print("Sample dataset created.")


def load_records():
    with open(FILE_NAME, "r", newline="") as file:
        return list(csv.DictReader(file))


def save_records(records):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)


def display_records():
    records = load_records()
    print(" | ".join(FIELDS))
    print("-" * 50)
    for rec in records:
        print(" | ".join(str(rec[f]) for f in FIELDS))


def count_cases():
    records = load_records()
    positive = sum(1 for r in records if r["Outcome"] == "1")
    negative = sum(1 for r in records if r["Outcome"] == "0")
    print("Positive cases:", positive)
    print("Negative cases:", negative)


def high_glucose():
    threshold = float(input("Enter glucose threshold: "))
    found = [r for r in load_records() if float(r["Glucose"]) > threshold]
    if not found:
        print("No patients above the threshold.")
        return
    for rec in found:
        print(rec)


def averages():
    records = load_records()
    if not records:
        print("No records available.")
        return
    avg_bmi = sum(float(r["BMI"]) for r in records) / len(records)
    avg_glucose = sum(float(r["Glucose"]) for r in records) / len(records)
    print(f"Average BMI: {avg_bmi:.2f}")
    print(f"Average Glucose: {avg_glucose:.2f}")


def add_record():
    records = load_records()
    new_id = input("ID: ").strip()
    if any(r["ID"] == new_id for r in records):
        print("ID already exists.")
        return
    record = {
        "ID": new_id,
        "Age": int(input("Age: ")),
        "BMI": float(input("BMI: ")),
        "BloodPressure": float(input("Blood pressure: ")),
        "Glucose": float(input("Glucose: ")),
        "Outcome": int(input("Outcome (1/0): ")),
    }
    records.append(record)
    save_records(records)
    print("Record added successfully.")


def update_record():
    records = load_records()
    target = input("Enter ID to update: ").strip()
    for rec in records:
        if rec["ID"] == target:
            for field in FIELDS[1:]:
                value = input(f"{field} [{rec[field]}]: ").strip()
                if value:
                    float(value)
                    rec[field] = value
            save_records(records)
            print("Record updated successfully.")
            return
    print("Record not found.")


def main():
    try:
        create_sample()
    except OSError as error:
        print("Could not create dataset:", error)
        return

    while True:
        print("\n1. Display records")
        print("2. Count positive/negative cases")
        print("3. Patients above glucose threshold")
        print("4. Average BMI and glucose")
        print("5. Add record")
        print("6. Update record")
        print("7. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                display_records()
            elif choice == "2":
                count_cases()
            elif choice == "3":
                high_glucose()
            elif choice == "4":
                averages()
            elif choice == "5":
                add_record()
            elif choice == "6":
                update_record()
            elif choice == "7":
                break
            else:
                print("Invalid option.")
        except ValueError:
            print("Invalid numeric input.")
        except KeyError as error:
            print("Missing column in CSV:", error)
        except FileNotFoundError:
            print("CSV file not found.")
        except OSError as error:
            print("File error:", error)


main()
