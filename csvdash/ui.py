"""
User interface module.
Handles Gradio UI components and dashboard functionality.
"""

import io
from typing import Dict, List, Tuple, Any
import pandas as pd
import gradio as gr

from .filters import apply_filters
from .analysis import summaries_and_figs
from .config import MAX_PREVIEW_ROWS, LARGE_DATASET_THRESHOLD


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
    if len(df) > LARGE_DATASET_THRESHOLD:
        print(f"Warning: Large dataset ({len(df):,} rows). Consider using column selection for better performance.")
    
    from .data_loader import infer_types
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
                        value=df.head(MAX_PREVIEW_ROWS),
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
            from .export import export_html
            export_html("current_view.html", title, df, types, filter_state, {})
            return "Exported to current_view.html"
        
        export_btn.click(export_current_view, outputs=gr.Textbox())
    
    demo.launch(server_name=host, server_port=port, share=False)
