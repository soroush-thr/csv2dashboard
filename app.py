#!/usr/bin/env python3
"""
CSV to Dashboard - Minimal implementation
Turns CSV/Excel files into interactive web dashboards and static HTML reports.
"""

import argparse
import os
import io
import datetime as dt
import warnings
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import gradio as gr

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


def summaries_and_figs(df: pd.DataFrame, types: Dict[str, str], topk: int = 20) -> Dict[str, Any]:
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
                fig = px.histogram(series, title=f"Distribution of {col}", nbins=30)
                fig.update_layout(height=300, showlegend=False)
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
                fig.update_layout(height=300, showlegend=False, 
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
                        fig.update_layout(height=300, showlegend=False)
                        results['figs']['datetime'][col] = fig
            except:
                pass
        
        if dt_data:
            results['datetime_summary'] = pd.DataFrame(dt_data)
    
    return results


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


def create_ui_components(df: pd.DataFrame, types: Dict[str, str]) -> Tuple[List, Dict]:
    """Create Gradio UI components for filters."""
    components = []
    state = {}
    
    # Global text search
    text_search = gr.Textbox(label="Global Text Search", placeholder="Search across all text columns...")
    components.append(text_search)
    state['text_search'] = text_search
    
    # Numeric filters
    numeric_cols = [col for col, t in types.items() if t == 'numeric']
    if numeric_cols:
        with gr.Group():
            gr.Markdown("### Numeric Filters")
            for col in numeric_cols:
                series = df[col].dropna()
                if len(series) > 0:
                    min_val, max_val = float(series.min()), float(series.max())
                    slider = gr.Slider(
                        minimum=min_val, maximum=max_val, 
                        value=(min_val, max_val),
                        label=f"{col} Range",
                        step=(max_val - min_val) / 100
                    )
                    components.append(slider)
                    state[f'num_{col}'] = slider
    
    # Datetime filters
    datetime_cols = [col for col, t in types.items() if t == 'datetime']
    if datetime_cols:
        with gr.Group():
            gr.Markdown("### Date Filters")
            for col in datetime_cols:
                try:
                    dt_series = pd.to_datetime(df[col]).dropna()
                    if len(dt_series) > 0:
                        min_date = dt_series.min().date()
                        max_date = dt_series.max().date()
                        date_range = gr.Textbox(
                            label=f"{col} Date Range",
                            placeholder=f"YYYY-MM-DD to YYYY-MM-DD",
                            value=f"{min_date} to {max_date}"
                        )
                        components.append(date_range)
                        state[f'date_{col}'] = date_range
                except:
                    pass
    
    # Categorical filters
    cat_cols = [col for col, t in types.items() if t == 'categorical']
    if cat_cols:
        with gr.Group():
            gr.Markdown("### Categorical Filters")
            for col in cat_cols:
                unique_values = df[col].dropna().unique()
                if len(unique_values) <= 20:
                    choices = ['All'] + sorted(unique_values.tolist())
                else:
                    top_values = df[col].value_counts().head(20).index.tolist()
                    choices = ['All'] + top_values
                
                multiselect = gr.Dropdown(
                    choices=choices,
                    value=['All'],
                    multiselect=True,
                    label=f"{col} (Top 20 values)"
                )
                components.append(multiselect)
                state[f'cat_{col}'] = multiselect
    
    return components, state


def update_dashboard(text_query, *filter_values, df=pd.DataFrame(), types={}):
    """Update dashboard based on current filters."""
    if df.empty:
        return "No data loaded", {}, {}, "", ""
    
    # Parse filter values
    numeric_cols = [col for col, t in types.items() if t == 'numeric']
    datetime_cols = [col for col, t in types.items() if t == 'datetime']
    cat_cols = [col for col, t in types.items() if t == 'categorical']
    
    num_ranges = {}
    date_ranges = {}
    cat_selections = {}
    
    idx = 0
    for col in numeric_cols:
        if f'num_{col}' in filter_values:
            num_ranges[col] = filter_values[idx]
            idx += 1
    
    for col in datetime_cols:
        if f'date_{col}' in filter_values:
            date_str = filter_values[idx]
            if ' to ' in date_str:
                start, end = date_str.split(' to ')
                date_ranges[col] = (start.strip(), end.strip())
            idx += 1
    
    for col in cat_cols:
        if f'cat_{col}' in filter_values:
            cat_selections[col] = filter_values[idx]
            idx += 1
    
    # Apply filters
    filtered_df = apply_filters(df, types, text_query, num_ranges, date_ranges, cat_selections)
    
    # Generate summaries and figures
    summaries = summaries_and_figs(filtered_df, types)
    
    # Create info text
    info_text = f"""
    **Dataset Info:**
    - Rows: {len(filtered_df):,} (filtered from {len(df):,})
    - Columns: {len(filtered_df.columns)}
    - Numeric columns: {len([c for c, t in types.items() if t == 'numeric'])}
    - Categorical columns: {len([c for c, t in types.items() if t == 'categorical'])}
    - Datetime columns: {len([c for c, t in types.items() if t == 'datetime'])}
    """
    
    # Create CSV download
    csv_buffer = io.StringIO()
    filtered_df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    return (
        info_text,
        summaries['figs']['numeric'],
        summaries['figs']['categorical'], 
        summaries['figs']['datetime'],
        csv_data
    )


def launch_ui(df: pd.DataFrame, title: str, host: str = "127.0.0.1", port: int = 7860):
    """Launch Gradio UI."""
    
    # Check for large datasets
    if len(df) > 500000:
        print(f"Warning: Large dataset ({len(df):,} rows). Consider using column selection for better performance.")
    
    types = infer_types(df)
    
    with gr.Blocks(title=title) as demo:
        gr.Markdown(f"# {title}")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## Filters")
                components, state = create_ui_components(df, types)
                
                export_btn = gr.Button("Export Current View to HTML", variant="secondary")
            
            with gr.Column(scale=3):
                info_display = gr.Markdown()
                
                # Charts will be displayed here
                with gr.Tabs():
                    with gr.Tab("Numeric Charts"):
                        numeric_charts = gr.Plot()
                    with gr.Tabs("Categorical Charts"):
                        categorical_charts = gr.Plot()
                    with gr.Tabs("Datetime Charts"):
                        datetime_charts = gr.Plot()
                
                # Data preview
                with gr.Row():
                    data_preview = gr.Dataframe(
                        value=df.head(200),
                        max_height=400,
                        wrap=True
                    )
                    download_btn = gr.DownloadButton("Download Filtered CSV", variant="primary")
        
        # Event handlers
        def update_all(*args):
            return update_dashboard(*args, df=df, types=types)
        
        # Connect all filter components
        all_components = [state['text_search']] + [comp for comp in components if comp != state['text_search']]
        
        for component in all_components:
            if hasattr(component, 'change'):
                component.change(update_all, all_components, 
                               [info_display, numeric_charts, categorical_charts, datetime_charts, download_btn])
        
        # Export functionality
        def export_current_view():
            # Get current filter state
            filter_state = {
                'text_query': state['text_search'].value if hasattr(state['text_search'], 'value') else '',
                'num_ranges': {},
                'date_ranges': {},
                'cat_selections': {}
            }
            
            # This is a simplified export - in a real implementation, you'd capture current filter values
            export_html("current_view.html", title, df, types, filter_state, {})
            return "Exported to current_view.html"
        
        export_btn.click(export_current_view, outputs=gr.Textbox())
    
    demo.launch(server_name=host, server_port=port, share=False)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Convert CSV/Excel to interactive dashboard")
    parser.add_argument("file", help="Path to CSV or Excel file")
    parser.add_argument("--sheet", help="Excel sheet name or number (default: first sheet)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=7860, help="Port to bind to (default: 7860)")
    parser.add_argument("--export", help="Export static HTML report and exit")
    parser.add_argument("--title", default="CSV Dashboard", help="Dashboard title")
    
    args = parser.parse_args()
    
    try:
        # Load data
        print(f"Loading {args.file}...")
        df = load_table(args.file, args.sheet)
        print(f"Loaded {len(df):,} rows × {len(df.columns)} columns")
        
        if args.export:
            # Export mode
            print("Generating HTML report...")
            types = infer_types(df)
            filter_state = {}  # No filters for export
            summaries = summaries_and_figs(df, types)
            export_html(args.export, args.title, df, types, filter_state, summaries)
            print(f"Report exported to: {args.export}")
        else:
            # Launch UI
            print(f"Launching dashboard at http://{args.host}:{args.port}")
            launch_ui(df, args.title, args.host, args.port)
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
