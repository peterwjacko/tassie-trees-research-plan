#!/usr/bin/env python3
"""
Module for downloading and processing satellite imagery from Digital Earth Australia.
"""

import logging
import os
from pathlib import Path

import boto3
import geopandas as gpd
import numpy as np
import pystac_client
import rasterio
from pystac.extensions.eo import EOExtension
from rasterio.mask import mask

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def search_sentinel_data(
    aoi_path,
    time_range=("2025-01-01", "2025-01-31"),
    collections=["ga_s2am_ard_3", "ga_s2bm_ard_3", "ga_s2cm_ard_3"],
    cloud_cover_threshold=10,
    stac_api_url="https://explorer.dea.ga.gov.au/stac/",
):
    """
    Search for Sentinel-2 imagery that match the specified criteria.

    Parameters:
    -----------
    aoi_path : str
        Path to the vector file containing the Area of Interest.
    time_range : tuple
        A tuple of strings in the format (start_date, end_date) in YYYY-MM-DD format.
    collections : list
        List of collection IDs to search within.
    cloud_cover_threshold : int
        Maximum acceptable cloud cover percentage (0-100).
    stac_api_url : str
        URL of the STAC API endpoint.

    Returns:
    --------
    list
        List of STAC Items that match the search criteria.
    """
    # Read the AOI file
    logger.info(f"Reading AOI from {aoi_path}")
    aoi = gpd.read_file(aoi_path)

    # Ensure the AOI is in the right CRS for searching (WGS84)
    if aoi.crs != "EPSG:4326":
        aoi = aoi.to_crs("EPSG:4326")

    # Get the geometry as GeoJSON
    geom = aoi.geometry.values[0].__geo_interface__

    # Create a STAC client
    logger.info(f"Connecting to STAC API at {stac_api_url}")
    catalog = pystac_client.Client.open(stac_api_url)

    # Search for items
    logger.info(
        f"Searching for items in collections {collections} between {time_range[0]} and {time_range[1]}"
    )
    search = catalog.search(
        collections=collections,
        datetime=f"{time_range[0]}/{time_range[1]}",
        intersects=geom,
        max_items=100,  # Adjust as needed
    )

    # Get all items
    items = list(search.get_all_items())
    logger.info(f"Found {len(items)} items initially")

    # Filter by cloud cover
    filtered_items = []
    for item in items:
        # Extract cloud cover property
        # Different collections might store cloud cover differently
        cloud_cover = None

        # Try different cloud cover property names
        for prop_name in ["eo:cloud_cover", "cloud_cover", "cloudy_pixel_percentage"]:
            if prop_name in item.properties:
                cloud_cover = item.properties[prop_name]
                break

        # Use EO extension if available
        if cloud_cover is None and EOExtension.has_extension(item):
            eo_ext = EOExtension.ext(item)
            cloud_cover = eo_ext.cloud_cover

        # If we found cloud cover and it's below threshold, add to filtered list
        if cloud_cover is not None and cloud_cover <= cloud_cover_threshold:
            filtered_items.append(item)

    logger.info(
        f"Found {len(filtered_items)} items with cloud cover <= {cloud_cover_threshold}%"
    )
    return filtered_items


