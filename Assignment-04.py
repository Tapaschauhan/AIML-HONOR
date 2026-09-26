
import os
import pandas as pd

CSV_FILE = "emp_data.csv"

class Employee:
    def __init__(self):
        if not os.path.isfile(CSV_FILE):
            headers = ["id", "name", "dept", "salary"]
            df = pd.DataFrame(columns=headers)
            df.to_csv(CSV_FILE, index=False)

    def add_record(self):
        df = pd.read_csv(CSV_FILE)
        
        try:
            emp_id = int(input("Enter Emp ID: "))
        except ValueError:
            print("ID must be a number!")
            return

        if not df.empty and emp_id in df["id"].values:
            print("Employee ID already exists.")
            return

        name = input("Enter Name: ")
        dept = input("Enter Department: ")
        
        try:
            salary = float(input("Enter Salary: "))
        except ValueError:
            print("Invalid salary input.")
            return

        new_row = {"id": emp_id, "name": name, "dept": dept, "salary": salary}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        df.to_csv(CSV_FILE, index=False)
        print("Record added successfully.")

    def show_records(self):
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            print("\nNo employee records to display.")
        else:
            print("\n--- EMPLOYEE TABLE ---")
            print(df.to_string(index=False))

    def update_record(self):
        df = pd.read_csv(CSV_FILE)
        
        try:
            target_id = int(input("Enter Emp ID to modify: "))
        except ValueError:
            print("Invalid ID!")
            return

        matching = df[df["id"] == target_id]
        if matching.empty:
            print("No employee found with that ID.")
            return

        idx = df.index[df["id"] == target_id][0]

        print("Leave field blank to keep current value.")
        new_name = input(f"New Name [{df.at[idx, 'name']}]: ")
        new_dept = input(f"New Dept [{df.at[idx, 'dept']}]: ")
        new_sal = input(f"New Salary [{df.at[idx, 'salary']}]: ")

        if new_name.strip() != "":
            df.at[idx, "name"] = new_name
        if new_dept.strip() != "":
            df.at[idx, "dept"] = new_dept
        if new_sal.strip() != "":
            try:
                df.at[idx, "salary"] = float(new_sal)
            except ValueError:
                print("Invalid salary entry. Keeping old salary.")

        df.to_csv(CSV_FILE, index=False)
        print("Record updated.")

    def delete_record(self):
        df = pd.read_csv(CSV_FILE)
        
        try:
            target_id = int(input("Enter Emp ID to remove: "))
        except ValueError:
            print("Invalid ID!")
            return

        if target_id not in df["id"].values:
            print("Record not found.")
            return

        df = df[df["id"] != target_id]
        df.to_csv(CSV_FILE, index=False)
        print("Record deleted successfully.")


def menu():
    emp_obj = Employee()
    
    while True:
        print("\n" + "="*25)
        print("   EMPLOYEE MANAGEMENT")
        print("="*25)
        print("1. Insert Employee")
        print("2. Display All")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. Exit")
        
        ch = input("Enter choice (1-5): ").strip()
        
        if ch == '1':
            emp_obj.add_record()
        elif ch == '2':
            emp_obj.show_records()
        elif ch == '3':
            emp_obj.update_record()
        elif ch == '4':
            emp_obj.delete_record()
        elif ch == '5':
            print("Exiting application...")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    menu()
