import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from collections import defaultdict
    from datetime import timedelta
    from pathlib import Path
    from urllib.parse import urlparse
    from urllib.request import urlopen

    import geopandas as gpd
    import pandas as pd
    from pystac_client import Client
    from shapely.geometry import shape
    from shapely.ops import unary_union

    return (
        Client,
        Path,
        defaultdict,
        gpd,
        pd,
        timedelta,
        unary_union,
        urlopen,
        urlparse,
    )


@app.cell
def _(Path):
    DEA_STAC_URL = "https://explorer.dea.ga.gov.au/stac/"
    SENTINEL_COLLECTIONS = ["ga_s2am_ard_3", "ga_s2bm_ard_3", "ga_s2cm_ard_3"]
    LANDSAT_COLLECTIONS = [
        "ga_ls5t_ard_3",
        "ga_ls7e_ard_3",
        "ga_ls8c_ard_3",
        "ga_ls9c_ard_3",
    ]
    # Narrow window: acquisition_date is known exactly, so ±5 days is enough
    SEARCH_WINDOW_DAYS = 5
    AOI_PATH = Path(__file__).parent.parent / "data/vector/study_areas.geojson"
    OUTPUT_ROOT = Path("../outputs/satellite_imagery")
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    return (
        AOI_PATH,
        DEA_STAC_URL,
        LANDSAT_COLLECTIONS,
        OUTPUT_ROOT,
        SEARCH_WINDOW_DAYS,
        SENTINEL_COLLECTIONS,
    )


@app.cell
def _(AOI_PATH, gpd, pd):
    _raw = gpd.read_file(AOI_PATH).to_crs(4326)
    _raw["acquisition_date"] = pd.to_datetime(
        _raw["acquisition_date"], errors="coerce"
    ).dt.date
    study_areas = _raw.dropna(subset=["acquisition_date"]).copy()
    n_dropped = len(_raw) - len(study_areas)
    return n_dropped, study_areas


@app.cell
def _(mo, n_dropped, study_areas):
    mo.vstack(
        [
            mo.md(
                f"**Study areas with acquisition dates:** {len(study_areas)}  \n"
                f"**Dropped (no acquisition date):** {n_dropped}"
            ),
            mo.ui.table(
                study_areas[["name", "region", "status", "acquisition_date"]]
                .reset_index(drop=True)
            ),
        ]
    )
    return


@app.cell
def _(
    Client,
    DEA_STAC_URL,
    LANDSAT_COLLECTIONS,
    SEARCH_WINDOW_DAYS,
    SENTINEL_COLLECTIONS,
    defaultdict,
    mo,
    pd,
    study_areas,
    timedelta,
    unary_union,
):
    _client = Client.open(DEA_STAC_URL)

    def _search_collections(collections, aoi_geom, target_date, window_days):
        date_start = target_date - timedelta(days=window_days)
        date_end = target_date + timedelta(days=window_days)
        try:
            results = _client.search(
                collections=collections,
                intersects=aoi_geom.__geo_interface__,
                datetime=f"{date_start.isoformat()}/{date_end.isoformat()}",
                limit=500,
            )
            return list(results.items())
        except Exception as exc:
            print(f"Search failed for {collections}: {exc}")
            return []

    # Dissolve AOI geometries per unique acquisition date
    _date_geoms = defaultdict(list)
    for _, _row in study_areas.iterrows():
        _date_geoms[_row["acquisition_date"]].append(_row.geometry)

    search_rows = []
    scene_items = []

    for _acq_date, _geoms in sorted(_date_geoms.items()):
        _aoi_geom = unary_union(_geoms)
        for _sensor_type, _collections in [
            ("sentinel", SENTINEL_COLLECTIONS),
            ("landsat", LANDSAT_COLLECTIONS),
        ]:
            _items = _search_collections(
                _collections, _aoi_geom, _acq_date, SEARCH_WINDOW_DAYS
            )
            for _item in _items:
                _coll = _item.collection_id or _item.properties.get(
                    "collection", "unknown"
                )
                _scene_date = (
                    _item.datetime.date() if _item.datetime else None
                )
                search_rows.append(
                    {
                        "acquisition_date": _acq_date,
                        "sensor_type": _sensor_type,
                        "collection": _coll,
                        "scene_id": _item.id,
                        "scene_date": _scene_date,
                        "n_assets": len(_item.assets),
                    }
                )
                scene_items.append(
                    {
                        "acquisition_date": _acq_date,
                        "sensor_type": _sensor_type,
                        "collection": _coll,
                        "item": _item,
                    }
                )

    search_summary = pd.DataFrame(search_rows)

    mo.vstack(
        [
            mo.md(f"**Total scenes found:** {len(search_summary)}"),
            mo.ui.table(
                search_summary.drop(columns=["n_assets"], errors="ignore")
                if not search_summary.empty
                else search_summary
            ),
        ]
    ) if not search_summary.empty else mo.md("⚠️ No scenes found.")
    return (scene_items,)


