import marimo

__generated_with = "0.19.11"
app = marimo.App(width="full")


@app.cell
def _():
    from pathlib import Path

    import geopandas as gpd
    import marimo as mo
    import pandas as pd
    import plotnine as p9
    from shapely.geometry import box as shapely_box

    return Path, gpd, mo, p9, pd, shapely_box


@app.cell
def _(mo):
    mo.md("""
    # Study Area Maps — Methods Section

    Three-panel figure: **A** northern sites cluster, **B** Davey River,
    **C** Tasmania overview. Pick a style variant below — the panels and
    export update reactively.
    """)
    return


@app.cell
def _(Path, gpd):
    CRS = "EPSG:7855"
    DATA = Path("../data/vector")

    study_areas = gpd.read_file(DATA / "study_areas.geojson").to_crs(CRS)
    tas_boundary = gpd.read_file(DATA / "tasmania_boundary.geojson").to_crs(CRS)
    towns = gpd.read_file(DATA / "gazetted_town_names.geojson").to_crs(CRS)
    capad = gpd.read_file(DATA / "CAPAD_TAS.geojson").to_crs(CRS)
    watercourses = gpd.read_file(DATA / "watercourse_lines.geojson").to_crs(CRS)

    # Fix CAPAD topology and dissolve for faster rendering (4677 → 1 feature)
    capad["geometry"] = capad.geometry.buffer(0)
    capad_dissolved = capad.dissolve()

    # Extract coordinates for geom_point / geom_text
    towns["x"] = towns.geometry.x
    towns["y"] = towns.geometry.y
    return capad_dissolved, study_areas, tas_boundary, towns, watercourses


@app.cell
def _(study_areas, tas_boundary):
    def _pad(gdf, frac=0.20):
        minx, miny, maxx, maxy = gdf.total_bounds
        pad = max(maxx - minx, maxy - miny) * frac
        return (minx - pad, maxx + pad, miny - pad, maxy + pad)

    northern = study_areas[
        study_areas["name"].isin(
            ["Harman River", "Stanley River", "Wilson River"]
        )
    ].copy()
    davey = study_areas[study_areas["name"] == "Davey River"].copy()

    north_ext = _pad(northern, 0.15)
    davey_ext = _pad(davey, 0.15)

    _b = tas_boundary.total_bounds
    _px, _py = (_b[2] - _b[0]) * 0.03, (_b[3] - _b[1]) * 0.03
    tas_ext = (_b[0] - _px, _b[2] + _px, _b[1] - _py, _b[3] + _py)

    # Centroid columns for labelling
    northern["cx"] = northern.geometry.centroid.x
    northern["cy"] = northern.geometry.centroid.y
    northern["short_name"] = northern["name"].str.replace(
        " River", "\nRiver", regex=False
    )
    davey["cx"] = davey.geometry.centroid.x
    davey["cy"] = davey.geometry.centroid.y
    davey["short_name"] = davey["name"].str.replace(
        " River", "\nRiver", regex=False
    )
    return davey, davey_ext, north_ext, northern, tas_ext


@app.cell
def _(mo):
    style_picker = mo.ui.dropdown(
        options={
            "Minimal": "v1_minimal",
            "Earthy": "v2_earthy",
            "Monochrome": "v3_mono",
        },
        value="Minimal",
        label="Style",
    )
    style_picker
    return (style_picker,)


@app.cell
def _(style_picker):
    _PALETTES = {
        "v1_minimal": dict(
            land_bg="#F5F5F5",
            ocean_bg="#D6E8F2",
            site_fill="#0072B2",
            site_edge="#003D66",
            site_alpha=0.55,
            wc_color="#74ADD1",
            wc_lw=0.3,
            capad_fill=None,
            tas_fill="#EFEFEF",
            tas_edge="#BBBBBB",
            town_fc="#333333",
            town_shape="o",
            town_ms=2,
            inset_color="#D55E00",
            label_color="white",
        ),
        "v2_earthy": dict(
            land_bg="#EDE8D0",
            ocean_bg="#C4D8E2",
            site_fill="#8B3A0F",
            site_edge="#4A1E07",
            site_alpha=0.65,
            wc_color="#4F7EA0",
            wc_lw=0.35,
            capad_fill="#A8C88B",
            capad_alpha=0.45,
            tas_fill="#DDD5B8",
            tas_edge="#9E8B6C",
            town_fc="#2C1A0E",
            town_shape="^",
            town_ms=2.5,
            inset_color="#8B3A0F",
            label_color="white",
        ),
        "v3_mono": dict(
            land_bg="#EEEEEE",
            ocean_bg="#F5F5F5",
            site_fill="#222222",
            site_edge="#000000",
            site_alpha=0.40,
            wc_color="#888888",
            wc_lw=0.3,
            capad_fill="#CCCCCC",
            capad_alpha=0.55,
            tas_fill="#DDDDDD",
            tas_edge="#999999",
            town_fc="#111111",
            town_shape="o",
            town_ms=2,
            inset_color="#333333",
            label_color="white",
        ),
    }
    S = _PALETTES[style_picker.value]
    return (S,)


