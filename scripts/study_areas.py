#!/usr/bin/env python3
"""
Study area maps for PhD Methods section.

Three-panel layout:
  A — Northern sites cluster (Harman River, Stanley River, Wilson River)
  B — Davey River
  C — Tasmania overview (boundary, towns, CAPAD, inset boxes for A & B)

Three style variations saved to outputs/figures/:
  study_areas_v1_minimal.{pdf,png}
  study_areas_v2_earthy.{pdf,png}
  study_areas_v3_mono.{pdf,png}

Usage:
  pixi run python scripts/study_areas.py
"""

from pathlib import Path

import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from shapely.geometry import box

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "vector"
OUT = ROOT / "outputs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

CRS = "EPSG:7855"  # GDA2020 / MGA Zone 55 — all source files already in this CRS

# ── Load data ──────────────────────────────────────────────────────────────────
print("Loading vector data…")
study_areas = gpd.read_file(DATA / "study_areas.geojson").to_crs(CRS)
tas_boundary = gpd.read_file(DATA / "tasmania_boundary.geojson").to_crs(CRS)
towns = gpd.read_file(DATA / "gazetted_town_names.geojson").to_crs(CRS)
capad = gpd.read_file(DATA / "CAPAD_TAS.geojson").to_crs(CRS)
watercourses = gpd.read_file(DATA / "watercourse_lines.geojson").to_crs(CRS)

# Fix potential topology issues in CAPAD (common with downloaded protected area data)
capad["geometry"] = capad.geometry.buffer(0)

# Site groups
northern = study_areas[
    study_areas["name"].isin(["Harman River", "Stanley River", "Wilson River"])
].copy()
davey = study_areas[study_areas["name"] == "Davey River"].copy()

# ── Extent helpers ─────────────────────────────────────────────────────────────


def padded_bounds(gdf, frac=0.20):
    """Return (xmin, xmax, ymin, ymax) with proportional padding."""
    minx, miny, maxx, maxy = gdf.total_bounds
    pad = max(maxx - minx, maxy - miny) * frac
    return minx - pad, maxx + pad, miny - pad, maxy + pad


north_ext = padded_bounds(northern, frac=0.15)
davey_ext = padded_bounds(davey, frac=0.15)


def tas_extent():
    minx, miny, maxx, maxy = tas_boundary.total_bounds
    px, py = (maxx - minx) * 0.03, (maxy - miny) * 0.03
    return minx - px, maxx + px, miny - py, maxy + py


# ── Watercourse helper (191k features — always clip to extent) ─────────────────


def subset_watercourses(extent):
    xmin, xmax, ymin, ymax = extent
    wc = watercourses.cx[xmin:xmax, ymin:ymax]  # fast bbox filter
    if wc.empty:
        return wc
    try:
        return gpd.clip(wc, box(xmin, ymin, xmax, ymax))
    except Exception:
        return wc


# ── Map utilities ──────────────────────────────────────────────────────────────


def apply_frame(ax, extent):
    xmin, xmax, ymin, ymax = extent
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color("#888888")


def add_scale_bar(ax, length_m, label=None, loc="lower right"):
    """Alternating black/white scale bar."""
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    xr, yr = xlim[1] - xlim[0], ylim[1] - ylim[0]
    bar_h = yr * 0.013
    mx, my = xr * 0.04, yr * 0.04
    x0 = xlim[1] - mx - length_m if "right" in loc else xlim[0] + mx
    y0 = ylim[0] + my if "lower" in loc else ylim[1] - my - bar_h * 3
    half = length_m / 2
    for start, fc in [(x0, "black"), (x0 + half, "white")]:
        ax.add_patch(
            mpatches.Rectangle(
                (start, y0), half, bar_h, fc=fc, ec="black", lw=0.6, zorder=12
            )
        )
    if label is None:
        label = f"{int(length_m / 1000)} km" if length_m >= 1000 else f"{int(length_m)} m"
    ax.text(
        x0 + length_m / 2, y0 + bar_h * 1.8, label,
        ha="center", va="bottom", fontsize=6, zorder=12,
    )


def add_north_arrow(ax, xf=0.06, yf=0.86):
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    xr, yr = xlim[1] - xlim[0], ylim[1] - ylim[0]
    cx, cy = xlim[0] + xf * xr, ylim[0] + yf * yr
    dy = yr * 0.07
    ax.annotate(
        "", xy=(cx, cy + dy), xytext=(cx, cy),
        arrowprops=dict(arrowstyle="-|>", color="black", lw=1.2, mutation_scale=9),
        zorder=12,
    )
    ax.text(cx, cy + dy * 1.35, "N", ha="center", va="bottom",
            fontsize=7, fontweight="bold", zorder=12)


