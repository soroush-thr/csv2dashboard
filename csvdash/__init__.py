"""
CSV to Dashboard - Professional implementation
Turns CSV/Excel files into interactive web dashboards and static HTML reports.
"""

__version__ = "1.0.0"
__author__ = "CSV Dashboard Team"

from .data_loader import load_table, infer_types
from .filters import apply_filters
from .analysis import summaries_and_figs
from .export import export_html
from .ui import create_ui_components, update_dashboard, launch_ui
from .utils import validate_file_path, get_file_info, format_number, get_column_stats
from .config import (
    DEFAULT_HOST, DEFAULT_PORT, DEFAULT_TITLE, DEFAULT_TOP_K,
    MAX_PREVIEW_ROWS, LARGE_DATASET_THRESHOLD, CHART_HEIGHT,
    HISTOGRAM_BINS, SUPPORTED_EXTENSIONS, UI_THEME, SHOW_LEGEND
)

__all__ = [
    'load_table',
    'infer_types', 
    'apply_filters',
    'summaries_and_figs',
    'export_html',
    'create_ui_components',
    'update_dashboard',
    'launch_ui',
    'validate_file_path',
    'get_file_info',
    'format_number',
    'get_column_stats',
    'DEFAULT_HOST',
    'DEFAULT_PORT',
    'DEFAULT_TITLE',
    'DEFAULT_TOP_K',
    'MAX_PREVIEW_ROWS',
    'LARGE_DATASET_THRESHOLD',
    'CHART_HEIGHT',
    'HISTOGRAM_BINS',
    'SUPPORTED_EXTENSIONS',
    'UI_THEME',
    'SHOW_LEGEND'
]
