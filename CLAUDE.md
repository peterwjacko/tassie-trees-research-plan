# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PhD research plan for studying ancient Tasmanian tree species using remote sensing and geospatial analysis. The repo combines a published research document (MyST/Jupyter Book), analysis notebooks, and a reveal.js presentation, all managed with Pixi.

Published at: https://peterwjacko.github.io/tassie-trees-research-plan/

## Environment Setup

```bash
pixi install          # preferred (uses pixi.lock for reproducibility)
# or
mamba create -n ttrp-env -f environment.yaml
```

## Key Commands

### Research Document (MyST)
```bash
myst build --html     # build the research document to HTML
myst start            # local dev server with live reload
```

### Presentation (Hugo + reveal.js)
```bash
cd presentation
hugo server           # local dev server
hugo                  # build to presentation/public/
```

The presentation uses the `reveal-hugo` theme (git submodule at `presentation/themes/reveal-hugo`).

### Notebooks
```bash
pixi run jupyter lab  # launch JupyterLab
```

## Architecture

**Three distinct output targets:**

1. **`document/`** — MyST Markdown research document. Configured via `myst.yml` at repo root. References `document/references.bib` for citations (APA style via `apa.csl`). Builds to `_build/site/`.

2. **`notebooks/`** — Jupyter notebooks for geospatial analysis and figures. Key notebooks:
   - `ala_occurances.ipynb` — fetches species occurrence data from ALA via `galah-python`
   - `burn_scar.ipynb` — burn scar mapping using DEA Sentinel-2 ARD imagery from AWS S3

3. **`presentation/`** — Hugo site using reveal-hugo theme for reveal.js slides. Separate from the MyST document.

**Data pipeline:** `notebooks/` → processed outputs → `data/vector/*.geojson` → referenced in `document/` as figures.

**Geospatial data** in `data/vector/` (GeoJSON format):
- `ala_occurences.geojson` — ALA biodiversity occurrence points
- `study_areas.geojson` — field study site polygons
- `CAPAD_TAS.geojson` — Tasmanian protected areas

Raster data (`.tif`) is gitignored. Satellite imagery accessed live from DEA (Digital Earth Australia) via AWS S3 using `boto3` and `pystac-client`.

## CI/CD

GitHub Actions (`.github/workflows/deploy.yml`) builds the MyST document and deploys to GitHub Pages on push to `main`. It uses `npm install -g mystmd` then `myst build --html`.