def download_sentinel_data(
    items, output_dir, bands=["red", "green", "blue", "nir"], aoi_path=None
):
    """
    Download Sentinel-2 imagery assets from STAC items.

    Parameters:
    -----------
    items : list
        List of STAC items to download.
    output_dir : str
        Directory to save downloaded files.
    bands : list
        List of band names to download.
    aoi_path : str, optional
        Path to the vector file containing the Area of Interest for clipping.

    Returns:
    --------
    dict
        Dictionary of downloaded file paths by item ID and band.
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Set up boto3 client for S3 downloads
    s3 = boto3.client("s3")

    # Track downloaded files
    downloaded_files = {}

    # Read the AOI if provided
    aoi = None
    if aoi_path:
        aoi = gpd.read_file(aoi_path)
        if aoi.crs != "EPSG:4326":
            aoi = aoi.to_crs("EPSG:4326")

    # Loop through each item
    for item in items:
        item_id = item.id
        downloaded_files[item_id] = {}

        logger.info(f"Processing item {item_id}")

        # Loop through each band
        for band in bands:
            # Find the asset for the band
            if band in item.assets:
                asset = item.assets[band]

                # Get the S3 URL
                href = asset.href

                # Parse S3 URL to get bucket and key
                if href.startswith("s3://"):
                    parts = href.replace("s3://", "").split("/")
                    bucket = parts[0]
                    key = "/".join(parts[1:])

                    # Define output file path
                    out_file = output_path / f"{item_id}_{band}.tif"

                    logger.info(f"Downloading {band} band from {href} to {out_file}")

                    try:
                        # Download the file
                        s3.download_file(bucket, key, str(out_file))

                        # If AOI is provided, clip the raster
                        if aoi is not None:
                            clipped_file = output_path / f"{item_id}_{band}_clipped.tif"

                            with rasterio.open(out_file) as src:
                                # Reproject AOI to match the raster if needed
                                aoi_reprojected = aoi.to_crs(src.crs)

                                # Perform the clip
                                out_image, out_transform = mask(
                                    src, aoi_reprojected.geometry, crop=True
                                )

                                # Copy the metadata from the source
                                out_meta = src.meta.copy()

                                # Update metadata with new dimensions
                                out_meta.update(
                                    {
                                        "driver": "GTiff",
                                        "height": out_image.shape[1],
                                        "width": out_image.shape[2],
                                        "transform": out_transform,
                                    }
                                )

                                # Write the clipped raster
                                with rasterio.open(
                                    clipped_file, "w", **out_meta
                                ) as dest:
                                    dest.write(out_image)

                                # Replace the original file with clipped
                                os.remove(out_file)
                                out_file = clipped_file

                        # Add to the list of downloaded files
                        downloaded_files[item_id][band] = str(out_file)

                    except Exception as e:
                        logger.error(
                            f"Error downloading {band} band for {item_id}: {str(e)}"
                        )
                else:
                    logger.warning(f"Asset URL for {band} is not an S3 URL: {href}")
            else:
                logger.warning(f"Band {band} not found in assets for item {item_id}")

    return downloaded_files


def create_rgb_composite(downloaded_files, output_dir, suffix="_rgb_composite"):
    """
    Create RGB composites from downloaded Sentinel-2 bands.

    Parameters:
    -----------
    downloaded_files : dict
        Dictionary of downloaded file paths by item ID and band.
    output_dir : str
        Directory to save composite files.
    suffix : str
        Suffix to add to the output file names.

    Returns:
    --------
    list
        List of paths to the created RGB composites.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    composites = []

    for item_id, bands in downloaded_files.items():
        # Check if we have all the RGB bands
        if all(b in bands for b in ["red", "green", "blue"]):
            logger.info(f"Creating RGB composite for {item_id}")

            # Define output file path
            out_file = output_path / f"{item_id}{suffix}.tif"

            try:
                # Open the individual bands
                with (
                    rasterio.open(bands["red"]) as red_src,
                    rasterio.open(bands["green"]) as green_src,
                    rasterio.open(bands["blue"]) as blue_src,
                ):
                    # Read the data
                    red_data = red_src.read(1)
                    green_data = green_src.read(1)
                    blue_data = blue_src.read(1)

                    # Create the RGB array (channels first for rasterio)
                    rgb_data = np.stack([red_data, green_data, blue_data])

                    # Get metadata from one of the bands
                    out_meta = red_src.meta.copy()

                    # Update metadata for 3 bands
                    out_meta.update({"count": 3, "driver": "GTiff"})

                    # Write the composite
                    with rasterio.open(out_file, "w", **out_meta) as dest:
                        dest.write(rgb_data)

                    composites.append(str(out_file))
                    logger.info(f"RGB composite created at {out_file}")

            except Exception as e:
                logger.error(f"Error creating RGB composite for {item_id}: {str(e)}")
        else:
            logger.warning(f"Not all RGB bands available for {item_id}")

    return composites


def main(
    aoi_path,
    output_dir="./data/sentinel",
    time_range=("2025-01-01", "2025-01-31"),
    cloud_cover_threshold=10,
    bands=["red", "green", "blue", "nir"],
):
    """
    Main function to search and download Sentinel-2 data.

    Parameters:
    -----------
    aoi_path : str
        Path to the vector file containing the Area of Interest.
    output_dir : str
        Directory to save downloaded files.
    time_range : tuple
        A tuple of strings in the format (start_date, end_date) in YYYY-MM-DD format.
    cloud_cover_threshold : int
        Maximum acceptable cloud cover percentage (0-100).
    bands : list
        List of band names to download.
    """
    # Search for data
    items = search_sentinel_data(
        aoi_path=aoi_path,
        time_range=time_range,
        cloud_cover_threshold=cloud_cover_threshold,
    )

    if not items:
        logger.warning("No items found that match the criteria")
        return

    # Download data
    downloaded_files = download_sentinel_data(
        items=items, output_dir=output_dir, bands=bands, aoi_path=aoi_path
    )

    # Create RGB composites
    composites = create_rgb_composite(
        downloaded_files=downloaded_files, output_dir=output_dir
    )

    logger.info(f"Processing complete. Created {len(composites)} RGB composites.")
    return composites


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download and process Sentinel-2 imagery"
    )
    parser.add_argument(
        "aoi_path", help="Path to the vector file containing the Area of Interest"
    )
    parser.add_argument(
        "--output-dir",
        default="./data/sentinel",
        help="Directory to save downloaded files",
    )
    parser.add_argument(
        "--start-date", default="2025-01-01", help="Start date in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--end-date", default="2025-01-31", help="End date in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--cloud-threshold",
        type=int,
        default=10,
        help="Maximum cloud cover percentage (0-100)",
    )
    parser.add_argument(
        "--bands",
        default="red,green,blue,nir",
        help="Comma-separated list of bands to download",
    )

    args = parser.parse_args()

    main(
        aoi_path=args.aoi_path,
        output_dir=args.output_dir,
        time_range=(args.start_date, args.end_date),
        cloud_cover_threshold=args.cloud_threshold,
        bands=args.bands.split(","),
    )
