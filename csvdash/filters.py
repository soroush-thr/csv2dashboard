"""
Data filtering module.
Handles all types of data filtering including text search, numeric ranges, 
date ranges, and categorical selections.
"""

from typing import Dict, List, Tuple
import pandas as pd


def apply_filters(df: pd.DataFrame, types: Dict[str, str], 
                 text_query: str, num_ranges: Dict[str, Tuple[float, float]], 
                 date_ranges: Dict[str, Tuple[str, str]], 
                 cat_selections: Dict[str, List[str]]) -> pd.DataFrame:
    """Apply all filters to the dataframe."""
    filtered_df = df.copy()
    
    # Global text search
    if text_query and text_query.strip():
        text_cols = [col for col, t in types.items() if t in ['text', 'categorical']]
        if text_cols:
            mask = pd.Series([False] * len(filtered_df))
            for col in text_cols:
                mask |= filtered_df[col].astype(str).str.contains(text_query, case=False, na=False)
            filtered_df = filtered_df[mask]
    
    # Numeric range filters
    for col, (min_val, max_val) in num_ranges.items():
        if col in filtered_df.columns and types.get(col) == 'numeric':
            if min_val is not None and max_val is not None:
                filtered_df = filtered_df[
                    (filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)
                ]
    
    # Date range filters
    for col, (start_date, end_date) in date_ranges.items():
        if col in filtered_df.columns and types.get(col) == 'datetime':
            if start_date and end_date:
                try:
                    start_dt = pd.to_datetime(start_date)
                    end_dt = pd.to_datetime(end_date)
                    col_dt = pd.to_datetime(filtered_df[col])
                    filtered_df = filtered_df[
                        (col_dt >= start_dt) & (col_dt <= end_dt)
                    ]
                except:
                    pass
    
    # Categorical filters
    for col, selected_values in cat_selections.items():
        if col in filtered_df.columns and types.get(col) == 'categorical' and selected_values:
            if 'All' not in selected_values:
                filtered_df = filtered_df[filtered_df[col].isin(selected_values)]
    
    return filtered_df
