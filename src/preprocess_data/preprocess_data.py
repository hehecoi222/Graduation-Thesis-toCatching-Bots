import pandas as pd
import numpy as np
import math
import os
from p2p_clustering.file_handling import SRC_LABEL, DST_LABEL, PROTO_LABEL, BPP_IN_LABEL, BPP_OUT_LABEL, G_BPP_IN_LABEL, G_BPP_OUT_LABEL

def group_nearby_integers(series: pd.Series, threshold_percent: float = 20.0) -> pd.Series:
    # Skip if the series is empty
    if series.empty:
        return series.copy()

    # Sort the unique values in the series
    unique_vals = sorted(series.unique())
    if not unique_vals:
        return series.copy()

    threshold_factor = threshold_percent / 100.0
    groups = []
    current_group = []
    mapping = {}

    for val in unique_vals:
        # First init new group
        if not current_group:
            current_group.append(val)
            continue

        # Calculate if adding current value
        potential_group = current_group + [val]
        potential_median = np.median(potential_group) 

        lower_bound = potential_median * (1 - threshold_factor)
        upper_bound = potential_median * (1 + threshold_factor)

        # Check if all in bounds after adding
        all_within_bounds = True
        for item in potential_group:
            if not (lower_bound <= item <= upper_bound):
                all_within_bounds = False
                break

        if all_within_bounds:
            current_group.append(val)
        else:
            # Finalize the current group
            final_median = np.median(current_group)
            # Get the representative value
            representative = int(math.ceil(final_median)) 
            
            groups.append({'group': current_group, 'representative': representative})
            for member in current_group:
                mapping[member] = representative
            # Start a new group with the current value
            current_group = [val]
    # Finalize the last group
    if current_group:
        final_median = np.median(current_group)
        representative = int(math.ceil(final_median)) # Using ceil like before
        
        groups.append({'group': current_group, 'representative': representative})
        for member in current_group:
            mapping[member] = representative

    return series.map(mapping)

def read_df_write_new(file_path: str, threshold_percent: float = 20.0) -> None:
    """read_df_write_new
    Require file_path to match format header: SrcBytes, SrcPkts, TotBytes, TotPkts

    Args:
        file_path (str): file to read and outfile is new_file_path
        threshold_percent (float, optional): amount to group. Defaults to 20.0.
    """
    df = pd.read_csv(file_path)
    df[BPP_OUT_LABEL] = (df['SrcBytes'] / df['SrcPkts']).fillna(0).astype(int)
    df[BPP_IN_LABEL] = ((df['TotBytes'] - df['SrcBytes']) / (df['TotPkts'] - df['SrcPkts'])).fillna(0).astype(int)
    df[G_BPP_OUT_LABEL] = group_nearby_integers(df[BPP_OUT_LABEL], threshold_percent=threshold_percent)
    df[G_BPP_IN_LABEL] = group_nearby_integers(df[BPP_IN_LABEL], threshold_percent=threshold_percent)
    if not os.path.exists('out_file'):
        os.makedirs('out_file')
    df.to_csv('out_file/new_infile.csv', index=False)
    