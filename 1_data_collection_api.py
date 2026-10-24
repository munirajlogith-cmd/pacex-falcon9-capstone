"""Lab 1: collect Falcon 9 launch data from the SpaceX REST API."""
import requests
import pandas as pd
from config import SPACEX_API

launches = requests.get(SPACEX_API + "launches/past", timeout=30).json()
df = pd.json_normalize(launches)

# Keep single-core, single-payload launches, as in the lab
df = df[df["cores"].map(len) == 1]
df = df[df["payloads"].map(len) == 1]
df["core"] = df["cores"].map(lambda x: x[0])
df["payload"] = df["payloads"].map(lambda x: x[0])
df["date"] = pd.to_datetime(df["date_utc"]).dt.date
df = df[df["date"] <= pd.to_datetime("2020-11-13").date()]


def lookup(endpoint, key, field):
    """Resolve an id to a field value via the API (cached per id)."""
    cache = {}
    out = []
    for _id in df[key]:
        if _id not in cache:
            cache[_id] = requests.get(f"{SPACEX_API}{endpoint}/{_id}", timeout=30).json()[field]
        out.append(cache[_id])
    return out


df["BoosterVersion"] = lookup("rockets", "rocket", "name")
df["PayloadMass"] = lookup("payloads", "payload", "mass_kg")
df["Orbit"] = lookup("payloads", "payload", "orbit")
df["LaunchSite"] = lookup("launchpads", "launchpad", "name")

df = df[df["BoosterVersion"] == "Falcon 9"].reset_index(drop=True)
df["FlightNumber"] = range(1, len(df) + 1)
df.to_csv("dataset_part_1_collected.csv", index=False)
print(df.shape)
print(df[["FlightNumber", "date", "BoosterVersion", "PayloadMass", "Orbit", "LaunchSite"]].head())
