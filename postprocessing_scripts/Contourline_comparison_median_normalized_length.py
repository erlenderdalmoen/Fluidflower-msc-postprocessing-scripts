import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# =========================
# Eksperimenter
# =========================

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


# =========================
# Samme farger som tidligere
# =========================

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
# Finn statistics.csv
# =========================

def find_statistics_csv(path):

    path = Path(path)

    # Hvis path allerede peker direkte til statistics.csv
    if path.is_file() and path.name == "statistics.csv":
        return path

    # Søk rekursivt
    matches = list(path.rglob("statistics.csv"))

    if len(matches) == 0:
        raise FileNotFoundError(
            f"Fant ingen statistics.csv under: {path}"
        )

    if len(matches) > 1:

        print(f"Fant flere statistics.csv under {path}:")
        for m in matches:
            print("  ", m)

        print("Bruker den første:", matches[0])

    return matches[0]


# =========================
# Last contour length
# =========================

def load_contour_length(path):

    csv_path = find_statistics_csv(path)

    print("Leser data fra:")
    print(csv_path.resolve())

    times = []
    contour_lengths = []

    with open(csv_path, "r", newline="") as f:

        reader = csv.DictReader(f)

        if "time" not in reader.fieldnames:
            raise KeyError(
                f"Mangler kolonnen 'time' i {csv_path}"
            )

        if "contour_length" not in reader.fieldnames:
            raise KeyError(
                f"Mangler kolonnen 'contour_length' i {csv_path}"
            )

        for row in reader:

            time = float(row["time"])
            contour_length = float(row["contour_length"])

            # sekunder -> timer
            times.append(time / 3600)

            contour_lengths.append(contour_length)

    return (
        np.array(times),
        np.array(contour_lengths),
    )


# =========================
# Plot normalized contour length
# =========================

plt.figure(figsize=(12, 7))

for name, path in experiments.items():

    times_hours, contour_lengths = load_contour_length(path)

    # Normaliser mot maksverdi
    max_contour_length = np.max(contour_lengths)

    normalized_contour_lengths = (
        contour_lengths / max_contour_length
    )

    plt.plot(
        times_hours,
        normalized_contour_lengths,
        marker="o",
        linewidth=2.5,
        markersize=6,
        color=colors[name],
        label=name,
    )


# =========================
# Figur-layout
# =========================

plt.xlabel(
    "Time [h]",
    fontsize=22,
)

plt.ylabel(
   "Relative contour length $L/L_{\mathrm{max}}$ [-]",
    fontsize=22,
)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.ylim(0, 1.05)

plt.legend(fontsize=16)

plt.grid(True)

plt.tight_layout()

plt.show()