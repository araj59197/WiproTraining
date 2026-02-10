import numpy as np
import pandas as pd
arr = np.array([1, 2, 3, 4, 5])
print(arr)
print("sum of array",np.sum(arr))
print("mean of array",np.mean(arr))
print("multiply by 2",arr*2)

data = {
    "name":["Aditya","Raj","Rahul","Amit"],
    "age":[21,22,23,24],
    "city":["Delhi","Mumbai","Kolkata","Chennai"]
}
df=pd.DataFrame(data)
print(df)

print("name column",df["name"])
print(df[df["age"]>22])
# add a column called salary and add 50000 to each employee
df["salary"]=df["age"]*1000
print(df)