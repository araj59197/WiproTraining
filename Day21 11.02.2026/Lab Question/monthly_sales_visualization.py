import matplotlib.pyplot as plt
import seaborn as sns

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [25000, 27000, 30000, 28000, 32000, 31000]

plt.figure(figsize=(10, 5))
plt.plot(months, sales, marker="o", linewidth=2, color="blue")
plt.title("Monthly Sales - Line Chart")
plt.xlabel("Month")
plt.ylabel("Sales (in USD)")
plt.grid(True, alpha=0.3)
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(x=months, y=sales, palette="viridis")
plt.title("Monthly Sales - Bar Plot")
plt.xlabel("Month")
plt.ylabel("Sales (in USD)")
plt.grid(True, alpha=0.3, axis="y")
plt.show()
