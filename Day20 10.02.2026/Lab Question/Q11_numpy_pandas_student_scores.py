"""
NumPy/Pandas Student Scores Analysis

This script demonstrates:
1. Converting Python list of dictionaries to Pandas DataFrame
2. Using NumPy to calculate mean, median, and standard deviation
3. Adding a conditional column based on mean score
"""

import numpy as np
import pandas as pd

# Student data as list of dictionaries
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78},
    {"name": "David", "score": 90},
    {"name": "Eva", "score": 88}
]

print("="*60)
print("STUDENT SCORES ANALYSIS")
print("="*60)

# Step 1: Convert to Pandas DataFrame
df = pd.DataFrame(students)
print("\nOriginal DataFrame:")
print(df)

# Step 2: Calculate statistics using NumPy
scores = df["score"].values  # Convert to NumPy array

mean_score = np.mean(scores)
median_score = np.median(scores)
std_dev_score = np.std(scores)

print("\n" + "="*60)
print("STATISTICAL ANALYSIS (Using NumPy)")
print("="*60)
print(f"Mean Score: {mean_score:.2f}")
print(f"Median Score: {median_score:.2f}")
print(f"Standard Deviation: {std_dev_score:.2f}")

# Step 3: Add 'above_average' column
df["above_average"] = df["score"] > mean_score

print("\n" + "="*60)
print("UPDATED DATAFRAME WITH ABOVE_AVERAGE COLUMN")
print("="*60)
print(df)

# Additional Analysis
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total Students: {len(df)}")
print(f"Students Above Average: {df['above_average'].sum()}")
print(f"Students Below Average: {(~df['above_average']).sum()}")

print("\nStudents Scoring Above Average:")
print(df[df["above_average"]][["name", "score"]])

print("\nStudents Scoring Below Average:")
print(df[~df["above_average"]][["name", "score"]])
print("="*60)