def panel_label(ax, letter):
    ax.text(-0.02, 1.04, letter, transform=ax.transAxes,
            fontsize=11, fontweight="bold", va="bottom", ha="right")


def inset_box(ax, extent, color, lw=1.2, label=None):
    xmin, xmax, ymin, ymax = extent
    ax.add_patch(
        mpatches.Rectangle(
            (xmin, ymin), xmax - xmin, ymax - ymin,
            lw=lw, ec=color, fc="none", zorder=6,
        )
    )
    if label:
        ylim = ax.get_ylim()
        offset = (ylim[1] - ylim[0]) * 0.012
        ax.text(
            xmin + (xmax - xmin) / 2, ymax + offset, label,
            ha="center", va="bottom", fontsize=7, fontweight="bold",
            color=color, zorder=7,
        )


# ── Style definitions ──────────────────────────────────────────────────────────
STYLES = {
    "v1_minimal": {
        "name": "Minimal",
        # Detail panels
        "land_bg": "#F5F5F5",
        "ocean_bg": "#D6E8F2",
        "site_fill": "#0072B2",   # Okabe-Ito blue
        "site_edge": "#003D66",
        "site_alpha": 0.55,
        "wc_color": "#74ADD1",
        "wc_lw": 0.5,
        # Overview
        "capad_fill": None,       # clean — no CAPAD fill
        "tas_fill": "#EFEFEF",
        "tas_edge": "#BBBBBB",
        "town_fc": "#333333",
        "town_marker": "o",
        "town_ms": 3,
        "inset_color": "#D55E00",  # Okabe-Ito vermillion
        # Site labels
        "label_fc": "white",
        "label_stroke": "#003D66",
    },
    "v2_earthy": {
        "name": "Earthy",
        "land_bg": "#EDE8D0",
        "ocean_bg": "#C4D8E2",
        "site_fill": "#8B3A0F",
        "site_edge": "#4A1E07",
        "site_alpha": 0.65,
        "wc_color": "#4F7EA0",
        "wc_lw": 0.6,
        "capad_fill": "#A8C88B",   # sage green protected areas
        "capad_alpha": 0.45,
        "tas_fill": "#DDD5B8",
        "tas_edge": "#9E8B6C",
        "town_fc": "#2C1A0E",
        "town_marker": "^",
        "town_ms": 3.5,
        "inset_color": "#8B3A0F",
        "label_fc": "white",
        "label_stroke": "#4A1E07",
    },
    "v3_mono": {
        "name": "Monochrome",
        "land_bg": "#EEEEEE",
        "ocean_bg": "#F5F5F5",
        "site_fill": "#222222",
        "site_edge": "#000000",
        "site_alpha": 0.40,
        "wc_color": "#888888",
        "wc_lw": 0.5,
        "capad_fill": "#CCCCCC",   # light grey protected areas
        "capad_alpha": 0.55,
        "tas_fill": "#DDDDDD",
        "tas_edge": "#999999",
        "town_fc": "#111111",
        "town_marker": "o",
        "town_ms": 3,
        "inset_color": "#333333",
        "label_fc": "white",
        "label_stroke": "#000000",
    },
}

# ── Figure builder ─────────────────────────────────────────────────────────────