@app.cell
def _(gpd, shapely_box, watercourses):
    def clip_wc(extent):
        """Spatial subset of 191k watercourse features to a map extent."""
        xmin, xmax, ymin, ymax = extent
        wc = watercourses.cx[xmin:xmax, ymin:ymax]
        if wc.empty:
            return wc
        try:
            return gpd.clip(wc, shapely_box(xmin, ymin, xmax, ymax))
        except Exception:
            return wc

    return (clip_wc,)


@app.cell
def _(p9):
    def detail_theme(S, figsize=(2.4, 3.4)):
        """plotnine theme for the detail panels (A & B)."""
        return (
            p9.theme_void()
            + p9.theme(
                figure_size=figsize,
                panel_background=p9.element_rect(fill=S["land_bg"]),
                panel_border=p9.element_rect(
                    color="#888888", fill="none", size=0.5
                ),
                plot_title=p9.element_text(size=9, weight="bold"),
            )
        )

    def add_decorations(plot, extent, scale_m, scale_label=None):
        """Append scale bar + north arrow annotation layers to *plot*."""
        xmin, xmax, ymin, ymax = extent
        xr, yr = xmax - xmin, ymax - ymin

        # ── scale bar ──
        h = yr * 0.013
        x0 = xmax - xr * 0.04 - scale_m
        y0 = ymin + yr * 0.04
        half = scale_m / 2
        if scale_label is None:
            scale_label = (
                f"{int(scale_m / 1000)} km"
                if scale_m >= 1000
                else f"{int(scale_m)} m"
            )
        plot = (
            plot
            + p9.annotate(
                "rect",
                xmin=x0,
                xmax=x0 + half,
                ymin=y0,
                ymax=y0 + h,
                fill="black",
                color="black",
                size=0.3,
            )
            + p9.annotate(
                "rect",
                xmin=x0 + half,
                xmax=x0 + scale_m,
                ymin=y0,
                ymax=y0 + h,
                fill="white",
                color="black",
                size=0.3,
            )
            + p9.annotate(
                "text",
                x=x0 + scale_m / 2,
                y=y0 + h * 2.5,
                label=scale_label,
                size=6,
                ha="center",
            )
        )

        # ── north arrow ──
        cx = xmin + xr * 0.06
        cy = ymin + yr * 0.86
        dy = yr * 0.07
        plot = (
            plot
            + p9.annotate(
                "segment",
                x=cx,
                xend=cx,
                y=cy,
                yend=cy + dy,
                arrow=p9.arrow(length=0.15, type="closed"),
                size=0.8,
                color="black",
            )
            + p9.annotate(
                "text",
                x=cx,
                y=cy + dy * 1.5,
                label="N",
                size=7,
                fontweight="bold",
                ha="center",
            )
        )
        return plot

    return add_decorations, detail_theme


@app.cell
def _(S, add_decorations, clip_wc, detail_theme, north_ext, northern, p9):
    _ext = north_ext
    _wc = clip_wc(_ext)

    p_north = p9.ggplot()
    if not _wc.empty:
        p_north = p_north + p9.geom_map(
            data=_wc, color=S["wc_color"], size=S["wc_lw"]
        )
    p_north = (
        p_north
        + p9.geom_map(
            data=northern,
            fill=S["site_fill"],
            color=S["site_edge"],
            alpha=S["site_alpha"],
            size=0.6,
        )
        + p9.geom_text(
            data=northern,
            mapping=p9.aes(x="cx", y="cy", label="short_name"),
            color=S["label_color"],
            size=6,
            fontweight="bold",
        )
        + p9.coord_fixed(
            ratio=1, xlim=(_ext[0], _ext[1]), ylim=(_ext[2], _ext[3])
        )
        + detail_theme(S)
        + p9.ggtitle("A  Northern Sites")
    )
    p_north = add_decorations(p_north, _ext, 2000)
    return (p_north,)


@app.cell
def _(S, add_decorations, clip_wc, davey, davey_ext, detail_theme, p9):
    _ext = davey_ext
    _wc = clip_wc(_ext)

    p_davey = p9.ggplot()
    if not _wc.empty:
        p_davey = p_davey + p9.geom_map(
            data=_wc, color=S["wc_color"], size=S["wc_lw"]
        )
    p_davey = (
        p_davey
        + p9.geom_map(
            data=davey,
            fill=S["site_fill"],
            color=S["site_edge"],
            alpha=S["site_alpha"],
            size=0.6,
        )
        + p9.geom_text(
            data=davey,
            mapping=p9.aes(x="cx", y="cy", label="short_name"),
            color=S["label_color"],
            size=6,
            fontweight="bold",
        )
        + p9.coord_fixed(
            ratio=1, xlim=(_ext[0], _ext[1]), ylim=(_ext[2], _ext[3])
        )
        + detail_theme(S)
        + p9.ggtitle("B  Davey River")
    )
    p_davey = add_decorations(p_davey, _ext, 2000)
    return (p_davey,)


