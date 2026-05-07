# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "aind-zarr-utils>=0.14",
# ]
# ///

# %%
import json
import numpy as np
import pandas as pd
from pathlib import Path

#%%
def convert_neuroglancer_points_to_ccf(folder_path: str | Path):
    "Convert all neuroglancer annotation JSON files in path to CCF points. Return a dict mapping file names to CCF points and descriptions of injection type."
    try:
        from aind_zarr_utils.pipeline_transformed import neuroglancer_to_ccf_auto_metadata
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "convert_neuroglancer_points_to_ccf requires 'aind_zarr_utils'. "
            "Install it in the active environment to use this function."
        ) from exc

    folder_path = Path(folder_path)
    ccf_pts = {}
    for json_path in folder_path.glob("*.json"):
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
            pts, description = neuroglancer_to_ccf_auto_metadata(
                data,
                    return_description=True,
                )
        
                # Keep points and description together
            ccf_pts[json_path.stem] = {
                    "points": pts,
                    "description": description,
                }
    return ccf_pts
        
        
def clean_neurogrlancer_ccf_pts(ccf_pts):
    "Clean CCF points by reordering to match CCF convention by changing numeric position and sign (took absolute value of ng coords). Return a DataFrame with mouse_id, region targeted_date, injection type, and CCF coords."
    rows = []
    for mouse_id, payload in ccf_pts.items():
                # Supports new format ({points, description}) and old format ({label: arr})
        if isinstance(payload, dict) and "points" in payload:
            labels = payload["points"]
            desc_payload = payload.get("description")
        else:
            labels = payload
            desc_payload = None
        
        for label, arr in labels.items():
            arr = np.asarray(arr, dtype=float).reshape(-1, 3)
            for x, y, z in arr:
                ap, dv, ml = abs(100 * y), abs(100 * z), abs(100 * x)
        
                if isinstance(desc_payload, dict):
                        description = desc_payload.get(label)
                else:
                    description = desc_payload
        
            rows.append({
                    "mouse_id": str(mouse_id),
                    "label": label,
                    "description": description,
                    "AP": ap,
                    "DV": dv,
                    "ML": ml,
                    })
        
    return pd.DataFrame(rows, columns=["mouse_id", "label", "description", "AP", "DV", "ML"])
        
    



