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
    #"Ex1": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex1\fingers\statistics.json",
    "Ex2": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex2\fingers\statistics.json",
    "Ex3": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex3\fingers\statistics.json",
    "Ex4": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex4\fingers\statistics.json",
    #"Ex6": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex6\fingers\statistics.json",
    #"Ex7": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex7\fingers\statistics.json",
    #"Ex9": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex9\fingers\statistics.json",
    #"Ex10": r"C:\Users\erlen\OneDrive - University of Bergen\Master\Results_DarSIA\Ex10\fingers\statistics.json",
}

colors = {
    #"Ex1": "tab:blue",
    "Ex2": "tab:orange",
    "Ex3": "tab:green",
    "Ex4": "tab:red",
    #"Ex6": "tab:cyan",
    #"Ex7": "tab:olive",
    #"Ex9": "tab:purple",
    #"Ex10": "tab:brown",
}


# =========================
# Funksjon for å hente median speed
# =========================

def load_median_speed(statistics_path, roi="storage"):
    statistics_path = Path(statistics_path)

    with open(statistics_path, "r") as f:
        results = json.load(f)

    paths = results["paths"][roi]

    speed_by_time = {}

    for path_name, path_data in paths.items():
        if not path_name.startswith("path_"):
            continue

        times = path_data["time"]
        speeds = path_data["speed"]

        #Endre fra og til 24 timer
        for t, s in zip(times[1:], speeds):
            #if t / 3600 > 24:
                #continue
            speed_by_time.setdefault(t, []).append(s)

    # Sort and convert
    times_h = []
    med = []

    for t in sorted(speed_by_time.keys()):
        values = np.array(speed_by_time[t], dtype=float)
        values = values[np.isfinite(values)]
        if len(values) == 0:
            continue
        times_h.append(t / 3600)
        med.append(np.median(values))

    return np.array(times_h), np.array(med)


# =========================
# Plot
# =========================

plt.figure(figsize=(12, 7))

all_interp = []
all_times = []

min_time = float("inf")
max_time = 0

# Load all experiments
for name, path in experiments.items():
    t, v = load_median_speed(path, roi=roi)

    if len(t) == 0:
        continue

    min_time = min(min_time, t[0])
    max_time = max(max_time, t[-1])

    # Plot each experiment
    plt.plot(t, v, marker="o", linewidth=2, alpha=0.85, color=colors[name], label=name)

    all_times.append((t, v))


# =========================
# Felles tidsakse kun der det finnes ekte data
# =========================

common_time = np.linspace(min_time, max_time, 200)

# Interpoler alle eksperimenter til denne aksen
for t, v in all_times:
    all_interp.append(np.interp(common_time, t, v))

mean_speed = np.nanmean(all_interp, axis=0)

# =========================
# Lineær regresjon kun på faktisk dataområde
# =========================

coef = np.polyfit(common_time, mean_speed, 1)
trend = np.polyval(coef, common_time)

start_speed = trend[0]
end_speed = trend[-1]
delta = end_speed - start_speed
delta_text = f"{delta:.2e} m/s"

# =========================
# Plot trendlinjen redusert
# =========================

plt.plot(
    common_time,
    trend,
    linestyle="--",
    linewidth=1.5,
    alpha=0.45,
    color="black",
    label=f"Δ = {delta_text}"
)


# =========================
# Figur-layout
# =========================

plt.xlabel("Time [h]", fontsize=24)
plt.ylabel("Median finger speed [m/s]", fontsize=24)

ax = plt.gca()
ax.yaxis.get_offset_text().set_fontsize(24)

plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

plt.legend(fontsize=16)
plt.grid(True)

plt.ylim(0, 6e-6)

plt.tight_layout()
plt.show()


# =========================
# Utskrift
# =========================

print("\n=== KVANTITATIV UTVIKLING I FINGER SPEED ===")
print(f"Første faktiske tidspunkt: {min_time:.2f} h")
print(f"Siste faktiske tidspunkt: {max_time:.2f} h")
print(f"Startverdi trend: {start_speed:.3e} m/s")
print(f"Sluttverdi trend: {end_speed:.3e} m/s")
print(f"Endring: {delta:.3e} m/s\n")