@app.cell
def _(
    S,
    add_decorations,
    capad_dissolved,
    davey_ext,
    north_ext,
    p9,
    pd,
    study_areas,
    tas_boundary,
    tas_ext,
    towns,
):
    _ext = tas_ext
    _nudge_y = (_ext[3] - _ext[2]) * 0.015
    _nudge_x = (_ext[1] - _ext[0]) * 0.018

    # Inset-box coordinates
    _boxes = pd.DataFrame(
        [
            dict(
                xmin=north_ext[0],
                xmax=north_ext[1],
                ymin=north_ext[2],
                ymax=north_ext[3],
                cx=(north_ext[0] + north_ext[1]) / 2,
                ytop=north_ext[3],
                label="A",
            ),
            dict(
                xmin=davey_ext[0],
                xmax=davey_ext[1],
                ymin=davey_ext[2],
                ymax=davey_ext[3],
                cx=(davey_ext[0] + davey_ext[1]) / 2,
                ytop=davey_ext[3],
                label="B",
            ),
        ]
    )

    p_overview = p9.ggplot()

    # Optional CAPAD (protected areas)
    if S.get("capad_fill"):
        p_overview = p_overview + p9.geom_map(
            data=capad_dissolved,
            fill=S["capad_fill"],
            alpha=S.get("capad_alpha", 0.4),
            color="none",
            size=0,
        )

    p_overview = (
        p_overview
        # Tasmania land
        + p9.geom_map(
            data=tas_boundary,
            fill=S["tas_fill"],
            color=S["tas_edge"],
            size=0.5,
        )
        # Study sites
        + p9.geom_map(
            data=study_areas,
            fill=S["site_fill"],
            color=S["site_edge"],
            alpha=S["site_alpha"],
            size=0.5,
        )
        # Inset boxes
        + p9.geom_rect(
            data=_boxes,
            mapping=p9.aes(
                xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"
            ),
            fill="none",
            color=S["inset_color"],
            size=0.7,
            inherit_aes=False,
        )
        # Inset box labels
        + p9.geom_text(
            data=_boxes,
            mapping=p9.aes(x="cx", y="ytop", label="label"),
            color=S["inset_color"],
            size=7,
            fontweight="bold",
            va="bottom",
            nudge_y=_nudge_y,
            inherit_aes=False,
        )
        # Town markers
        + p9.geom_point(
            data=towns,
            mapping=p9.aes(x="x", y="y"),
            shape=S["town_shape"],
            color=S["town_fc"],
            size=S["town_ms"],
            inherit_aes=False,
        )
        # Town labels
        + p9.geom_text(
            data=towns,
            mapping=p9.aes(x="x", y="y", label="NAME"),
            color=S["town_fc"],
            size=5.5,
            ha="left",
            nudge_x=_nudge_x,
            inherit_aes=False,
        )
        + p9.coord_fixed(
            ratio=1, xlim=(_ext[0], _ext[1]), ylim=(_ext[2], _ext[3])
        )
        + p9.theme_void()
        + p9.theme(
            figure_size=(2.4, 3.4),
            panel_background=p9.element_rect(fill=S["ocean_bg"]),
            panel_border=p9.element_rect(
                color="#888888", fill="none", size=0.5
            ),
            plot_title=p9.element_text(size=9, weight="bold"),
        )
        + p9.ggtitle("C  Tasmania")
    )
    p_overview = add_decorations(p_overview, _ext, 50_000, "50 km")
    return (p_overview,)


@app.cell
def _(mo, p_davey, p_north, p_overview):
    mo.hstack(
        [p_north, p_davey, p_overview],
        justify="center",
        widths="equal",
    )
    return


@app.cell
def _(Path, mo, p_davey, p_north, p_overview, style_picker):
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt
    from io import BytesIO

    _OUT = Path("outputs/figures")
    _OUT.mkdir(parents=True, exist_ok=True)
    _tag = style_picker.value

    # Individual panel PDFs (vector) and PNGs
    for _name, _plot in [
        ("north", p_north),
        ("davey", p_davey),
        ("overview", p_overview),
    ]:
        for _fmt in ("pdf", "png"):
            _plot.save(
                _OUT / f"study_areas_{_tag}_{_name}.{_fmt}",
                dpi=300,
                verbose=False,
            )

    # Combined raster figure via matplotlib composition
    _fig, _axes = plt.subplots(1, 3, figsize=(7.2, 3.6))
    for _ax, _plot in zip(_axes, [p_north, p_davey, p_overview]):
        _buf = BytesIO()
        _plot.save(_buf, format="png", dpi=300, verbose=False)
        _buf.seek(0)
        _ax.imshow(mpimg.imread(_buf))
        _ax.axis("off")
    _fig.tight_layout(pad=0.2)
    for _fmt in ("pdf", "png"):
        _fig.savefig(
            _OUT / f"study_areas_{_tag}.{_fmt}",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
        )
    plt.close(_fig)

    mo.md(
        f"""
        **Exported** `outputs/figures/study_areas_{_tag}.*`
        — individual panels (PDF + PNG) and combined figure.
        """
    )
    return


if __name__ == "__main__":
    app.run()
