import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


roi = "storage"

threshold_files = {
    "Threshold: 0.1": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex2\Lav_threshold\fingers\statistics.json",
    "Threshold: 0.3": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex2\God_threshold\fingers\statistics.json",
    "Threshold: 0.6": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex2\Høy_threshold\fingers\statistics.json",
}

colors = {
    "Threshold: 0.1": "#fdd0a2",   # lys oransje
    "Threshold: 0.3": "#f16913",   # medium oransje
    "Threshold: 0.6": "#7f2704",   # mørk oransje
}

def load_results(statistics_path):
    statistics_path = Path(statistics_path)

    print("Leser data fra:")
    print(statistics_path.resolve())

    if not statistics_path.is_file():
        raise FileNotFoundError(f"Fant ikke filen: {statistics_path}")

    with open(statistics_path, "r") as f:
        return json.load(f)


def load_all_speeds(statistics_path, roi="storage"):
    results = load_results(statistics_path)
    paths = results["paths"][roi]

    all_speeds = []

    for path_name, path_data in paths.items():
        if not path_name.startswith("path_"):
            continue

        all_speeds.extend(path_data["speed"])

    all_speeds = np.array(all_speeds, dtype=float)
    all_speeds = all_speeds[np.isfinite(all_speeds)]

    return all_speeds


def load_number_of_tracked_fingers(statistics_path, roi="storage"):
    results = load_results(statistics_path)

    times = results["times"]
    paths = results["paths"][roi]

    number_of_fingers = []

    for time in times:
        count = 0

        for path_name, path_data in paths.items():
            if not path_name.startswith("path_"):
                continue

            if time in path_data["time"]:
                count += 1

        number_of_fingers.append(count)

    times_hours = np.array(times, dtype=float) / 3600
    number_of_fingers = np.array(number_of_fingers, dtype=int)

    return times_hours, number_of_fingers


# =========================
# Plot 1: Speed distribution
# =========================

plt.figure(figsize=(12, 7))

for label, path in threshold_files.items():
    values = load_all_speeds(path, roi=roi)

    mean = np.mean(values)
    std = np.std(values, ddof=1)

    x = np.linspace(mean - 4 * std, mean + 4 * std, 300)
    y = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(
        -0.5 * ((x - mean) / std) ** 2
    )

    plt.plot(
    x,
    y,
    linewidth=4 if label == "Threshold: 0.3" else 3,
    color=colors[label],
    label=f"{label} | σ={std:.1e}",
)

plt.xlabel("Finger speed [m/s]", fontsize=24)
plt.ylabel("Normalized frequency [-]", fontsize=24)

ax = plt.gca()
ax.yaxis.get_offset_text().set_fontsize(24)

ax = plt.gca()
ax.xaxis.get_offset_text().set_fontsize(24)

plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.legend(fontsize=22)

plt.grid(True)
plt.tight_layout()
plt.show()