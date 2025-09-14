"""
Configuration settings for CSV to Dashboard.
"""

# Default settings
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 7860
DEFAULT_TITLE = "CSV Dashboard"
DEFAULT_TOP_K = 20
MAX_PREVIEW_ROWS = 200
LARGE_DATASET_THRESHOLD = 500000

# Chart settings
CHART_HEIGHT = 300
HISTOGRAM_BINS = 30

# File format support
SUPPORTED_EXTENSIONS = ['.csv', '.csv.gz', '.xlsx', '.xls']

# UI settings
UI_THEME = "default"
SHOW_LEGEND = False
