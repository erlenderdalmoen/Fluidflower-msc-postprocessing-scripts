import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# =========================
# Eksperimenter
# =========================
# Du kan enten skrive direkte til statistics.csv
# eller til en mappe som inneholder statistics.csv et sted under seg.

experiments = {
    "Ex1": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex1",
    "Ex2": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex2",
    "Ex3": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex3",
    "Ex4": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex4",
    "Ex6": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex6",
    "Ex7": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex7",
    "Ex9": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex9",
    "Ex10": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex10",
}


# Samme standardfarger som Matplotlib bruker i finger speed-plottet
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


def find_statistics_csv(path):
    path = Path(path)

    if path.is_file() and path.name == "statistics.csv":
        return path

    matches = list(path.rglob("statistics.csv"))

    if len(matches) == 0:
        raise FileNotFoundError(f"Fant ingen statistics.csv under: {path}")

    if len(matches) > 1:
        print(f"Fant flere statistics.csv under {path}:")
        for m in matches:
            print("  ", m)
        print("Bruker den første:", matches[0])

    return matches[0]


def load_contour_length(path):
    csv_path = find_statistics_csv(path)

    print("Leser data fra:")
    print(csv_path.resolve())

    times = []
    contour_lengths = []

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)

        if "time" not in reader.fieldnames:
            raise KeyError(f"Mangler kolonnen 'time' i {csv_path}")

        if "contour_length" not in reader.fieldnames:
            raise KeyError(f"Mangler kolonnen 'contour_length' i {csv_path}")

        for row in reader:
            time = float(row["time"])
            contour_length = float(row["contour_length"])

            times.append(time / 3600)  # sekunder til timer
            contour_lengths.append(contour_length)

    return np.array(times), np.array(contour_lengths)


# =========================
# Plot
# =========================

plt.figure(figsize=(12, 7))

for name, path in experiments.items():
    times_hours, contour_lengths = load_contour_length(path)

    plt.plot(
        times_hours,
        contour_lengths,
        marker="o",
        linewidth=2.5,
        markersize=6,
        color=colors[name],
        label=name,
    )

plt.xlabel("Time [h]", fontsize=22)
plt.ylabel("Contour length [m]", fontsize=22)
ax = plt.gca()
ax.yaxis.get_offset_text().set_fontsize(24)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.legend(fontsize=16)
plt.grid(True)

plt.tight_layout()
plt.show()