import mysql.connector
from mysql.connector import Error


def connect_to_database():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost", database="company_db", user="root", password="root1234"
        )

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            # Fetch data from employees table
            print("\nFetching data from employees table:")
            sql_select_query = "SELECT * FROM employees"
            cursor.execute(sql_select_query)
            records = cursor.fetchall()

            print("Total number of rows in employees is: ", cursor.rowcount)

            print("\nPrinting each row")
            for row in records:
                print("Id = ", row[0])
                print("Name = ", row[1])
                print("Department = ", row[2])
                print("Salary = ", row[3])
                print("-----------------------")

            # Fetch employees with salary > 50,000
            print("\nFetching employees with salary > 50,000:")
            sql_select_query = "SELECT * FROM employees WHERE salary > 50000"
            cursor.execute(sql_select_query)
            high_salary_records = cursor.fetchall()
            for row in high_salary_records:
                print(f"Id: {row[0]}, Name: {row[1]}, Dept: {row[2]}, Salary: {row[3]}")

            # Insert a new employee record
            print("\nInserting a new employee record...")
            sql_insert_query = (
                "INSERT INTO employees (name, department, salary) VALUES (%s, %s, %s)"
            )
            val = ("John Doe", "Marketing", 60000)
            cursor.execute(sql_insert_query, val)
            connection.commit()
            print(cursor.rowcount, "record inserted.")
            new_employee_id = cursor.lastrowid
            print(f"New employee ID: {new_employee_id}")

            print(f"\nUpdating salary of employee ID {new_employee_id} by 10%...")
            sql_update_query = (
                "UPDATE employees SET salary = salary * 1.10 WHERE id = %s"
            )
            cursor.execute(sql_update_query, (new_employee_id,))
            connection.commit()
            print(cursor.rowcount, "record(s) affected.")

            # Verify update
            print("\nVerifying update for employee ID", new_employee_id)
            cursor.execute("SELECT * FROM employees WHERE id = %s", (new_employee_id,))
            updated_record = cursor.fetchone()
            if updated_record:
                print(
                    f"Id: {updated_record[0]}, Name: {updated_record[1]}, Dept: {updated_record[2]}, Salary: {updated_record[3]}"
                )

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nMySQL connection is closed")


if __name__ == "__main__":
    connect_to_database()
