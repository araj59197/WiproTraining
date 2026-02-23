import subprocess
import glob
import os

def run_robot_tests():
    # Get the current directory (robot framework)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level to Final_Capstone
    parent_dir = os.path.dirname(current_dir)
    
    # We will check both "pytest framework" and "pytest-framework"
    possible_data_paths = [
        os.path.join(parent_dir, "pytest framework", "data"),
        os.path.join(parent_dir, "pytest-framework", "data")
    ]
    
    data_dir = None
    for p in possible_data_paths:
        if os.path.exists(p):
            data_dir = p
            break
            
    if not data_dir:
        print(f"ERROR: Could not find data directory in {parent_dir}")
        print("Checked: 'pytest framework/data' and 'pytest-framework/data'")
        return

    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    report_dir = os.path.join(current_dir, "reports")
    
    print(f"Checking for CSVs in: {data_dir}")
    
    if not csv_files:
        print(f"ERROR: No .csv files found in {data_dir}")
        return

    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    for csv in csv_files:
        csv_name = os.path.basename(csv)
        print(f"\n>>> Starting Robot Suite for: {csv_name}")
        
        # We wrap path in quotes to handle the spaces in "Dibyojyoti Deb" and "pytest framework"
        cmd = [
            "robot",
            "--variable", f"CSV_PATH:{csv}",
            "--outputdir", report_dir,
            "--report", "report.html",
            "--log", "log.html",
            "tests/shop.robot"
        ]
        
        # shell=True is necessary for MINGW64 to handle the robot command correctly
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    run_robot_tests()