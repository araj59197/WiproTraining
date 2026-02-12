import mysql.connector
host="localhost"
user="root"
password="root1234"
database="feb2026"

myconn=mysql.connector.connect(host=host,user=user,password=password,database=database)

mycursor=myconn.cursor()

mycursor.execute("select * from employee")
# Consume results to clear buffer
for x in mycursor:
    print(x)

#Insert query
try:
    mycursor.execute("insert into employee values(6,'aditya',25000)")
    myconn.commit()
    print("Record inserted successfully")
except mysql.connector.errors.IntegrityError as e:
    print(f"Error: {e}")

# Fetch results again to verify
mycursor.execute("select * from employee")

for i in mycursor:
    print(i)