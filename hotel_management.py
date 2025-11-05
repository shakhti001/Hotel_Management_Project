# hotel_management.py
# Menu-driven Hotel Management (improved)
import csv
import datetime
import os
import sys
import time

FILENAME = "hotel_data.csv"

def init_file():
    """Create CSV with header if it doesn't exist."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    if not os.path.exists(path):
        try:
            with open(path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "CustomerID","Name","Phone","Email","Address",
                    "RoomType","Days","Amount","CheckInDate","CheckOutDate"
                ])
            print(f"Created new data file: {FILENAME}")
        except PermissionError:
            print(f"Permission error: cannot create {FILENAME}. Close programs using it and try again.")
            sys.exit(1)

def safe_write_row(row):
    """Append a row to CSV with PermissionError handling."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    tries = 0
    while tries < 3:
        try:
            with open(path, "a", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(row)
            return True
        except PermissionError:
            tries += 1
            print("Permission denied while writing file. Make sure the CSV is not open (Excel/Editor). Retrying...")
            time.sleep(1)
    print("Failed to write file after several attempts. Please close any program locking the file.")
    return False

def add_customer():
    print("\n--- Add New Customer ---")
    customer_id = input("Enter customer ID: ").strip()
    name = input("Enter customer name: ").strip()
    phone = input("Enter contact number: ").strip()
    email = input("Enter email address: ").strip().replace(" ", "")
    address = input("Enter address: ").strip()
    room_type = input("Enter room type (Single/Double/Deluxe): ").capitalize().strip()
    try:
        days = int(input("Enter number of days stayed: ").strip())
        if days < 0:
            raise ValueError
    except ValueError:
        print("Invalid number of days. Operation cancelled.")
        return

    rates = {"Single":1500, "Double":2500, "Deluxe":4000}
    if room_type not in rates:
        print("Invalid room type! Use Single, Double or Deluxe.")
        return

    amount = rates[room_type] * days
    checkin = datetime.date.today()
    checkout = checkin + datetime.timedelta(days=days)

    row = [customer_id, name, phone, email, address,
           room_type, days, amount, str(checkin), str(checkout)]

    ok = safe_write_row(row)
    if ok:
        print(f"\n Record added! Total Bill = ₹{amount}\n")

def view_customers():
    print("\n--- All Customer Records ---")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    if not os.path.exists(path):
        print("No records found. Add customers first.")
        return
    with open(path, "r", newline='', encoding="utf-8") as f:
        reader = list(csv.reader(f))
    if len(reader) <= 1:
        print("No records found!")
        return
    header = reader[0]
    print(" | ".join(header))
    print("-" * 100)
    for row in reader[1:]:
        print(" | ".join(row))

def search_customer():
    key = input("Enter CustomerID or Name to search: ").strip().lower()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    if not os.path.exists(path):
        print("No data file found.")
        return
    found = False
    with open(path, "r", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row.get("CustomerID","").strip().lower() == key) or (row.get("Name","").strip().lower() == key):
                print("\nCustomer Found:")
                for k,v in row.items():
                    print(f"{k}: {v}")
                found = True
    if not found:
        print("Customer not found!")

def delete_customer():
    key = input("Enter CustomerID or Name to delete: ").strip().lower()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME)
    if not os.path.exists(path):
        print("No data file found.")
        return
    rows = []
    deleted = False
    with open(path, "r", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not ((row.get("CustomerID","").strip().lower() == key) or (row.get("Name","").strip().lower() == key)):
                rows.append(row)
            else:
                deleted = True
    if deleted:
        try:
            with open(path, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["CustomerID","Name","Phone","Email","Address","RoomType","Days","Amount","CheckInDate","CheckOutDate"])
                writer.writeheader()
                writer.writerows(rows)
            print(" Record deleted successfully!")
        except PermissionError:
            print("Permission denied while writing file. Close the CSV and try again.")
    else:
        print("Customer not found!")

def main_menu():
    init_file()
    while True:
        print("""
======== HOTEL MANAGEMENT ========
1. Add New Customer
2. View All Customers
3. Search Customer
4. Delete Customer
5. Exit
==================================
""")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_customer()
        elif choice == '2':
            view_customers()
        elif choice == '3':
            search_customer()
        elif choice == '4':
            delete_customer()
        elif choice == '5':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()

