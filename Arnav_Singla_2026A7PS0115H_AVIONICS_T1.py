import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

file_name = r"C:\Users\mysin\OneDrive\Desktop\Arnav Singla\Depth Data.csv"

data = pd.read_csv(file_name)

time = pd.to_numeric(data["Point"], errors="coerce")
depth = pd.to_numeric(data["Depth (m)"], errors="coerce")

depth.loc[depth.abs() > 1000] = np.nan
depth.loc[depth == 0] = np.nan

depth_clean = depth.interpolate(method="linear")
depth_clean = depth_clean.bfill().ffill()

window_size = 7

depth_smooth = depth_clean.rolling(
    window=window_size, center=True, min_periods=1
).mean()

depth_smooth = depth_smooth.bfill().ffill()

valid = time.notna() & depth_clean.notna() & depth_smooth.notna()

time = time[valid].reset_index(drop=True)
depth_clean = depth_clean[valid].reset_index(drop=True)
depth_smooth = depth_smooth[valid].reset_index(drop=True)

sort_order = np.argsort(time.values)

time = time.iloc[sort_order].reset_index(drop=True)
depth_clean = depth_clean.iloc[sort_order].reset_index(drop=True)
depth_smooth = depth_smooth.iloc[sort_order].reset_index(drop=True)


ANIMATION_SECONDS = 10
FPS = 60
TOTAL_FRAMES = ANIMATION_SECONDS * FPS

start_time = float(time.iloc[0])
end_time = float(time.iloc[-1])

animation_times = np.linspace(start_time, end_time, TOTAL_FRAMES)

time_values = time.to_numpy()
clean_values = depth_clean.to_numpy()
smooth_values = depth_smooth.to_numpy()

all_depth_values = np.concatenate([clean_values, smooth_values])

depth_min = float(np.min(all_depth_values))
depth_max = float(np.max(all_depth_values))

depth_range = depth_max - depth_min
margin = max(depth_range * 0.10, 1)


fig, ax = plt.subplots(figsize=(12, 6))

ax.set_xlim(start_time, end_time)

ax.set_ylim(depth_min - margin, depth_max + margin)

ax.set_xlabel("Time (seconds)", fontsize=12)

ax.set_ylabel("Depth (m)", fontsize=12)

ax.set_title("Ship Depth vs Time", fontsize=15, fontweight="bold")

ax.grid(True, alpha=0.3)


(cleaned_line,) = ax.plot(
    [], [], color="#90EE90", linewidth=2.8, alpha=0.95, label="Cleaned Depth", zorder=1
)


(smoothed_line,) = ax.plot(
    [], [], color="#FFD700", linewidth=3, alpha=1.0, label="Smoothed Depth", zorder=2
)


value_text = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    fontsize=12,
    fontweight="bold",
    verticalalignment="top",
    bbox=dict(
        boxstyle="round,pad=0.5", facecolor="white", edgecolor="black", alpha=0.9
    ),
    zorder=4,
)


ax.legend(loc="upper right")


def init():

    cleaned_line.set_data([], [])
    smoothed_line.set_data([], [])
    value_text.set_text("")

    return (cleaned_line, smoothed_line, value_text)


def update(frame):

    current_time = animation_times[frame]

    index = np.searchsorted(time_values, current_time, side="right")

    current_clean_depth = np.interp(current_time, time_values, clean_values)

    current_smooth_depth = np.interp(current_time, time_values, smooth_values)

    cleaned_x = time_values[:index]
    cleaned_y = clean_values[:index]

    smooth_x = time_values[:index]
    smooth_y = smooth_values[:index]

    cleaned_x = np.append(cleaned_x, current_time)

    cleaned_y = np.append(cleaned_y, current_clean_depth)

    smooth_x = np.append(smooth_x, current_time)

    smooth_y = np.append(smooth_y, current_smooth_depth)

    cleaned_line.set_data(cleaned_x, cleaned_y)

    smoothed_line.set_data(smooth_x, smooth_y)

    value_text.set_text(
        f"Time : {current_time:.2f} s\n" f"Depth : {current_clean_depth:.2f} m"
    )

    return (cleaned_line, smoothed_line, value_text)


animation = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    init_func=init,
    interval=1000 / FPS,
    blit=False,
    repeat=False,
)

plt.tight_layout()

plt.show()
