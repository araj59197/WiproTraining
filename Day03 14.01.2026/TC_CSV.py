import csv

with open("student.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "ID", "Age"])
    writer.writerow(["Tena", 1, 20])
    writer.writerow(["Veena", 2, 21])
    writer.writerow(["Taruna", 3, 22])
