"""Lab 6: interactive launch-site map with Folium. Open spacex_map.html and screenshot it."""
import math
import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition
from config import LAUNCH_GEO

df = pd.read_csv(LAUNCH_GEO)[["Launch Site", "Lat", "Long", "class"]]
sites = df.groupby("Launch Site", as_index=False).first()

m = folium.Map(location=[29.56, -95.09], zoom_start=4)
for _, r in sites.iterrows():
    loc = [r["Lat"], r["Long"]]
    folium.Circle(loc, radius=1000, color="#d35400", fill=True).add_child(
        folium.Popup(r["Launch Site"])).add_to(m)

# Success (green) / failure (red) markers per launch
cluster = MarkerCluster().add_to(m)
for _, r in df.iterrows():
    colour = "green" if r["class"] == 1 else "red"
    folium.Marker([r["Lat"], r["Long"]], icon=folium.Icon(color=colour)).add_to(cluster)


def distance_km(lat1, lon1, lat2, lon2):
    R = 6373.0
    a = (math.sin(math.radians(lat2 - lat1) / 2) ** 2 + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2)) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# Proximity: set the coordinates of the nearest coastline/railway/highway/city
# by hovering the map with MousePosition, then fill in below.
MousePosition().add_to(m)
proximity = {  # name: (lat, lon)  <- replace with the points you pick on the map
    "coastline": (28.56342, -80.56794),
}
site = sites[sites["Launch Site"].str.contains("40")].iloc[0]  # CCAFS SLC-40
for name, (lat, lon) in proximity.items():
    d = distance_km(site["Lat"], site["Long"], lat, lon)
    folium.PolyLine([[site["Lat"], site["Long"]], [lat, lon]], weight=1).add_to(m)
    folium.Marker([lat, lon], icon=folium.DivIcon(
        html=f'<div style="font-size:12px;color:#d35400"><b>{d:.2f} KM</b></div>')).add_to(m)
    print(f"{name}: {d:.2f} km from {site['Launch Site']}")

m.save("spacex_map.html")
