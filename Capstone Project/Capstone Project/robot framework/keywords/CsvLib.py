import csv
from pathlib import Path

class CsvLib:
    """Library for handling CSV operations in Robot Framework"""
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def get_csv_data(self, csv_path):
        """Read CSV file and return data as dictionary"""
        data = {}
        csv_file = Path(csv_path)
        
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.update(row)
        
        return data