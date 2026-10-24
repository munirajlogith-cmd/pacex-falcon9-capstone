"""Lab 5: EDA with matplotlib/seaborn. Each figure is saved as a PNG for the slides."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import DATASET_PART_2

df = pd.read_csv(DATASET_PART_2)
sns.set_theme(style="whitegrid")


def save(name):
    plt.tight_layout()
    plt.savefig(name, dpi=150)
    plt.close()


# Flight number vs launch site, coloured by outcome
sns.catplot(data=df, x="FlightNumber", y="LaunchSite", hue="Class", aspect=3)
save("fig_flight_vs_site.png")

# Payload vs launch site
sns.catplot(data=df, x="PayloadMass", y="LaunchSite", hue="Class", aspect=3)
save("fig_payload_vs_site.png")

# Success rate by orbit
df.groupby("Orbit")["Class"].mean().sort_values().plot(kind="barh", figsize=(7, 5))
plt.xlabel("Success rate")
save("fig_success_by_orbit.png")

# Flight number vs orbit
sns.catplot(data=df, x="FlightNumber", y="Orbit", hue="Class", aspect=3)
save("fig_flight_vs_orbit.png")

# Yearly success trend
df["Year"] = pd.to_datetime(df["Date"]).dt.year
df.groupby("Year")["Class"].mean().plot(marker="o", figsize=(7, 4))
plt.ylabel("Success rate")
save("fig_yearly_trend.png")

# Feature engineering for modelling
features = df[["FlightNumber", "PayloadMass", "Orbit", "LaunchSite", "Flights",
               "GridFins", "Reused", "Legs", "LandingPad", "Block",
               "ReusedCount", "Serial"]]
features_one_hot = pd.get_dummies(features, columns=["Orbit", "LaunchSite", "LandingPad", "Serial"])
features_one_hot = features_one_hot.astype("float64")
features_one_hot.to_csv("dataset_part_3_mine.csv", index=False)
print(features_one_hot.shape)
