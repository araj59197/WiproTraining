num = 4
if num > 0:
    print("Positive number")
else:
    print("Non-positive number")

marks = 85
if marks >= 90:
    grade = "A"
elif marks >= 80:
    grade = "B"
elif marks >= 70:
    grade = "C"
elif marks >= 60:
    grade = "D"
else:
    grade = "F"
print(grade)


for i in range(1, 6):
    print(i)

j = 1
while j <= 5:
    print(j)
    j += 1
    if j == 2:
        break
day = 2
match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 3:
        print("Wednesday")
    case 4:
        print("Thursday")
    case 5:
        print("Friday")
    case 6:
        print("Saturday")
    case 7:
        print("Sunday")
    case _:
        print("Invalid day")
