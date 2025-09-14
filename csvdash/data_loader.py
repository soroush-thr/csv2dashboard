"""
Data loading and type inference module.
Handles CSV/Excel file loading and automatic column type detection.
"""

import os
import warnings
from typing import Dict
import pandas as pd

# Suppress pandas warnings
warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)
warnings.filterwarnings('ignore', message='Could not infer format')
warnings.filterwarnings('ignore', message='falling back to `dateutil`')


def load_table(path: str, sheet=None) -> pd.DataFrame:
    """Load CSV or Excel file with robust parsing."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    # Handle gzipped CSV
    if path.endswith('.csv.gz'):
        import gzip
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            df = pd.read_csv(f)
    elif path.endswith('.csv'):
        # Auto-detect delimiter
        with open(path, 'r', encoding='utf-8') as f:
            sample = f.read(1024)
            f.seek(0)
            from csv import Sniffer
            sniffer = Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            df = pd.read_csv(f, delimiter=delimiter)
    elif path.endswith(('.xlsx', '.xls')):
        if sheet is None:
            df = pd.read_excel(path)
        else:
            df = pd.read_excel(path, sheet_name=sheet)
    else:
        raise ValueError(f"Unsupported file format: {path}")
    
    return df


def infer_types(df: pd.DataFrame) -> Dict[str, str]:
    """Infer column types for filtering and visualization."""
    types = {}
    
    for col in df.columns:
        # Check for datetime
        if df[col].dtype == 'object':
            # Try to parse as datetime
            try:
                pd.to_datetime(df[col].dropna().head(100), errors='raise')
                types[col] = 'datetime'
                continue
            except:
                pass
        
        # Check for boolean
        if df[col].dtype == 'bool' or df[col].dtype.name == 'bool':
            types[col] = 'boolean'
        # Check for numeric
        elif pd.api.types.is_numeric_dtype(df[col]):
            types[col] = 'numeric'
        # Check for categorical (low cardinality)
        elif df[col].dtype == 'object':
            unique_count = df[col].nunique()
            if unique_count <= 50 and unique_count < len(df) * 0.5:
                types[col] = 'categorical'
            else:
                types[col] = 'text'
        else:
            types[col] = 'text'
    
    return types
