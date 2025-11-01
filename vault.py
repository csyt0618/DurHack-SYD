import json
import os
from getpass import getpass

FILENAME = "vault.json" 

def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"user": [], "password": []}

def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_entry():
    data = load_data()
    user = input("Enter username: ")
    pwd = getpass("Enter password (hidden): ")
    data["user"].append(user)
    data["password"].append(pwd)
    save_data(data)
    print("✅ Saved.")

if __name__ == "__main__":
    if input("Add new entry (y/n): ").lower() == "y":
        add_entry()

    print("\nCurrent file contents:")
    print(open(FILENAME, "r", encoding="utf-8").read())
