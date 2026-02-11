import matplotlib.pyplot as plt

categories = ["A", "B", "C", "D", "E"]
values = [23, 45, 56, 78, 89]
data = [12, 23, 34, 45, 56, 67, 78, 89, 90, 100]
x = [1, 2, 3, 4]
y = [2, 4, 6, 8]

# multiple charts in one figure with beautiful colors
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.patch.set_facecolor("#f0f0f0")

# Pie chart with beautiful colors
pie_colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24", "#6c5ce7"]
explode = (0.05, 0.05, 0.05, 0.05, 0.05)
axs[0, 0].pie(
    values,
    labels=categories,
    autopct="%1.1f%%",
    startangle=140,
    colors=pie_colors,
    explode=explode,
    shadow=True,
)
axs[0, 0].set_title("Pie Chart", fontsize=14, fontweight="bold", color="#2c3e50")

# Bar chart with gradient colors
bar_colors = ["#e74c3c", "#e67e22", "#f39c12", "#16a085", "#2980b9"]
bars = axs[0, 1].bar(
    categories, values, color=bar_colors, edgecolor="#34495e", linewidth=1.5
)
axs[0, 1].set_title("Bar Chart", fontsize=14, fontweight="bold", color="#2c3e50")
axs[0, 1].set_xlabel("Categories", fontweight="bold")
axs[0, 1].set_ylabel("Values", fontweight="bold")
axs[0, 1].grid(axis="y", alpha=0.3, linestyle="--")
axs[0, 1].set_facecolor("#f8f9fa")

# Histogram with beautiful styling
n, bins, patches = axs[1, 0].hist(data, bins=30, edgecolor="#2c3e50", linewidth=1.2)
cm = plt.cm.viridis
for i, patch in enumerate(patches):
    patch.set_facecolor(cm(i / len(patches)))
axs[1, 0].set_title("Histogram", fontsize=14, fontweight="bold", color="#2c3e50")
axs[1, 0].set_xlabel("Value", fontweight="bold")
axs[1, 0].set_ylabel("Frequency", fontweight="bold")
axs[1, 0].grid(axis="y", alpha=0.3, linestyle="--")
axs[1, 0].set_facecolor("#f8f9fa")

# Scatter plot with color mapping
scatter_colors = [10, 20, 30, 40]
scatter = axs[1, 1].scatter(
    x,
    y,
    c=scatter_colors,
    s=200,
    cmap="rainbow",
    edgecolors="#2c3e50",
    linewidth=2,
    alpha=0.7,
)
axs[1, 1].set_title("Scatter Plot", fontsize=14, fontweight="bold", color="#2c3e50")
axs[1, 1].set_xlabel("X axis", fontweight="bold")
axs[1, 1].set_ylabel("Y axis", fontweight="bold")
axs[1, 1].grid(True, alpha=0.3, linestyle="--")
axs[1, 1].set_facecolor("#f8f9fa")
plt.colorbar(scatter, ax=axs[1, 1])

plt.tight_layout()
plt.savefig("charts.png")
plt.show()