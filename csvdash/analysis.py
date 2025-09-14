"""
Data analysis and visualization module.
Handles statistical summaries and chart generation for different data types.
"""

from typing import Dict, Any
import pandas as pd
import plotly.express as px
from .config import DEFAULT_TOP_K, CHART_HEIGHT, HISTOGRAM_BINS, SHOW_LEGEND


def summaries_and_figs(df: pd.DataFrame, types: Dict[str, str], topk: int = DEFAULT_TOP_K) -> Dict[str, Any]:
    """Generate summaries and figures for the dataset."""
    results = {
        'numeric_summaries': pd.DataFrame(),
        'categorical_summaries': pd.DataFrame(),
        'datetime_summary': pd.DataFrame(),
        'figs': {'numeric': {}, 'categorical': {}, 'datetime': {}}
    }
    
    # Numeric summaries and histograms
    numeric_cols = [col for col, t in types.items() if t == 'numeric']
    if numeric_cols:
        numeric_data = []
        for col in numeric_cols:
            series = df[col].dropna()
            if len(series) > 0:
                stats = {
                    'Column': col,
                    'Count': len(series),
                    'Mean': series.mean(),
                    'Std': series.std(),
                    'Min': series.min(),
                    'Median': series.median(),
                    'P95': series.quantile(0.95),
                    'Max': series.max(),
                    'Missing%': (df[col].isna().sum() / len(df)) * 100
                }
                numeric_data.append(stats)
                
                # Create histogram
                fig = px.histogram(series, title=f"Distribution of {col}", nbins=HISTOGRAM_BINS)
                fig.update_layout(height=CHART_HEIGHT, showlegend=SHOW_LEGEND)
                results['figs']['numeric'][col] = fig
        
        if numeric_data:
            results['numeric_summaries'] = pd.DataFrame(numeric_data)
    
    # Categorical summaries and bar charts
    cat_cols = [col for col, t in types.items() if t == 'categorical']
    if cat_cols:
        cat_data = []
        for col in cat_cols:
            value_counts = df[col].value_counts()
            top_values = value_counts.head(topk)
            others_count = value_counts.iloc[topk:].sum() if len(value_counts) > topk else 0
            
            stats = {
                'Column': col,
                'Unique_Count': df[col].nunique(),
                'Most_Common': value_counts.index[0] if len(value_counts) > 0 else None,
                'Most_Common_Count': value_counts.iloc[0] if len(value_counts) > 0 else 0,
                'Others_Count': others_count,
                'Missing%': (df[col].isna().sum() / len(df)) * 100
            }
            cat_data.append(stats)
            
            # Create bar chart
            if len(top_values) > 0:
                fig_data = top_values.copy()
                if others_count > 0:
                    fig_data['Others'] = others_count
                
                fig = px.bar(x=fig_data.index, y=fig_data.values, 
                           title=f"Top values in {col}")
                fig.update_layout(height=CHART_HEIGHT, showlegend=SHOW_LEGEND, 
                                xaxis_tickangle=45)
                results['figs']['categorical'][col] = fig
        
        if cat_data:
            results['categorical_summaries'] = pd.DataFrame(cat_data)
    
    # Datetime summaries and line charts
    datetime_cols = [col for col, t in types.items() if t == 'datetime']
    if datetime_cols:
        dt_data = []
        for col in datetime_cols:
            try:
                dt_series = pd.to_datetime(df[col]).dropna()
                if len(dt_series) > 0:
                    # Resample to daily
                    daily_counts = dt_series.dt.date.value_counts().sort_index()
                    
                    stats = {
                        'Column': col,
                        'Date_Range': f"{dt_series.min().date()} to {dt_series.max().date()}",
                        'Total_Records': len(dt_series),
                        'Missing%': (df[col].isna().sum() / len(df)) * 100
                    }
                    dt_data.append(stats)
                    
                    # Create line chart
                    if len(daily_counts) > 0:
                        fig = px.line(x=daily_counts.index, y=daily_counts.values,
                                    title=f"Records over time - {col}")
                        fig.update_layout(height=CHART_HEIGHT, showlegend=SHOW_LEGEND)
                        results['figs']['datetime'][col] = fig
            except:
                pass
        
        if dt_data:
            results['datetime_summary'] = pd.DataFrame(dt_data)
    
    return results
