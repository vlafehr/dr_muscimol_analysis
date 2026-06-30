## Dynamic Routing Muscimol Analysis

Analysis of muscimol inactivation experiments for the Dynamic Routing project. This repository contains Jupyter notebooks and utils files for analyzing behavioral effects of pharmacological inactivation across the mouse brain. Run noteboooks using envrionment requirements specified below. With the notebooks included in this project, you can:

- analyze different elements of behavior in control versus perturbation sessions
- map injection site coordinates to the Allen Common Coordinate Framework (CCF)
- look at electrophysiological effects of muscimol in the brain
- and more...(Look under 'Notebooks' description below for a description of what each notebook does)


## Navigate to project directory
cd path/to/dr_muscimol_analysis

### Dependencies

This project requires two separate environments due to package conflicts. The `allensdk` package conflicts with `dynamic_routing_analysis` and cannot be installed in the same environment. Create a separate environment when working with TissueCyte coordinate utilities. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

### Install environments with specific dependencies
Toggle between two different envs using uv optional functionality when running notebooks and utils for this project.

use dr (dynamic routing) for every notebook and neuroglancer_injections_coords_utils.py EXCEPT for `tissuecyte_injections_coords_utils.py`:
uv sync --extra dr

use sdk (allensdk) for `tissuecyte_injections_coords_utils.py` ONLY:
uv sync --extra sdk

sdk and dr are mutually exclusive. syncing one disengages the dependencies of the other and vice versa.


## Notebooks

| Notebook | Description |
|----------|-------------|
| `muscimol_analysis_notebook.ipynb` | includes ephys analysis of muscimol effects |
| `muscimol_controls_analysis.ipynb` | compares behavior in control sessions with and without saline injections to muscimol sessions |
| `ORBm_versus_AId_analysis.ipynb` | restricts behaviroal analysis to subregions in orbitofrontal cortex |
| `adaptations_analysis.ipynb` | looks at behavioral adaptations to consecutive muscimol injection sessions |
| `adaptations_analysis_part_2.ipynb` | looks at electrophysiological adaptations to consecutive muscimol injection sessions
| `ccf_injection_coords_behavior_metric_correlations.ipynb` | looks at ccf-aligned muscimol injections and attempts to correlate structure-specific inactivation to behavioral outcomes |
| `poster_session_muscimol_figures.ipynb` | generates SfN ready figures for switching dynamics and response rates in control vs muscimol sessions |

## Utils 

Both utils files pull coordinate files from this folder: Z:\Vayle\Muscimol\injections_ccf_coordinates

### `tissuecyte_injections_coords_utils.py`
**Requires sdk environment (includes allensdk, deactivates dependencies in dr env)** (conflicts with dr environment)

Contains functions that convert TissueCyte injection coordinate data in .csv format to CCF data.


### `neuroglancer_injections_coords_utils.py`
**Requires dr environment (includes aind_zarr_utils, deactivates dependencies in sdk env)**

Contains functions that convert neuroglancer annotation files in .json format to CCF coordinates.


## How to use
-need credentials for aws and codeoecean

-if you are having trouble pulling sessions from npc.sessions, check quilt (https://open.quiltdata.com/b/aind-scratch-data/tree/dynamic-routing/DynamicRoutingTask/Data/). sometimes need to update quilt. ask ben hardcastle to run script for update.


