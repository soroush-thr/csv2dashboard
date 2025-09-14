# csv-to-dashboard-min: turn CSV/Excel into an interactive dashboard & a shareable HTML report (one command)

A minimal Python tool that converts CSV and Excel files into interactive web dashboards with filtering, charts, and static HTML export capabilities. Perfect for quick data exploration and sharing insights.

## Quickstart

```bash
# Install dependencies
pip install -r requirements.txt

# Launch interactive dashboard
python app.py examples/sales.csv

# Export static HTML report
python app.py examples/sales.csv --export report.html
```

## Features

- **Interactive Dashboard**: Search, filter, and visualize your data in real-time
- **Auto-Detection**: Automatically detects column types (numeric, categorical, datetime, text)
- **Smart Filtering**: 
  - Global text search across all text columns
  - Range sliders for numeric columns
  - Date pickers for datetime columns
  - Multi-select dropdowns for categorical columns
- **Auto-Generated Charts**: Histograms, bar charts, and time series plots
- **Static Export**: Generate standalone HTML reports that work offline
- **Multiple Formats**: Supports CSV, CSV.GZ, and Excel (.xlsx) files

## Usage

### Interactive Dashboard
```bash
python app.py data.csv                    # Launch dashboard
python app.py data.xlsx --sheet "Sales"  # Excel with specific sheet
python app.py data.csv --host 0.0.0.0    # Make accessible from network
python app.py data.csv --port 8080       # Custom port
```

### Static HTML Export
```bash
python app.py data.csv --export report.html
python app.py data.xlsx --export "Sales Report.html" --title "Q4 Sales Analysis"
```

## Example Dataset

Create a sample dataset to test the tool:

```bash
# Create examples directory
mkdir examples

# Create sample sales data
cat > examples/sales.csv << 'EOF'
Date,Product,Category,Quantity,Price,Region
2024-01-15,Laptop,Electronics,5,999.99,North
2024-01-16,Mouse,Electronics,20,29.99,South
2024-01-17,Desk,Furniture,3,299.99,East
2024-01-18,Chair,Furniture,8,149.99,West
2024-01-19,Monitor,Electronics,4,399.99,North
2024-01-20,Keyboard,Electronics,15,79.99,South
2024-01-21,Bookshelf,Furniture,2,199.99,East
2024-01-22,Table,Furniture,6,249.99,West
2024-01-23,Phone,Electronics,12,699.99,North
2024-01-24,Headphones,Electronics,25,199.99,South
EOF

# Test the dashboard
python app.py examples/sales.csv
```

## FAQ

### How do I make a dashboard from a CSV for free?
This tool provides a completely free solution! Just install the dependencies and run `python app.py your_file.csv`. No registration, no cloud services required.

### How do I convert Excel to a web dashboard?
Use the `--sheet` parameter to specify which sheet to load: `python app.py data.xlsx --sheet "Sheet2"`. If no sheet is specified, it loads the first sheet.

### How do I export my dashboard to a static HTML file?
Use the `--export` flag: `python app.py data.csv --export report.html`. The generated HTML file includes all charts and works offline.

### What file formats are supported?
- CSV files (with auto-delimiter detection)
- Compressed CSV files (.csv.gz)
- Excel files (.xlsx, .xls)

### How large datasets can it handle?
The tool works well with datasets up to ~200k rows. For larger datasets (>500k rows), consider filtering to specific columns or time ranges for better performance.

## Limitations

- Maximum recommended dataset size: ~500k rows
- Limited to basic filter types (no complex queries)
- Charts are generated automatically (no custom chart types)
- No real-time data updates (static snapshots only)

## Requirements

- Python 3.11+
- pandas, plotly, gradio, openpyxl

## License

MIT License - see LICENSE file for details.

## Contributing

Found a bug or want a new feature? Please open an issue on GitHub!