import pandas as pd
import glob


# Find JSON files in the data folder
json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("No JSON file found in data/ folder.")
    exit()

# Use the first matching JSON file
json_file = json_files[0]

# Load JSON data into DataFrame
df = pd.read_json(json_file)
print(f"Loaded {len(df)} stories from {json_file}")

# Remove duplicate rows based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Remove rows with missing post_id, title, or score
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Remove extra spaces from title
df["title"] = df["title"].astype(str).str.strip()

# Convert score and num_comments to integers safely
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Drop invalid numeric rows
df = df.dropna(subset=["score", "num_comments"])

# Convert to integer type
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low quality stories with score less than 5
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Save cleaned data to CSV
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)
print(f"\nSaved {len(df)} rows to {output_file}")

# Print stories per category
print("\nStories per category:")
print(df["category"].value_counts())