#!/usr/bin/env python3
"""
Entry point for running the satellite data download functionality from the command line.
"""

from tassie_trees_research_plan.satellite_data import main

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
