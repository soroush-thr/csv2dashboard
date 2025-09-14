"""
Command-line interface for CSV to Dashboard.
"""

import argparse
from .data_loader import load_table, infer_types
from .ui import launch_ui
from .export import export_html, summaries_and_figs
from .config import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_TITLE


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Convert CSV/Excel to interactive dashboard")
    parser.add_argument("file", help="Path to CSV or Excel file")
    parser.add_argument("--sheet", help="Excel sheet name or number (default: first sheet)")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host to bind to (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to bind to (default: {DEFAULT_PORT})")
    parser.add_argument("--export", help="Export static HTML report and exit")
    parser.add_argument("--title", default=DEFAULT_TITLE, help=f"Dashboard title (default: {DEFAULT_TITLE})")
    
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
