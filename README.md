# Tasmanian Trees Research Plan

Research plan and supporting tools for studying Tasmanian forests using satellite imagery.

## Features

- Download cloud-free Sentinel imagery from Digital Earth Australia
- Process and analyze satellite data for forest research
- Support for temporal analysis of tree cover changes

## Installation

This project uses [pixi](https://github.com/prefix-dev/pixi) for environment management.

```bash
# Clone the repository
git clone https://github.com/yourusername/tassie-trees-research-plan.git
cd tassie-trees-research-plan

# Install with pixi
pixi install
```

Alternatively, you can install with pip:

```bash
pip install -e .
```

## Usage

### Downloading Sentinel Imagery

The project includes a module for downloading cloud-free Sentinel-2 imagery from the Digital Earth Australia STAC API.

```python
from tassie_trees_research_plan.satellite_data import main as satellite_main

# Define parameters
aoi_path = "path/to/your/area_of_interest.geojson"
time_range = ("2025-01-01", "2025-01-31")
cloud_cover_threshold = 5  # 5% cloud cover maximum

# Download imagery and create RGB composites
composites = satellite_main(
    aoi_path=aoi_path,
    time_range=time_range,
    cloud_cover_threshold=cloud_cover_threshold,
    bands=["red", "green", "blue", "nir"]
)
```

See the [Satellite Data README](src/tassie_trees_research_plan/README_satellite_data.md) for more details.

## Documentation

- [Project Timeline](project-timeline.md)
- [Research Plan Draft](research-plan-draft.md)
- [Satellite Data Processing](src/tassie_trees_research_plan/README_satellite_data.md)

## License

[MIT](LICENSE)