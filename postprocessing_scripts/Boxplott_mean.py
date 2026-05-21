# Plotting av finger speed fra statistics.json

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# =========================
# Brukervalg
# =========================

roi = "storage"

# Velg hvilken statistics.json som skal brukes
results_path = Path(
    r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex1\fingers\statistics.json"
)

print("Leser data fra:")
print(results_path.resolve())


# Sjekk at filen faktisk finnes
if not results_path.is_file():
    raise FileNotFoundError(f"Fant ikke filen: {results_path}")


# =========================
# Les statistics.json
# =========================

with open(results_path, "r") as f:
    results = json.load(f)


# =========================
# Hent ut speed-data
# =========================

times = results["times"]
paths = results["paths"][roi]

distributions = []

# speed[i] hører til intervallet mellom time[i] og time[i+1]
# derfor bruker vi times[1:]
for time in times[1:]:

    speeds_at_time = []

    for path_name, path_data in paths.items():

        # Hopp over "roi", "statistics", osv.
        if not path_name.startswith("path_"):
            continue

        path_times = path_data["time"]
        path_speeds = path_data["speed"]

        for t, speed in zip(path_times[1:], path_speeds):
            if t == time:
                speeds_at_time.append(speed)

    distributions.append(speeds_at_time)


# Fjern eventuelle tomme tidspunkter
filtered_times = []
filtered_distributions = []

for time, distribution in zip(times[1:], distributions):
    if len(distribution) > 0:
        filtered_times.append(time)
        filtered_distributions.append(distribution)


# =========================
# Beregn mean speed
# =========================

mean_speeds = []

for distribution in filtered_distributions:

    values = np.array(distribution, dtype=float)

    values = values[np.isfinite(values)]

    if len(values) > 0:
        mean_speeds.append(np.mean(values))
    else:
        mean_speeds.append(np.nan)


# =========================
# Plot
# =========================

from matplotlib.lines import Line2D
from matplotlib.patches import Patch

times_hours = [t / 3600 for t in filtered_times]

plt.figure(figsize=(15, 7))

box = plt.boxplot(
    filtered_distributions,
    positions=times_hours,
    widths=1.0,
    showfliers=False,
    patch_artist=True,
    boxprops=dict(facecolor="white", edgecolor="black", linewidth=2),
    whiskerprops=dict(color="black", linewidth=2),
    capprops=dict(color="black", linewidth=2),
    medianprops=dict(color="darkorange", linewidth=3.5),
)

# Plot mean speed som blå linje
plt.plot(
    times_hours,
    mean_speeds,
    color="tab:blue",
    linewidth=3,
    marker="o",
    markersize=5,
    label="Mean finger speed",
)

tick_step = 3  # vis hver tredje verdi på x-aksen

plt.xticks(
    times_hours[::tick_step],
    [f"{int(np.round(t))}" for t in times_hours[::tick_step]],
    rotation=45,
    ha="right",
    fontsize=22,
)

plt.yticks(fontsize=22)

plt.xlabel("Time [h]", fontsize=24)
plt.ylabel("Finger speed [m/s]", fontsize=24)

ax = plt.gca()
ax.yaxis.get_offset_text().set_fontsize(24)

# Fjern rutenett
plt.grid(False)

# Legend
legend_elements = [
    Patch(
        facecolor="white",
        edgecolor="black",
        linewidth=2,
        label="Middle 50% of measured finger speeds",
    ),
    Line2D(
        [0],
        [0],
        color="darkorange",
        linewidth=3.5,
        label="Median finger speed",
    ),
    Line2D(
        [0],
        [0],
        color="tab:blue",
        linewidth=3,
        marker="o",
        label="Mean finger speed",
    ),
]

plt.legend(
    handles=legend_elements,
    fontsize=15,
    loc="upper right",
)

plt.tight_layout()
plt.show()