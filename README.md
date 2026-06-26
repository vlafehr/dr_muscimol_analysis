# Dynamic Routing Muscimol Analysis

Analysis of muscimol inactivation experiments for the Dynamic Routing project. This repository contains Jupyter notebooks and utils files for analyzing behavioral effects of pharmacological inactivation in across mouse brain.

## Overview

This project investigates how targeted muscimol injections to specific brain regions (e.g., ORBmvl, CP) affect behavioral performance in a dynamic routing task. The analysis pipeline includes:

- Behavioral metrics extraction from experimental sessions
- Injection site coordinate mapping to the Allen Common Coordinate Framework (CCF)
- Statistical comparisons between control and perturbation conditions
- Visualization of results for poster presentations

## Installation

This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

```bash
# Navigate to project directory
cd path/to/dr_muscimol_analysis

# Install dependencies
uv sync
```

### Dependencies

Core dependencies include:
- `ipykernel` - Jupyter notebook support
- `npc_lims` / `npc_sessions` - Session data access (install separately)
- `dynamic_routing_analysis` - Analysis utilities (install separately)
- `allensdk` - Allen Institute SDK for CCF utilities
- `aind-zarr-utils` - For neuroglancer coordinate conversion

## Project Structure

```
dr_muscimol_analysis/
├── pyproject.toml                          # Project configuration
├── README.md
└── notebooks/
    ├── muscimol_analysis_notebook.ipynb    # Main muscimol analysis pipeline
    ├── muscimol_controls_analysis.ipynb    # Control condition analysis
    ├── ORBm_versus_AId_analysis.ipynb      # Regional comparison analysis
    ├── adaptations_analysis.ipynb          # Behavioral adaptation analysis
    ├── adaptations_analysis_part_2.ipynb   # Extended adaptation analysis
    ├── ccf_injection_coords_behavior_metric_correlations.ipynb  # Coordinate-behavior correlations
    ├── poster_session_muscimol_figures.ipynb  # Figure generation for presentations
    ├── neuroglancer_injections_coords_utils.py  # Neuroglancer → CCF conversion
    └── tissuecyte_injections_coords_utils.py    # TissueCyte → CCF mapping utilities
```

## Notebooks

| Notebook | Description |
|----------|-------------|
| `muscimol_analysis_notebook.ipynb` | Primary analysis of muscimol injection effects on behavior |
| `muscimol_controls_analysis.ipynb` | Analysis of control (saline) sessions |
| `ORBm_versus_AId_analysis.ipynb` | Comparison between ORB subregions: ORBm vs AId inactivation effects |
| `adaptations_analysis.ipynb` | Analysis of behavioral adaptations over consecutive muscimol injection sessions |
| `ccf_injection_coords_behavior_metric_correlations.ipynb` | Correlating injection coordinates with behavioral outcomes |
| `poster_session_muscimol_figures.ipynb` | Generate SfN ready figures |

## Utils 

### `tissuecyte_injections_coords_utils.py`
Functions for mapping injection coordinates to the Allen CCF using TissueCyte data:
- `sort_structures_by_region()` - Categorize CCF structures into broad brain regions

### `neuroglancer_injections_coords_utils.py`
Functions for converting neuroglancer annotation files to CCF coordinates:
- `convert_neuroglancer_points_to_ccf()` - Batch convert annotation JSONs
- `clean_neurogrlancer_ccf_pts()` - Clean and reformat coordinate data

## How to use

1. Open notebooks in VS Code or Jupyter
2. Ensure you have access to the session data via `npc_lims`
3. Run cells sequentially to reproduce analyses

```python
# Example: Load a session
import npc_sessions
session = npc_sessions.Session('ecephys_XXXXXX_YYYY-MM-DD_HH-MM-SS')
```

## Brain Regions

The analysis focuses on the following CCF regions:
 - Isocortex, Thalamus, Midbrain, etc.

