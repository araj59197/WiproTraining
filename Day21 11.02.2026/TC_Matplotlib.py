import matplotlib.pyplot as plt

# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')
# plt.show()

x = [1, 2, 3, 4]
y = [1, 2, 3, 4]
plt.plot(x, y, marker="o", linestyle="--", color="r")
plt.xlabel("x axis")
plt.ylabel("y axis")
plt.title("Line Graph")
plt.savefig("1_line_graph.png")
plt.show()

# Bar Chart Example
categories = ["A", "B", "C", "D", "E"]
values = [23, 45, 56, 78, 32]

plt.bar(categories, values, color="skyblue", edgecolor="black")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.title("Bar Chart Example")
plt.savefig("2_bar_chart_vertical.png")
plt.show()

# Horizontal Bar Chart
plt.barh(categories, values, color="coral", edgecolor="navy")
plt.xlabel("Values")
plt.ylabel("Categories")
plt.title("Horizontal Bar Chart")
plt.savefig("3_bar_chart_horizontal.png")
plt.show()

# Multiple Bars (Grouped Bar Chart)
x_pos = [0, 1, 2, 3, 4]
values1 = [23, 45, 56, 78, 32]
values2 = [30, 40, 50, 60, 35]

width = 0.35
plt.bar([p - width / 2 for p in x_pos], values1, width, label="Series 1", color="blue")
plt.bar(
    [p + width / 2 for p in x_pos], values2, width, label="Series 2", color="orange"
)
plt.xlabel("Categories")
plt.ylabel("Values")
plt.title("Grouped Bar Chart")
plt.xticks(x_pos, categories)
plt.legend()
plt.savefig("4_grouped_bar_chart.png")
plt.show()

# Histogram Example 1 - Basic Histogram
import numpy as np

data = np.random.randn(1000)  # Generate 1000 random numbers from normal distribution

plt.hist(data, bins=30, color="green", edgecolor="black")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Basic Histogram")
plt.savefig("5_histogram_basic.png")
plt.show()

# Histogram Example 2 - Custom bins and styling
ages = [
    22,
    24,
    25,
    27,
    29,
    30,
    32,
    33,
    35,
    38,
    40,
    42,
    45,
    48,
    50,
    52,
    55,
    58,
    60,
    62,
    65,
    67,
    70,
    22,
    25,
    28,
    30,
    33,
    35,
    38,
]

plt.hist(
    ages,
    bins=[20, 30, 40, 50, 60, 70, 80],
    color="purple",
    edgecolor="white",
    alpha=0.7,
)
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.title("Age Distribution with Custom Bins")
plt.grid(axis="y", alpha=0.3)
plt.savefig("6_histogram_age_distribution.png")
plt.show()

# Histogram Example 3 - Multiple Histograms
data1 = np.random.normal(100, 15, 1000)  # Mean=100, Std=15
data2 = np.random.normal(90, 20, 1000)  # Mean=90, Std=20

plt.hist(data1, bins=30, color="blue", alpha=0.5, label="Group 1")
plt.hist(data2, bins=30, color="red", alpha=0.5, label="Group 2")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Multiple Histograms Comparison")
plt.legend()
plt.savefig("7_histogram_multiple.png")
plt.show()

plt.scatter(x, y, color="green")
plt.title("Scatter Plot")
plt.savefig("8_scatter_plot.png")
plt.show()

labels = ["chrome", "firefox", "edge", "safari", "opera"]
values = [100, 80, 60, 40, 20]

plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
plt.title("Pie Chart Example")
plt.savefig("pie_chart.png")
plt.show()




