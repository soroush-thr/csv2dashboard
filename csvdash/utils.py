"""
Utility functions for CSV to Dashboard.
"""

import os
from typing import List, Tuple
import pandas as pd


def validate_file_path(file_path: str) -> bool:
    """Validate that the file exists and has a supported extension."""
    if not os.path.exists(file_path):
        return False
    
    _, ext = os.path.splitext(file_path.lower())
    supported_extensions = ['.csv', '.csv.gz', '.xlsx', '.xls']
    return ext in supported_extensions


def get_file_info(file_path: str) -> dict:
    """Get basic information about a file."""
    if not os.path.exists(file_path):
        return {}
    
    stat = os.stat(file_path)
    return {
        'size_bytes': stat.st_size,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'modified': stat.st_mtime
    }


def format_number(num: float, precision: int = 2) -> str:
    """Format a number with appropriate precision."""
    if num >= 1e6:
        return f"{num/1e6:.{precision}f}M"
    elif num >= 1e3:
        return f"{num/1e3:.{precision}f}K"
    else:
        return f"{num:.{precision}f}"


def get_column_stats(df: pd.DataFrame, column: str) -> dict:
    """Get basic statistics for a specific column."""
    if column not in df.columns:
        return {}
    
    series = df[column].dropna()
    if len(series) == 0:
        return {'count': 0, 'missing': len(df)}
    
    stats = {
        'count': len(series),
        'missing': len(df) - len(series),
        'missing_pct': round((len(df) - len(series)) / len(df) * 100, 2)
    }
    
    if pd.api.types.is_numeric_dtype(series):
        stats.update({
            'mean': series.mean(),
            'std': series.std(),
            'min': series.min(),
            'max': series.max(),
            'median': series.median()
        })
    elif series.dtype == 'object':
        stats.update({
            'unique': series.nunique(),
            'most_common': series.value_counts().index[0] if len(series) > 0 else None,
            'most_common_count': series.value_counts().iloc[0] if len(series) > 0 else 0
        })
    
    return stats
