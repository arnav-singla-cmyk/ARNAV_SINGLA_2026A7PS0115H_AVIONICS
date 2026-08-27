import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# ============================================================
# 1. LOAD THE CSV DATA
# ============================================================

# Path of the CSV file containing the ship's depth data
file_name = r"C:\Users\mysin\OneDrive\Desktop\Arnav Singla\Depth Data.csv"

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(file_name)

# Convert the Point column into numeric time values
# Invalid values are converted to NaN
time = pd.to_numeric(data["Point"], errors="coerce")

# Convert the Depth column into numeric depth values
depth = pd.to_numeric(data["Depth (m)"], errors="coerce")


# ============================================================
# 2. CLEAN THE DEPTH DATA
# ============================================================

# Remove unrealistic depth values
# Any absolute depth greater than 1000 m is considered invalid
depth.loc[depth.abs() > 1000] = np.nan

# Treat zero depth values as invalid/missing data
depth.loc[depth == 0] = np.nan

# Fill missing values by linear interpolation
depth_clean = depth.interpolate(method="linear")

# If missing values remain at the beginning or end,
# fill them using the nearest available value
depth_clean = depth_clean.bfill().ffill()


# ============================================================
# 3. SMOOTH THE DEPTH DATA
# ============================================================

# Number of data points used for calculating the moving average
window_size = 7

# Apply a centered moving average to reduce noise
depth_smooth = depth_clean.rolling(
    window=window_size,
    center=True,
    min_periods=1
).mean()

# Fill any remaining missing values
depth_smooth = depth_smooth.bfill().ffill()


# ============================================================
# 4. REMOVE INVALID ROWS
# ============================================================

# Keep only rows where:
# - Time is valid
# - Cleaned depth is valid
# - Smoothed depth is valid
valid = (
    time.notna()
    & depth_clean.notna()
    & depth_smooth.notna()
)

# Remove invalid rows and reset the index
time = time[valid].reset_index(drop=True)
depth_clean = depth_clean[valid].reset_index(drop=True)
depth_smooth = depth_smooth[valid].reset_index(drop=True)


# ============================================================
# 5. SORT DATA ACCORDING TO TIME
# ============================================================

# Get the order of rows required to arrange time from
# smallest to largest
sort_order = np.argsort(time.values)

# Apply the same sorting order to all columns
time = time.iloc[sort_order].reset_index(drop=True)
depth_clean = depth_clean.iloc[sort_order].reset_index(drop=True)
depth_smooth = depth_smooth.iloc[sort_order].reset_index(drop=True)


# ============================================================
# 6. SET ANIMATION PARAMETERS
# ============================================================

# Number of frames shown every second
FPS = 2

# Use every data point from the CSV as an animation frame
# This makes the animation cover the complete dataset
animation_times = time.to_numpy()

# Total number of frames in the animation
TOTAL_FRAMES = len(animation_times)

# Find the starting and ending time values
start_time = float(time.iloc[0])
end_time = float(time.iloc[-1])


# ============================================================
# 7. CONVERT DATA TO NUMPY ARRAYS
# ============================================================

# NumPy arrays make the animation calculations faster
time_values = time.to_numpy()
clean_values = depth_clean.to_numpy()
smooth_values = depth_smooth.to_numpy()


# ============================================================
# 8. CALCULATE Y-AXIS LIMITS
# ============================================================

# Combine cleaned and smoothed depth values
# so that both graphs fit properly on the Y-axis
all_depth_values = np.concatenate([
    clean_values,
    smooth_values
])

# Find minimum and maximum depth
depth_min = float(np.min(all_depth_values))
depth_max = float(np.max(all_depth_values))

# Calculate the range of depth values
depth_range = depth_max - depth_min

# Add 10% space above and below the graph
# Minimum margin is set to 1 metre
margin = max(depth_range * 0.10, 1)


# ============================================================
# 9. CREATE THE GRAPH
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

# Set the X-axis to cover the complete time range
ax.set_xlim(start_time, end_time)

# Set the Y-axis limits with some extra margin
ax.set_ylim(
    depth_min - margin,
    depth_max + margin
)

# Label the X-axis
ax.set_xlabel(
    "Time (seconds)",
    fontsize=12
)

# Label the Y-axis
ax.set_ylabel(
    "Depth (m)",
    fontsize=12
)

# Set the graph title
ax.set_title(
    "Ship Depth vs Time",
    fontsize=15,
    fontweight="bold"
)

# Add a light grid to make the graph easier to read
ax.grid(
    True,
    alpha=0.3
)


# ============================================================
# 10. CREATE THE TWO ANIMATED LINES
# ============================================================

# Line showing the cleaned depth data
(cleaned_line,) = ax.plot(
    [],
    [],
    color="#90EE90",
    linewidth=2.8,
    alpha=0.95,
    label="Cleaned Depth",
    zorder=1
)

# Line showing the smoothed depth data
(smoothed_line,) = ax.plot(
    [],
    [],
    color="#FFD700",
    linewidth=3,
    alpha=1.0,
    label="Smoothed Depth",
    zorder=2
)


# ============================================================
# 11. CREATE THE LIVE DATA DISPLAY
# ============================================================

# Create a text box inside the graph
# It will display the current time and depth
value_text = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    fontsize=12,
    fontweight="bold",
    verticalalignment="top",
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="white",
        edgecolor="black",
        alpha=0.9
    ),
    zorder=4
)

# Display the legend
ax.legend(loc="upper right")


# ============================================================
# 12. INITIALIZE THE ANIMATION
# ============================================================

def init():

    # Start with both lines empty
    cleaned_line.set_data([], [])
    smoothed_line.set_data([], [])

    # Clear the live data display
    value_text.set_text("")

    return (
        cleaned_line,
        smoothed_line,
        value_text
    )


# ============================================================
# 13. UPDATE THE GRAPH FOR EACH FRAME
# ============================================================

def update(frame):

    # Get the time corresponding to the current frame
    current_time = animation_times[frame]

    # Include all data points up to the current frame
    index = frame + 1

    # Get X and Y values for the cleaned depth line
    cleaned_x = time_values[:index]
    cleaned_y = clean_values[:index]

    # Get X and Y values for the smoothed depth line
    smooth_x = time_values[:index]
    smooth_y = smooth_values[:index]

    # Update the cleaned depth line
    cleaned_line.set_data(
        cleaned_x,
        cleaned_y
    )

    # Update the smoothed depth line
    smoothed_line.set_data(
        smooth_x,
        smooth_y
    )

    # Update the live time and depth display
    value_text.set_text(
        f"Time : {current_time:.2f} s\n"
        f"Depth : {clean_values[frame]:.2f} m"
    )

    return (
        cleaned_line,
        smoothed_line,
        value_text
    )


# ============================================================
# 14. CREATE THE ANIMATION
# ============================================================

animation = FuncAnimation(
    fig,

    # Function that updates the graph
    update,

    # Number of frames to display
    frames=TOTAL_FRAMES,

    # Function used to initialize the animation
    init_func=init,

    # 1000 ms = 1 second between frames
    interval=1000 / FPS,

    # Do not use blitting
    blit=False,

    # Play the animation only once
    repeat=False
)


# ============================================================
# 15. DISPLAY THE GRAPH
# ============================================================

# Automatically adjust spacing so labels don't overlap
plt.tight_layout()

# Show the animated graph
plt.show()
