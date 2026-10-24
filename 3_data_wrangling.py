"""Lab 3: data wrangling - missing values, orbit/outcome counts, landing Class label."""
import pandas as pd
from config import DATASET_PART_1

df = pd.read_csv(DATASET_PART_1)

print("Missing % per column:\n", (df.isnull().mean() * 100).round(2))
print("\nLaunches per site:\n", df["LaunchSite"].value_counts())
print("\nLaunches per orbit:\n", df["Orbit"].value_counts())

outcomes = df["Outcome"].value_counts()
print("\nOutcomes:\n", outcomes)

# Bad outcomes = landing not successful
bad = {o for o in outcomes.index if o.startswith("False") or o == "None None"}
df["Class"] = df["Outcome"].apply(lambda o: 0 if o in bad else 1)

print("\nSuccess rate: %.2f%%" % (df["Class"].mean() * 100))
df.to_csv("dataset_part_2_mine.csv", index=False)
