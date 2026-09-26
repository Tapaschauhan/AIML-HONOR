import csv
import os

FILENAME = "employees.csv"

def initialize_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["EmpID", "Name", "Department", "Salary"])

class EmployeeManager:
    def create_employee(self):
        print("\n- Add New Employee -")
        emp_id = input("Enter Employee ID: ").strip()
        
        if self.find_employee(emp_id):
            print("Error: Employee ID already exists!")
            return

        name = input("Enter Name: ").strip()
        dept = input("Enter Department: ").strip()
        salary = input("Enter Salary: ").strip()

        with open(FILENAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([emp_id, name, dept, salary])
            
        print("Employee added successfully!")

    def read_employees(self):
        print("\n- Employee Records -")
        if not os.path.exists(FILENAME):
            print("No records found.")
            return

        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            records = list(reader)
            
            if len(records) <= 1:
                print("No employee records found.")
                return


            for row in records:
                print(f"{row[0]:<10} {row[1]:<20} {row[2]:<15} {row[3]:<10}")

    def update_employee(self):
        print("\n- Update Employee -")
        emp_id = input("Enter Employee ID to update: ").strip()
        
        records = []
        found = False

        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == emp_id:
                    found = True
                    print(f"Current Data: Name: {row[1]}, Dept: {row[2]}, Salary: {row[3]}")
                    new_name = input("Enter New Name (leave blank to keep current): ").strip()
                    new_dept = input("Enter New Dept (leave blank to keep current): ").strip()
                    new_salary = input("Enter New Salary (leave blank to keep current): ").strip()

                    row[1] = new_name if new_name else row[1]
                    row[2] = new_dept if new_dept else row[2]
                    row[3] = new_salary if new_salary else row[3]
                
                records.append(row)

        if found:
            with open(FILENAME, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(records)
            print("Employee record updated successfully!")
        else:
            print("Employee ID not found.")

    def delete_employee(self):
        print("\n- Delete Employee -")
        emp_id = input("Enter Employee ID to delete: ").strip()

        records = []
        found = False

        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == emp_id:
                    found = True
                else:
                    records.append(row)

        if found:
            with open(FILENAME, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(records)
            print("Employee record deleted successfully!")
        else:
            print("Employee ID not found.")

    def find_employee(self, emp_id):
        if not os.path.exists(FILENAME):
            return False
            
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == emp_id:
                    return True
        return False


def main():
    initialize_file()
    manager = EmployeeManager()

    while True:
        print("\n= EMPLOYEE MANAGEMENT SYSTEM =")
        print("1. Create (Add Employee)")
        print("2. Read (View All Employees)")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            manager.create_employee()
        elif choice == '2':
            manager.read_employees()
        elif choice == '3':
            manager.update_employee()
        elif choice == '4':
            manager.delete_employee()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
