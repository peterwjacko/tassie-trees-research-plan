"""
Animate the Harman River field track with Huon Pine occurrence records.

Output: outputs/harman_river_track_animation.mp4
  - 30 s, 24 fps
  - Left panel : OSM basemap + track drawing + position dot + tree markers appearing
  - Right panel: elevation profile + time cursor + tree record tick marks
"""

import warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import contextily as cx
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.lines import Line2D
from zoneinfo import ZoneInfo

warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
GPX_PATH = "data/tracks/harman_river_track.gpx"
OCC_PATH = "data/vector/gt_occurrences.geojson"
OUT_PATH = "outputs/harman_river_track_animation.mp4"

AEDT = ZoneInfo("Australia/Hobart")

# ── Animation settings ────────────────────────────────────────────────────────
FPS = 24
DURATION_S = 30
N_FRAMES = FPS * DURATION_S          # 720 frames total

# ── Colour palette ────────────────────────────────────────────────────────────
C_TRACK_FADED = "#90B8D4"            # faint track not yet drawn
C_TRACK       = "#2271B3"            # drawn portion of track
C_DOT         = "#E69F00"            # current position
C_TREE        = "#44AA99"            # Huon Pine occurrences
C_ELE         = "#2271B3"            # elevation profile fill
C_CURSOR      = "#E69F00"            # time cursor
BG            = "#F9F7F2"            # figure background

# ── 1. Load & prepare track ───────────────────────────────────────────────────
print("Loading GPX…")
track = gpd.read_file(GPX_PATH, layer="track_points")
track = track.sort_values("time").reset_index(drop=True)
track["time_aedt"] = track["time"].dt.tz_convert(AEDT)

# Reproject to Web Mercator for contextily
track_merc = track.to_crs(epsg=3857)
xs = track_merc.geometry.x.values
ys = track_merc.geometry.y.values
eles = track["ele"].values.astype(float)

t_start = track["time"].iloc[0]
t_end   = track["time"].iloc[-1]
total_s = (t_end - t_start).total_seconds()

# ── 2. Load & filter occurrences ─────────────────────────────────────────────
print("Loading occurrences…")
occ = gpd.read_file(OCC_PATH)
occ["created_at"] = pd.to_datetime(occ["created_at"], utc=True)
occ = occ[(occ["created_at"] >= t_start) & (occ["created_at"] <= t_end)].copy()
occ = occ.sort_values("created_at").reset_index(drop=True)
occ_merc = occ.to_crs(epsg=3857)

# Elapsed seconds since track start for each occurrence
occ["elapsed_s"] = (occ["created_at"] - t_start).dt.total_seconds()

# Nearest track elevation for each occurrence (match by closest timestamp)
def nearest_ele(t):
    idx = (track["time"] - t).abs().argmin()
    return eles[idx]

occ["ele"] = occ["created_at"].apply(nearest_ele)

print(f"  {len(occ)} Huon Pine records spanning track window")

# ── 3. Map bounds ─────────────────────────────────────────────────────────────
pad_m = 600   # metres padding around track bounding box
x_min, x_max = xs.min() - pad_m, xs.max() + pad_m
y_min, y_max = ys.min() - pad_m, ys.max() + pad_m

# ── 4. Figure layout ──────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 7), facecolor=BG)
gs  = fig.add_gridspec(1, 2, width_ratios=[1.4, 1], wspace=0.06,
                        left=0.02, right=0.98, top=0.92, bottom=0.10)

ax_map = fig.add_subplot(gs[0])
ax_ele = fig.add_subplot(gs[1])

# ── 5. Map panel ─────────────────────────────────────────────────────────────
print("Fetching OSM basemap tiles…")
cx.add_basemap(ax_map, crs="EPSG:3857", source=cx.providers.OpenStreetMap.Mapnik,
               zoom="auto", attribution=False)
ax_map.set_xlim(x_min, x_max)
ax_map.set_ylim(y_min, y_max)
ax_map.set_axis_off()

# Faint full track (shows the route ahead)
ax_map.plot(xs, ys, color=C_TRACK_FADED, lw=1.5, alpha=0.4, zorder=2)

# Animated track line (grows each frame)
(track_line,) = ax_map.plot([], [], color=C_TRACK, lw=2.5, zorder=3,
                             solid_capstyle="round")
# Position dot
(pos_dot,) = ax_map.plot([], [], "o", color=C_DOT, ms=10, zorder=5,
                          markeredgecolor="white", markeredgewidth=1.5)

# Occurrence scatter (all invisible initially; revealed per-frame)
occ_scatter = ax_map.scatter(
    occ_merc.geometry.x, occ_merc.geometry.y,
    s=70, color=C_TREE, edgecolors="white", linewidths=0.8,
    zorder=4, alpha=0.0,   # start invisible
)

# ── 6. Elevation panel ────────────────────────────────────────────────────────
# Smooth elevation for the profile (all time, full track)
elapsed_all = (track["time"] - t_start).dt.total_seconds().values
ax_ele.fill_between(elapsed_all / 3600, eles, eles.min(),
                    color=C_ELE, alpha=0.18, zorder=1)
ax_ele.plot(elapsed_all / 3600, eles, color=C_ELE, lw=1.5, zorder=2)

