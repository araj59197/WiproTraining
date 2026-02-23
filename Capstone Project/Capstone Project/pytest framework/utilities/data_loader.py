import csv
import os

def load_kv_csv(file_path):
    """
    Reads a CSV where column 1 is Key and column 2 is Value.
    Returns a dictionary.
    """
    data = {}
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
        
    with open(file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Strip whitespace to handle potential CSV formatting issues
            key = row['parameter'].strip()
            val = row['value'].strip()
            data[key] = val
    return data