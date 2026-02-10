"""
DataFrame Employee Analysis

This script demonstrates:
1. Filtering DataFrame rows by department
2. Calculating average salary per department using groupby
"""

import pandas as pd

# Employee data
data = {
    "Employee": ["John", "Alice", "Bob", "Eva", "Mark"],
    "Department": ["IT", "HR", "IT", "Finance", "HR"],
    "Salary": [50000, 60000, 55000, 65000, 62000]
}

# Create DataFrame
df = pd.DataFrame(data)

print("="*60)
print("EMPLOYEE DATAFRAME ANALYSIS")
print("="*60)
print("\nOriginal DataFrame:")
print(df)

# Task 1: Filter all employees from IT department
print("\n" + "="*60)
print("TASK 1: FILTER IT DEPARTMENT EMPLOYEES")
print("="*60)
it_employees = df[df["Department"] == "IT"]
print(it_employees)

# Task 2: Find average salary per department
print("\n" + "="*60)
print("TASK 2: AVERAGE SALARY PER DEPARTMENT")
print("="*60)
avg_salary_per_dept = df.groupby("Department")["Salary"].mean()
print(avg_salary_per_dept)

# Additional formatted output
print("\n" + "="*60)
print("DETAILED SALARY ANALYSIS")
print("="*60)
for department, avg_salary in avg_salary_per_dept.items():
    print(f"{department}: ${avg_salary:,.2f}")

# Summary statistics
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total Employees: {len(df)}")
print(f"IT Department Employees: {len(it_employees)}")
print(f"Total Departments: {df['Department'].nunique()}")
print(f"Highest Avg Salary Department: {avg_salary_per_dept.idxmax()}")
print(f"Lowest Avg Salary Department: {avg_salary_per_dept.idxmin()}")
print("="*60)