# Occurrence tick marks on the elevation profile
for _, row in occ.iterrows():
    ax_ele.axvline(x=row["elapsed_s"] / 3600, color=C_TREE,
                   lw=1.0, alpha=0.0, zorder=3, ymin=0, ymax=0.12)

occ_vlines = [ch for ch in ax_ele.get_children()
              if isinstance(ch, plt.matplotlib.lines.Line2D) and ch.get_alpha() == 0.0]

# Occurrence dots on the profile (appear at their elevation)
occ_ele_scatter = ax_ele.scatter(
    occ["elapsed_s"] / 3600, occ["ele"],
    s=50, color=C_TREE, edgecolors="white", linewidths=0.8,
    zorder=4, alpha=0.0,
)

# Animated time cursor
(cursor_line,) = ax_ele.plot([], [], color=C_CURSOR, lw=2.0, zorder=5, alpha=0.9)

# Axes styling
ax_ele.set_xlim(0, total_s / 3600)
ele_pad = 15
ax_ele.set_ylim(eles.min() - ele_pad, eles.max() + ele_pad)
ax_ele.set_xlabel("Time (AEDT)", fontsize=9, color="#444")
ax_ele.set_ylabel("Elevation (m)", fontsize=9, color="#444")
ax_ele.set_facecolor(BG)
ax_ele.spines[["top", "right"]].set_visible(False)
ax_ele.tick_params(labelsize=8, colors="#666")

# X-axis ticks as AEDT hour labels
hour_ticks = np.arange(0, total_s / 3600 + 0.5, 1.0)
hour_labels = [
    (t_start + pd.Timedelta(hours=h)).tz_convert(AEDT).strftime("%H:%M")
    for h in hour_ticks
]
ax_ele.set_xticks(hour_ticks)
ax_ele.set_xticklabels(hour_labels, fontsize=7.5)

# ── 7. Labels & legend ────────────────────────────────────────────────────────
title_text = fig.text(0.50, 0.96, "Harman River Field Traverse · 21 Jan 2026",
                       ha="center", va="top", fontsize=13, color="#222",
                       fontweight="bold")

time_label = fig.text(0.50, 0.025, "", ha="center", va="bottom",
                       fontsize=10, color="#444")

legend_handles = [
    Line2D([0], [0], color=C_TRACK, lw=2.5, label="Track"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=C_DOT,
           markersize=9, label="Position"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=C_TREE,
           markersize=8, label="Lagarostrobos franklinii"),
]
ax_map.legend(handles=legend_handles, loc="lower left",
              fontsize=8, framealpha=0.85, edgecolor="#ccc")

# ── 8. Per-frame data indices ─────────────────────────────────────────────────
# Map each frame → index into the track point array
frame_elapsed_s = np.linspace(0, total_s, N_FRAMES)

def elapsed_to_track_idx(e):
    """Nearest track point index for a given elapsed time in seconds."""
    target = t_start + pd.Timedelta(seconds=float(e))
    return int((track["time"] - target).abs().argmin())

# Pre-compute per-frame track indices (fast)
frame_track_idx = np.array([elapsed_to_track_idx(e) for e in frame_elapsed_s])

# Occurrence alphas: array of shape (n_frames, n_occ)
occ_elapsed = occ["elapsed_s"].values
occ_alphas  = np.zeros((N_FRAMES, len(occ)))
for fi, fe in enumerate(frame_elapsed_s):
    occ_alphas[fi] = np.where(occ_elapsed <= fe, 1.0, 0.0)

# ── 9. Animation update function ──────────────────────────────────────────────
def update(frame):
    ti = frame_track_idx[frame]
    fe = frame_elapsed_s[frame]

    # Map: draw track up to current position
    track_line.set_data(xs[:ti+1], ys[:ti+1])
    pos_dot.set_data([xs[ti]], [ys[ti]])

    # Map: reveal tree markers
    alphas = occ_alphas[frame]
    face_colors = np.array([[*plt.matplotlib.colors.to_rgb(C_TREE), a]
                             for a in alphas])
    occ_scatter.set_facecolor(face_colors)

    # Elevation: cursor
    cursor_line.set_data([fe / 3600, fe / 3600],
                         [eles.min() - ele_pad, eles.max() + ele_pad])

    # Elevation: reveal tree dots
    ele_face_colors = np.array([[*plt.matplotlib.colors.to_rgb(C_TREE), a]
                                 for a in alphas])
    occ_ele_scatter.set_facecolor(ele_face_colors)

    # Time label
    t_now = (t_start + pd.Timedelta(seconds=float(fe))).tz_convert(AEDT)
    time_label.set_text(t_now.strftime("%H:%M  AEDT"))

    return track_line, pos_dot, occ_scatter, cursor_line, occ_ele_scatter, time_label

# ── 10. Render ────────────────────────────────────────────────────────────────
print(f"Rendering {N_FRAMES} frames at {FPS} fps…")
anim = FuncAnimation(fig, update, frames=N_FRAMES, blit=True, interval=1000/FPS)

writer = FFMpegWriter(fps=FPS, bitrate=4000,
                      extra_args=["-vcodec", "libx264", "-pix_fmt", "yuv420p"])
anim.save(OUT_PATH, writer=writer, dpi=150)
print(f"Saved → {OUT_PATH}")
