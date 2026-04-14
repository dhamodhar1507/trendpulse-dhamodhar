import pandas as pd
import numpy as np

# Load the cleaned CSV file
df = pd.read_csv("data/trends_clean.csv")

# Print first 5 rows
print("Loaded data:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# Print average score and average comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print("\nAverage score :", avg_score)
print("Average comments:", avg_comments)

# NumPy analysis
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()
categories = df["category"].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print("Mean score   :", mean_score)
print("Median score :", median_score)
print("Std deviation:", std_score)
print("Max score    :", max_score)
print("Min score    :", min_score)

# Category with most stories
unique_categories, counts = np.unique(categories, return_counts=True)
max_category_index = np.argmax(counts)
most_common_category = unique_categories[max_category_index]
most_common_count = counts[max_category_index]

print(f"\nMost stories in: {most_common_category} ({most_common_count} stories)")

# Story with most comments
max_comments_index = np.argmax(comments)
most_commented_title = df.loc[max_comments_index, "title"]
most_comments_value = df.loc[max_comments_index, "num_comments"]

print(f'\nMost commented story: "{most_commented_title}" - {most_comments_value} comments')

# Add new columns
df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > avg_score

# Save result
output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")