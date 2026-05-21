import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator


# =========================
# Brukervalg
# =========================

roi = "storage"
midpoint_x = 1.3725


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
# Velg hvilke eksperimenter
# =========================

#selected_experiments = [
    #"Ex1",
    #"Ex3",
    #"Ex6",
    #"Ex10",
#]

# Andre figur:
selected_experiments = [
    "Ex2",
    "Ex4",
    "Ex7",
    "Ex9",
 ]


# =========================
# Funksjon
# =========================

def calculate_difference(statistics_path):

    with open(statistics_path, "r") as f:
        results = json.load(f)

    paths = results["paths"][roi]

    x_by_time = {}

    for path_name, path_data in paths.items():

        if not path_name.startswith("path_"):
            continue

        times = path_data["time"]
        coordinates = path_data["coordinates"]

        for time, coord in zip(times, coordinates):

            x = coord[0]

            if time not in x_by_time:
                x_by_time[time] = []

            x_by_time[time].append(x)

    times_hours = []
    difference_values = []

    for time in sorted(x_by_time.keys()):

        x_values = np.array(x_by_time[time])

        n_left = np.sum(x_values < midpoint_x)
        n_right = np.sum(x_values > midpoint_x)

        difference = n_right - n_left

        times_hours.append(time / 3600)
        difference_values.append(difference)

    return times_hours, difference_values


# =========================
# Plot
# =========================

fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8),
    sharex=True,
    sharey=True,
)

axes = axes.flatten()

for ax, name in zip(axes, selected_experiments):

    path = experiments[name]

    times_hours, difference_values = calculate_difference(path)

    ax.barh(
        times_hours,
        difference_values,
        height=1.2,
        color=colors[name],
        alpha=0.8,
    )

    ax.axvline(0, color="black", linewidth=1.2)

    ax.set_title(name, fontsize=18)

    ax.grid(axis="x", alpha=0.3)

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.set_xlim(-10, 10)
    ax.set_ylim(0, 68)

    ax.tick_params(axis='both', labelsize=14)

# Felles labels
fig.supxlabel(
    "Right - left finger count [-]",
    fontsize=18,
)

fig.supylabel(
    "Time [h]",
    fontsize=18,
)

plt.tight_layout()

plt.show()