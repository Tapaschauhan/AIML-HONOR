import sqlite3

class EmployeeDatabase:
    def _init_(self, db_name="employee_db.db"):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
        CREATE TABLE IF NOT EXISTS employee (
            emp_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
        """
        cursor.execute(query)
        conn.commit()
        conn.close()

    def add_employee(self):
        print("\n--- Add New Employee ---")
        try:
            emp_id = int(input("Enter Employee ID: "))
            name = input("Enter Employee Name: ").strip()
            department = input("Enter Department: ").strip()
            salary = float(input("Enter Salary: "))

            conn = self.get_connection()
            cursor = conn.cursor()

            query = "INSERT INTO employee (emp_id, name, department, salary) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (emp_id, name, department, salary))
            
            conn.commit()
            conn.close()
            print("Employee added successfully!")

        except sqlite3.IntegrityError:
            print("Error: An employee with this ID already exists.")
        except ValueError:
            print("Error: Invalid input type. ID and Salary must be numbers.")

    def view_employees(self):
        print("\n- Employee List -")
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employee")
        records = cursor.fetchall()
        conn.close()

        if not records:
            print("No records found in the database.")
            return

        # Print header and data
        print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'Salary':<10}")
        print("-" * 55)
        for row in records:
            print(f"{row[0]:<10} {row[1]:<20} {row[2]:<15} {row[3]:<10.2f}")

    def update_employee(self):
        print("\n- Update Employee Record -")
        try:
            emp_id = int(input("Enter Employee ID to update: "))

            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employee WHERE emp_id = ?", (emp_id,))
            record = cursor.fetchone()

            if not record:
                print("Error: Employee ID not found.")
                conn.close()
                return

            print(f"Current Record -> Name: {record[1]}, Dept: {record[2]}, Salary: {record[3]}")
            
            new_name = input("Enter New Name (leave blank to keep current): ").strip()
            new_dept = input("Enter New Department (leave blank to keep current): ").strip()
            new_salary_str = input("Enter New Salary (leave blank to keep current): ").strip()

            
            updated_name = new_name if new_name else record[1]
            updated_dept = new_dept if new_dept else record[2]
            updated_salary = float(new_salary_str) if new_salary_str else record[3]

            query = """
            UPDATE employee 
            SET name = ?, department = ?, salary = ? 
            WHERE emp_id = ?
            """
            cursor.execute(query, (updated_name, updated_dept, updated_salary, emp_id))
            conn.commit()
            conn.close()
            
            print("Employee record updated successfully!")

        except ValueError:
            print("Error: Invalid numeric input.")

    def delete_employee(self):
        print("\n- Delete Employee -")
        try:
            emp_id = int(input("Enter Employee ID to delete: "))

            conn = self.get_connection()
            cursor = conn.cursor()

            
            cursor.execute("SELECT * FROM employee WHERE emp_id = ?", (emp_id,))
            if not cursor.fetchone():
                print("Error: Employee ID not found.")
                conn.close()
                return

            cursor.execute("DELETE FROM employee WHERE emp_id = ?", (emp_id,))
            conn.commit()
            conn.close()

            print("Employee record deleted successfully!")

        except ValueError:
            print("Error: Please enter a valid numerical ID.")


def main():
    db = EmployeeDatabase()

    while True:
        print("\n=== EMPLOYEE DATABASE MENU ===")
        print("1. Create (Add Employee)")
        print("2. Read (View All Employees)")
        print("3. Update Employee Record")
        print("4. Delete Employee Record")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            db.add_employee()
        elif choice == '2':
            db.view_employees()
        elif choice == '3':
            db.update_employee()
        elif choice == '4':
            db.delete_employee()
        elif choice == '5':
            print("Closing application. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 5.")

if __name__ == "__main__":
    main()