def make_figure(style_key):
    s = STYLES[style_key]
    print(f"  Building '{s['name']}' variant…")

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 8,
        "axes.linewidth": 0.6,
        "figure.dpi": 150,
    })

    # 3 equal-width columns; 183 mm ≈ 7.2 in (double-column journal width)
    fig, (ax_n, ax_d, ax_o) = plt.subplots(
        1, 3, figsize=(7.2, 3.6),
        gridspec_kw={"wspace": 0.12},
    )

    # ── A: Northern sites (Harman, Stanley, Wilson) ────────────────────────────
    ax_n.set_facecolor(s["land_bg"])
    wc_n = subset_watercourses(north_ext)
    if not wc_n.empty:
        wc_n.plot(ax=ax_n, color=s["wc_color"], lw=s["wc_lw"], zorder=2)
    northern.plot(
        ax=ax_n, color=s["site_fill"], alpha=s["site_alpha"],
        edgecolor=s["site_edge"], linewidth=1.3, zorder=3,
    )
    for _, row in northern.iterrows():
        c = row.geometry.centroid
        short = row["name"].replace(" River", "\nRiver")
        ax_n.text(
            c.x, c.y, short, ha="center", va="center",
            fontsize=5.5, fontweight="bold", color=s["label_fc"],
            path_effects=[pe.withStroke(linewidth=1.8, foreground=s["label_stroke"])],
            zorder=5,
        )
    apply_frame(ax_n, north_ext)
    add_scale_bar(ax_n, 2000)
    add_north_arrow(ax_n)
    panel_label(ax_n, "A")

    # ── B: Davey River ─────────────────────────────────────────────────────────
    ax_d.set_facecolor(s["land_bg"])
    wc_d = subset_watercourses(davey_ext)
    if not wc_d.empty:
        wc_d.plot(ax=ax_d, color=s["wc_color"], lw=s["wc_lw"], zorder=2)
    davey.plot(
        ax=ax_d, color=s["site_fill"], alpha=s["site_alpha"],
        edgecolor=s["site_edge"], linewidth=1.3, zorder=3,
    )
    for _, row in davey.iterrows():
        c = row.geometry.centroid
        short = row["name"].replace(" River", "\nRiver")
        ax_d.text(
            c.x, c.y, short, ha="center", va="center",
            fontsize=5.5, fontweight="bold", color=s["label_fc"],
            path_effects=[pe.withStroke(linewidth=1.8, foreground=s["label_stroke"])],
            zorder=5,
        )
    apply_frame(ax_d, davey_ext)
    add_scale_bar(ax_d, 2000)
    add_north_arrow(ax_d)
    panel_label(ax_d, "B")

    # ── C: Tasmania overview ───────────────────────────────────────────────────
    te = tas_extent()
    ax_o.set_facecolor(s["ocean_bg"])

    if s.get("capad_fill"):
        capad.plot(
            ax=ax_o, color=s["capad_fill"],
            alpha=s.get("capad_alpha", 0.4), edgecolor="none", zorder=1,
        )
    tas_boundary.plot(
        ax=ax_o, color=s["tas_fill"],
        edgecolor=s["tas_edge"], linewidth=0.7, zorder=2,
    )
    study_areas.plot(
        ax=ax_o, color=s["site_fill"], alpha=s["site_alpha"],
        edgecolor=s["site_edge"], linewidth=0.8, zorder=4,
    )
    inset_box(ax_o, north_ext, color=s["inset_color"], lw=1.1, label="A")
    inset_box(ax_o, davey_ext, color=s["inset_color"], lw=1.1, label="B")

    # Town markers + labels (small x offset to avoid marker overlap)
    apply_frame(ax_o, te)
    xr = te[1] - te[0]
    dx = xr * 0.018   # label offset — ~1.8% of map width
    for _, row in towns.iterrows():
        pt = row.geometry
        ax_o.plot(
            pt.x, pt.y, marker=s["town_marker"],
            color=s["town_fc"], ms=s["town_ms"],
            mec="white", mew=0.5, zorder=5,
        )
        ax_o.text(
            pt.x + dx, pt.y, row["NAME"],
            fontsize=5.5, color=s["town_fc"],
            va="center", ha="left", zorder=6,
        )

    add_scale_bar(ax_o, 50_000, label="50 km")
    add_north_arrow(ax_o)
    panel_label(ax_o, "C")

    # ── Legend ─────────────────────────────────────────────────────────────────
    legend_handles = [
        mpatches.Patch(
            fc=s["site_fill"], alpha=s["site_alpha"],
            ec=s["site_edge"], label="Study area",
        ),
        Line2D([0], [0], color=s["wc_color"], lw=1.2, label="Watercourse"),
        Line2D(
            [0], [0], marker=s["town_marker"], color="none",
            mfc=s["town_fc"], ms=4, label="Town",
        ),
    ]
    if s.get("capad_fill"):
        legend_handles.insert(
            1,
            mpatches.Patch(
                fc=s["capad_fill"], alpha=s.get("capad_alpha", 0.4),
                ec="none", label="Protected area",
            ),
        )
    fig.legend(
        handles=legend_handles, loc="lower center",
        ncol=len(legend_handles), fontsize=6.5,
        frameon=False, bbox_to_anchor=(0.5, -0.05),
    )

    # ── Save ───────────────────────────────────────────────────────────────────
    for fmt in ("pdf", "png"):
        path = OUT / f"study_areas_{style_key}.{fmt}"
        fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white", format=fmt)
        print(f"    → {path}")
    plt.close(fig)


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    for key in STYLES:
        print(f"\n── {STYLES[key]['name']} ──")
        make_figure(key)
    print("\nDone. Outputs in outputs/figures/")
