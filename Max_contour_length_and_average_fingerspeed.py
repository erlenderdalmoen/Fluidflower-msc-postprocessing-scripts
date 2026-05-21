from pathlib import Path
import json
import pandas as pd
import numpy as np

folder = Path(r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex10\fingers")

csv_file = folder / "statistics.csv"
json_file = folder / "statistics.json"

# --- Maximum contour length ---
df = pd.read_csv(csv_file)
max_contour_length = df["contour_length"].max()

# --- Median finger speed ---
with open(json_file, "r") as f:
    data = json.load(f)

all_speeds = []

for path_name, path_data in data["paths"]["storage"].items():
    if path_name == "roi":
        continue

    speeds = path_data.get("speed", [])
    all_speeds.extend(speeds)

median_finger_speed = np.median(all_speeds)

print("Median finger speed:", median_finger_speed, "m/s")
print("Maximum contour length:", max_contour_length, "m")