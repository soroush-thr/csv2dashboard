"""
HTML export module.
Handles generation of static HTML reports from filtered data.
"""

import datetime as dt
from typing import Dict, Any
import pandas as pd
import plotly.io as pio

from .analysis import summaries_and_figs


def export_html(out_path: str, title: str, df_filtered: pd.DataFrame, 
                types: Dict[str, str], filter_state: Dict[str, Any], 
                summaries: Dict[str, Any]) -> None:
    """Export current view to standalone HTML report."""
    
    # Generate summaries and figures for filtered data
    filtered_summaries = summaries_and_figs(df_filtered, types)
    
    html_parts = [
        f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
        .section {{ margin: 20px 0; }}
        .stats-table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        .stats-table th, .stats-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .stats-table th {{ background-color: #f2f2f2; }}
        .chart {{ margin: 20px 0; }}
        .filter-summary {{ background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>Generated on {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Dataset: {len(df_filtered):,} rows × {len(df_filtered.columns)} columns</p>
    </div>
"""
    ]
    
    # Filter summary
    if any(filter_state.values()):
        html_parts.append('<div class="filter-summary"><h3>Applied Filters</h3><ul>')
        if filter_state.get('text_query'):
            html_parts.append(f'<li>Text search: "{filter_state["text_query"]}"</li>')
        for col, (min_val, max_val) in filter_state.get('num_ranges', {}).items():
            if min_val is not None and max_val is not None:
                html_parts.append(f'<li>{col}: {min_val} to {max_val}</li>')
        for col, values in filter_state.get('cat_selections', {}).items():
            if values and 'All' not in values:
                html_parts.append(f'<li>{col}: {", ".join(values)}</li>')
        html_parts.append('</ul></div>')
    
    # Numeric summaries
    if not filtered_summaries['numeric_summaries'].empty:
        html_parts.append('<div class="section"><h2>Numeric Columns Summary</h2>')
        html_parts.append(filtered_summaries['numeric_summaries'].to_html(
            classes='stats-table', index=False, escape=False, float_format='%.2f'
        ))
        html_parts.append('</div>')
        
        # Numeric charts
        for col, fig in filtered_summaries['figs']['numeric'].items():
            html_parts.append(f'<div class="chart">{pio.to_html(fig, include_plotlyjs="inline", div_id=f"numeric_{col}")}</div>')
    
    # Categorical summaries
    if not filtered_summaries['categorical_summaries'].empty:
        html_parts.append('<div class="section"><h2>Categorical Columns Summary</h2>')
        html_parts.append(filtered_summaries['categorical_summaries'].to_html(
            classes='stats-table', index=False, escape=False
        ))
        html_parts.append('</div>')
        
        # Categorical charts
        for col, fig in filtered_summaries['figs']['categorical'].items():
            html_parts.append(f'<div class="chart">{pio.to_html(fig, include_plotlyjs="inline", div_id=f"cat_{col}")}</div>')
    
    # Datetime summaries
    if not filtered_summaries['datetime_summary'].empty:
        html_parts.append('<div class="section"><h2>Datetime Columns Summary</h2>')
        html_parts.append(filtered_summaries['datetime_summary'].to_html(
            classes='stats-table', index=False, escape=False
        ))
        html_parts.append('</div>')
        
        # Datetime charts
        for col, fig in filtered_summaries['figs']['datetime'].items():
            html_parts.append(f'<div class="chart">{pio.to_html(fig, include_plotlyjs="inline", div_id=f"dt_{col}")}</div>')
    
    html_parts.append('</body></html>')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))