@app.cell
def _(OUTPUT_ROOT, Path, mo, pd, scene_items, urlopen, urlparse):
    _RASTER_TYPES = {
        "image/tiff",
        "image/geotiff",
        "image/tiff; application=geotiff",
        "image/tiff; application=geotiff; profile=cloud-optimized",
    }

    def _is_raster(asset):
        if asset.media_type:
            # Normalise by stripping trailing parameters for comparison
            base_type = asset.media_type.lower().split(";")[0].strip()
            if base_type in {"image/tiff", "image/geotiff"}:
                return True
        href = (asset.href or "").lower()
        return href.split("?")[0].endswith((".tif", ".tiff"))

    def _download(url, dest, chunk_size=1024 * 1024):
        if dest.exists() and dest.stat().st_size > 0:
            return dest
        dest.parent.mkdir(parents=True, exist_ok=True)
        parsed = urlparse(url)
        if parsed.scheme == "s3":
            import boto3
            from botocore import UNSIGNED
            from botocore.config import Config

            s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
            with dest.open("wb") as fh:
                s3.download_fileobj(parsed.netloc, parsed.path.lstrip("/"), fh)
            return dest
        with urlopen(url) as resp, dest.open("wb") as fh:
            while chunk := resp.read(chunk_size):
                fh.write(chunk)
        return dest

    download_rows = []

    for _entry in mo.status.progress_bar(
        scene_items,
        title="Downloading assets",
        subtitle="scene",
        remove_on_exit=True,
    ):
        _acq_date = _entry["acquisition_date"]
        _sensor_type = _entry["sensor_type"]
        _collection = _entry["collection"]
        _item = _entry["item"]
        _item_dir = (
            OUTPUT_ROOT
            / str(_acq_date)
            / _sensor_type
            / _collection
            / _item.id
        )

        for _asset_key, _asset in _item.assets.items():
            if not _is_raster(_asset):
                continue
            _href = _asset.href
            _suffix = Path(_href.split("?", 1)[0]).suffix or ".tif"
            _dest = _item_dir / f"{_asset_key}{_suffix}"
            try:
                _download(_href, _dest)
                _status = "ok"
            except Exception as exc:
                _status = f"error: {exc}"
            download_rows.append(
                {
                    "acquisition_date": _acq_date,
                    "sensor_type": _sensor_type,
                    "collection": _collection,
                    "scene_id": _item.id,
                    "asset": _asset_key,
                    "path": str(_dest),
                    "status": _status,
                }
            )

    download_manifest = pd.DataFrame(download_rows)
    return (download_manifest,)


@app.cell
def _(download_manifest, mo):
    if download_manifest.empty:
        _out = mo.md("⚠️ No assets downloaded.")
    else:
        _n_ok = (download_manifest["status"] == "ok").sum()
        _n_err = (download_manifest["status"] != "ok").sum()
        _out = mo.vstack(
            [
                mo.md(
                    f"**Downloaded:** {_n_ok} assets ✅  \n"
                    f"**Errors:** {_n_err} ❌"
                ),
                mo.ui.table(download_manifest),
            ]
        )
    _out
    return


if __name__ == "__main__":
    app.run()
