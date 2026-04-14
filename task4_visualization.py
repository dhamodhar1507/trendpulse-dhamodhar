# Task 4 - Visualizations

import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# 1. Load Data
# -------------------------------
df = pd.read_csv("data/trends_analysed.csv")

# -------------------------------
# 2. Create outputs folder
# -------------------------------
os.makedirs("outputs", exist_ok=True)

# -------------------------------
# 3. Chart 1: Top 10 Stories by Score
# -------------------------------

top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles
top10["short_title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure(figsize=(10, 6))
plt.barh(top10["short_title"], top10["score"])
plt.gca().invert_yaxis()

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# -------------------------------
# 4. Chart 2: Stories per Category
# -------------------------------

category_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))
category_counts.plot(kind="bar")

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

# -------------------------------
# 5. Chart 3: Score vs Comments
# -------------------------------

plt.figure(figsize=(8, 5))

# Separate popular vs non-popular
popular = df[df["is_popular"] == True]
non_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(non_popular["score"], non_popular["num_comments"], label="Not Popular")

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# -------------------------------
# 6. BONUS: Dashboard
# -------------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1
axes[0].barh(top10["short_title"], top10["score"])
axes[0].invert_yaxis()
axes[0].set_title("Top Stories")

# Chart 2
category_counts.plot(kind="bar", ax=axes[1])
axes[1].set_title("Categories")

# Chart 3
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(non_popular["score"], non_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].legend()

plt.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("✅ All charts generated successfully!")