import xml.etree.ElementTree as ET

tree = ET.parse("student.xml")
root = tree.getroot()
for student in root.findall("student"):
    id = student.find("name").text
    name = student.find("id").text
    marks = student.find("marks").text
    print(f"Name: {name}, ID: {id}, Age: {marks}")

root = ET.Element("employees")
employee1 = ET.SubElement(root, "employee")
ET.SubElement(employee1, "id").text = "101"
ET.SubElement(employee1, "name").text = "Ravi"
ET.SubElement(employee1, "Salary").text = "25000"
employee2 = ET.SubElement(root, "employee")
ET.SubElement(employee2, "id").text = "102"
ET.SubElement(employee2, "name").text = "Leena"
ET.SubElement(employee2, "Salary").text = "24000"

tree = ET.ElementTree(root)
tree.write("employees.xml")
print("\nXML file 'employees.xml' created successfully.")
