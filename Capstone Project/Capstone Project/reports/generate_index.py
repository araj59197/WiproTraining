import os

html_content = """
<html>
<head><title>Test Execution Reports</title></head>
<body>
    <h1>Automation Summary Reports</h1>
    <ul>
        <li><a href="report.html">Pytest HTML Report</a></li>
        <li><a href="pytest_terminal_output.txt">Pytest Terminal Log (Text)</a></li>
        <li><a href="robot_terminal_output.txt">Robot Terminal Log (Text)</a></li>
    </ul>
</body>
</html>
"""

report_path = os.path.join("pytest-framework", "reports", "index.html")
with open(report_path, "w") as f:
    f.write(html_content)
print(f"Summary index created at {report_path}")