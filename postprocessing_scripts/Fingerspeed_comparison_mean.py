import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# =========================
# Brukervalg
# =========================

roi = "storage"


# =========================
# Eksperimenter
# =========================

experiments = {
    "Ex1": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex1\fingers\statistics.json",

    "Ex2": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex2\fingers\statistics.json",

    "Ex3": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex3\fingers\statistics.json",

    "Ex4": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex4\fingers\statistics.json",

    "Ex6": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex6\fingers\statistics.json",

    "Ex7": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex7\fingers\statistics.json",

    "Ex9": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex9\fingers\statistics.json",

    "Ex10": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex10\fingers\statistics.json",
}

colors = {
    "Ex1": "tab:blue",
    "Ex2": "tab:orange",
    "Ex3": "tab:green",
    "Ex4": "tab:red",
    "Ex6": "tab:cyan",
    "Ex7": "tab:olive",
    "Ex9": "tab:purple",
    "Ex10": "tab:brown",
} 

# =========================
# Funksjon for å hente mean speed
# =========================

def load_mean_speed(statistics_path, roi="storage"):

    statistics_path = Path(statistics_path)

    print("Leser data fra:")
    print(statistics_path.resolve())

    if not statistics_path.is_file():
        raise FileNotFoundError(f"Fant ikke filen: {statistics_path}")

    with open(statistics_path, "r") as f:
        results = json.load(f)

    paths = results["paths"][roi]

    # time -> liste med speeds
    speed_by_time = {}

    # Gå gjennom alle finger-paths
    for path_name, path_data in paths.items():

        if not path_name.startswith("path_"):
            continue

        times = path_data["time"]
        speeds = path_data["speed"]

        # speed[i] gjelder mellom time[i] og time[i+1]
        for time, speed in zip(times[1:], speeds):

            if time not in speed_by_time:
                speed_by_time[time] = []

            speed_by_time[time].append(speed)

    times_sorted = sorted(speed_by_time.keys())

    times_hours = []
    mean_speeds = []
    stderr_speeds = []

    for time in times_sorted:

        values = np.array(speed_by_time[time], dtype=float)

        # fjern NaN
        values = values[np.isfinite(values)]

        if len(values) == 0:

            mean_speed = np.nan
            stderr_speed = np.nan

        else:

            mean_speed = np.mean(values)

            # Standard error
            if len(values) > 1:
                stderr_speed = (
                    np.std(values, ddof=1)
                    / np.sqrt(len(values))
                )
            else:
                stderr_speed = 0

        times_hours.append(time / 3600)
        mean_speeds.append(mean_speed)
        stderr_speeds.append(stderr_speed)

    return (
        np.array(times_hours),
        np.array(mean_speeds),
        np.array(stderr_speeds),
    )


# =========================
# Plot
# =========================

plt.figure(figsize=(12, 7))

for name, path in experiments.items():

    times_hours, mean_speeds, stderr_speeds = load_mean_speed(
        path,
        roi=roi,
    )

    plt.plot(
    times_hours,
    mean_speeds,

    # yerr=stderr_speeds,   # kommentert ut

    marker="o",
    linewidth=2,

    # elinewidth=1,         # kommentert ut
    # capsize=3,            # kommentert ut

    alpha=0.8,
    color=colors[name],
    label=name,
)
# =========================
# Figur-layout
# =========================

plt.xlabel("Time [h]", fontsize=24)
plt.ylabel(
    "Mean finger speed [m/s]",
    fontsize=24,)
ax = plt.gca()
ax.yaxis.get_offset_text().set_fontsize(24)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.legend(fontsize=17)
plt.grid(True)

# Sett y-akse slik at outliers ikke ødelegger figuren
plt.ylim(0, 6e-6)
plt.tight_layout()
plt.show()