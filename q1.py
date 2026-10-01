import os

FILE_NAME = "experiments.txt"


def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as file:
            file.write("E001,ResNet50,CIFAR10,0.001,50\n")
            file.write("E002,BERT,IMDB,0.00002,10\n")
            file.write("E003,LSTM,PennTreebank,0.01,30\n")
        print("File created successfully.")
    else:
        print("File already exists.")


def load_records():
    records = []
    with open(FILE_NAME, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                records.append(line.split(","))
    return records


def save_records(records):
    with open(FILE_NAME, "w") as file:
        for record in records:
            file.write(",".join(record) + "\n")


def display_records():
    records = load_records()
    if not records:
        print("No experiments found.")
        return
    print(f"{'ID':<8}{'Model':<15}{'Dataset':<15}{'LR':<10}{'Epochs':<8}")
    print("-" * 56)
    for rec in records:
        print(f"{rec[0]:<8}{rec[1]:<15}{rec[2]:<15}{rec[3]:<10}{rec[4]:<8}")


def search_experiment():
    exp_id = input("Enter experiment ID: ").strip().upper()
    for rec in load_records():
        if rec[0].upper() == exp_id:
            print("ID:", rec[0])
            print("Model:", rec[1])
            print("Dataset:", rec[2])
            print("Learning Rate:", rec[3])
            print("Epochs:", rec[4])
            return
    print("Experiment not found.")


def add_experiment():
    exp_id = input("Experiment ID: ").strip().upper()
    for rec in load_records():
        if rec[0].upper() == exp_id:
            print("An experiment with this ID already exists.")
            return
    model = input("Model name: ").strip()
    dataset = input("Dataset name: ").strip()
    lr = float(input("Learning rate: "))
    epochs = int(input("Number of epochs: "))
    with open(FILE_NAME, "a") as file:
        file.write(f"{exp_id},{model},{dataset},{lr},{epochs}\n")
    print("Experiment added successfully.")


def update_experiment():
    exp_id = input("Enter experiment ID to update: ").strip().upper()
    records = load_records()
    for rec in records:
        if rec[0].upper() == exp_id:
            model = input(f"Model [{rec[1]}]: ").strip()
            dataset = input(f"Dataset [{rec[2]}]: ").strip()
            lr = input(f"Learning rate [{rec[3]}]: ").strip()
            epochs = input(f"Epochs [{rec[4]}]: ").strip()
            if model:
                rec[1] = model
            if dataset:
                rec[2] = dataset
            if lr:
                rec[3] = str(float(lr))
            if epochs:
                rec[4] = str(int(epochs))
            save_records(records)
            print("Experiment updated successfully.")
            return
    print("Experiment not found.")


def remove_experiment():
    exp_id = input("Enter experiment ID to remove: ").strip().upper()
    records = load_records()
    remaining = [rec for rec in records if rec[0].upper() != exp_id]
    if len(remaining) == len(records):
        print("Experiment not found.")
        return
    save_records(remaining)
    print("Experiment removed successfully.")


def main():
    try:
        create_file()
    except OSError as error:
        print("Could not create file:", error)
        return

    while True:
        print("\n1. Display experiments")
        print("2. Search experiment")
        print("3. Add experiment")
        print("4. Update experiment")
        print("5. Remove experiment")
        print("6. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                display_records()
            elif choice == "2":
                search_experiment()
            elif choice == "3":
                add_experiment()
            elif choice == "4":
                update_experiment()
            elif choice == "5":
                remove_experiment()
            elif choice == "6":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")
        except ValueError:
            print("Invalid numeric input.")
        except FileNotFoundError:
            print("File not found.")
        except OSError as error:
            print("File error:", error)


main()
