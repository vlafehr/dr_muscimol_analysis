import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as st
import os
from pathlib import Path
import dynamic_routing_analysis as dra
from allensdk.core.reference_space_cache import ReferenceSpaceCache
dra.ANALYSIS_ROOT_PATH = Path(".")  # or your desired root path
output_dir = dra.ANALYSIS_ROOT_PATH / "ccf_cache"

#define reference space information to generate volume
reference_space_key = "annotation/ccf_2022"
resolution = 10
rspc = ReferenceSpaceCache(resolution, reference_space_key, manifest=Path(output_dir) / 'manifest.json')
tree = rspc.get_structure_tree(structure_graph_id=1) 
# get id_acronym map
id_acronym_map = tree.get_id_acronym_map()
# make reference space object
rsp = rspc.get_reference_space()
# get annotation volume
annotation, meta = rspc.get_annotation_volume()

#define organization of CCF regions
parents=tree.parents([id_acronym_map['SNc']])[0]['structure_id_path']
broad_categories = [
    'Isocortex',
    'Hippocampal formation',
    'Cerebral nuclei',
    'Thalamus', 
    'Hypothalamus',
    'Midbrain', #sensory vs. motor vs. behavioral state?
    'Hindbrain',
    'Cerebellum'
]

broad_category_ids = []
for category in broad_categories:
    structures = tree.get_structures_by_name([category])
    if len(structures) > 0:
        broad_category_ids.append(structures[0]['id'])
    else:
        raise ValueError(f"Broad category '{category}' not found in structure tree.")
    
more_specific_categories = [
    'Thalamus, sensory-motor cortex related',
    'Thalamus, polymodal association cortex related',
    'Midbrain, motor related',
    'Midbrain, sensory related',
    'Midbrain, behavioral state related',
]

more_specific_category_ids = []
for category in more_specific_categories:
    structures = tree.get_structures_by_name([category])
    if len(structures) > 0:
        more_specific_category_ids.append(structures[0]['id'])
    else:
        raise ValueError(f"More specific category '{category}' not found in structure tree.")
    
def sort_structures_by_region(structure_acronym,broad_categories=None):
    "Sort CCF structures into broad categories based on their position in the structure tree."
    output_dir = dra.ANALYSIS_ROOT_PATH / "ccf_cache"
    reference_space_key = "annotation/ccf_2022"
    resolution = 10
    rspc = ReferenceSpaceCache(resolution, reference_space_key, manifest=Path(output_dir) / 'manifest.json')

    # get structure tree
    # ID 1 is the adult mouse structure graph
    tree = rspc.get_structure_tree(structure_graph_id=1) 

    # get id_acronym map
    id_acronym_map = tree.get_id_acronym_map()
    
    if broad_categories is None:
        broad_categories = [
            'Isocortex',
            'Hippocampal formation',
            'Cerebral nuclei',
            'Thalamus', 
            'Hypothalamus',
            'Midbrain',
            'Hindbrain',
            'Cerebellum'
        ]

    broad_category_ids = []
    for category in broad_categories:
        structures = tree.get_structures_by_name([category])
        if len(structures) > 0:
            broad_category_ids.append(structures[0]['id'])
        else:
            raise ValueError(f"Broad category '{category}' not found in structure tree.")

    parents=tree.parents([id_acronym_map[structure_acronym]])[0]['structure_id_path']

    for parent in parents:
        if parent in broad_category_ids:
            return tree.get_structures_by_id([parent])[0]['name']
        

def load_csv_annotations(folder_path):
    "Load all CSV files in path, process AP/DV/ML columns, and return a dict of DataFrames. CSV files are originally in 25um space so need to convert to 10um space."
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    annotations_csv = {}
    cols_of_interest = ['AP', 'DV', 'ML']
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        for col in cols_of_interest:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col] * 25
                df[col] = (df[col] // 10).astype('Int64')
        annotations_csv[csv_file] = df
    return annotations_csv


def get_structure_info_for_annotations(df, annotation, tree):
    """Get CCF structure info for each coordinate in a Polars dataframe."""
    results = []
    
    for row in df.iter_rows(named=True):
        try:
            # Ensure integer indices for annotation volume
            coord = (int(row['AP']), int(row['DV']), int(row['ML']))
            struct_id = annotation[coord]
            struct_info = tree.get_structures_by_id([struct_id])
            structure_name = struct_info[0]['name'] if struct_info else 'Unknown'
            results.append(structure_name)
            print(f"Coord: {coord} | Structure: {structure_name}")
        except Exception as e:
            results.append(None)
            print(f"Error at coord ({row.get('AP')}, {row.get('DV')}, {row.get('ML')}): {e}")
    
    return results
