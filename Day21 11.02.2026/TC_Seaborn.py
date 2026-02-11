import seaborn as sns
import matplotlib.pyplot as plt

marks = [45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

sns.set_style("whitegrid")

plt.hist(marks, bins=10, color="skyblue", edgecolor="black")
plt.title("Marks Distribution")
plt.xlabel("Marks")
plt.ylabel("Frequency")
plt.grid(True, alpha=0.3)
plt.show()
