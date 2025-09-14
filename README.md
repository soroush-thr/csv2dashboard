# 📊 CSV2Dashboard: Professional Data Visualization Tool

**Transform your CSV and Excel files into stunning interactive dashboards and professional HTML reports with just one command!**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A powerful, modular Python tool that instantly converts your data files into interactive web dashboards with advanced filtering, automatic chart generation, and professional HTML export capabilities. Perfect for data scientists, analysts, and anyone who needs to quickly explore and share data insights.

## ✨ Key Features

- 🚀 **One-Command Setup**: Launch interactive dashboards instantly
- 🎯 **Smart Auto-Detection**: Automatically identifies column types and generates appropriate visualizations
- 🔍 **Advanced Filtering**: Multi-dimensional filtering with text search, ranges, and categorical selections
- 📈 **Auto-Generated Charts**: Beautiful histograms, bar charts, and time series plots
- 📄 **Professional Export**: Generate standalone HTML reports that work offline
- 🗂️ **Multi-Format Support**: CSV, CSV.GZ, Excel (.xlsx, .xls) files
- ⚡ **High Performance**: Optimized for datasets up to 500K+ rows
- 🎨 **Modern UI**: Clean, responsive interface built with Gradio

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/soroush-thr/csv2dashboard.git
cd csv2dashboard

# Install dependencies
pip install -r requirements.txt

# Optional: Install in development mode
pip install -e .
```

### Basic Usage

```bash
# Launch interactive dashboard
python app.py examples/sales.csv

# Export static HTML report
python app.py examples/sales.csv --export report.html

# Use as a package (after installation)
csv2dashboard examples/sales.csv
```

### Try It Now!

```bash
# First, verify everything is working
python test_installation.py

# Then test with the included sample data
python app.py examples/sales.csv --title "Sales Dashboard Demo"
```

## 📋 Detailed Features

### 🎯 Smart Data Processing
- **Automatic Type Detection**: Intelligently identifies numeric, categorical, datetime, and text columns
- **Robust File Parsing**: Handles various CSV delimiters, compressed files, and Excel sheets
- **Data Validation**: Built-in error handling and data quality checks

### 🔍 Advanced Filtering System
- **Global Text Search**: Search across all text and categorical columns simultaneously
- **Numeric Range Filters**: Interactive sliders for precise numeric value filtering
- **Date Range Selection**: Intuitive date pickers for time-based data
- **Categorical Multi-Select**: Dropdown filters for categorical data with "All" option
- **Real-time Updates**: Filters apply instantly as you interact with the interface

### 📊 Automatic Visualization
- **Histograms**: Distribution analysis for numeric columns
- **Bar Charts**: Top value analysis for categorical data
- **Time Series**: Trend analysis for datetime columns
- **Responsive Design**: Charts automatically resize and adapt to your screen

### 📄 Professional Export
- **Standalone HTML**: Self-contained reports that work offline
- **Interactive Charts**: Exported reports maintain chart interactivity
- **Custom Styling**: Professional CSS styling for reports
- **Filter Documentation**: Exported reports include applied filter information

## 💻 Usage Guide

### Interactive Dashboard

```bash
# Basic usage
python app.py data.csv

# Excel files with specific sheet
python app.py data.xlsx --sheet "Sales"

# Network access (accessible from other devices)
python app.py data.csv --host 0.0.0.0 --port 8080

# Custom title and port
python app.py data.csv --title "My Analysis" --port 9000
```

### Static HTML Export

```bash
# Basic export
python app.py data.csv --export report.html

# Custom title and filename
python app.py data.xlsx --export "Q4_Sales_Report.html" --title "Q4 Sales Analysis"

# Export with specific sheet
python app.py data.xlsx --sheet "Q4" --export "Q4_Report.html"
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `file` | Path to CSV or Excel file | Required |
| `--sheet` | Excel sheet name or number | First sheet |
| `--host` | Host to bind to | 127.0.0.1 |
| `--port` | Port to bind to | 7860 |
| `--export` | Export static HTML report | None |
| `--title` | Dashboard title | "CSV Dashboard" |

## 🧪 Testing

### Quick Test

Test the tool with the included sample data:

```bash
# Test interactive dashboard
python app.py examples/sales.csv

# Test HTML export
python app.py examples/sales.csv --export test_report.html

# Test with different parameters
python app.py examples/sales.csv --title "Test Dashboard" --port 8080
```

### Test with Your Own Data

```bash
# Test with your CSV file
python app.py your_data.csv

# Test Excel file
python app.py your_data.xlsx --sheet "Sheet1"

# Test compressed CSV
python app.py your_data.csv.gz
```

### Unit Tests

```bash
# Run comprehensive installation test
python test_installation.py

# Run basic import tests
python -c "from csvdash import load_table, infer_types; print('✅ Import successful!')"

# Test data loading
python -c "
from csvdash import load_table, infer_types
df = load_table('examples/sales.csv')
types = infer_types(df)
print(f'✅ Loaded {len(df)} rows, detected {len(types)} column types')
"
```

### Performance Testing

```bash
# Test with large dataset (if you have one)
python app.py large_dataset.csv --title "Performance Test"
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use the issue template** and provide:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Sample data (if applicable)
   - System information (OS, Python version)

### 🚀 Contributing Code

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following our coding standards
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to your branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### 📝 Development Setup

```bash
# Clone your fork
git clone https://github.com/soroush-thr/csv2dashboard.git
cd csv2dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest  # Optional: for code formatting and testing
```

### 🧪 Running Tests

```bash
# Test imports
python -c "import csvdash; print('✅ Package imports successfully')"

# Test with sample data
python app.py examples/sales.csv --export test_output.html

# Code formatting (if you have black installed)
black csvdash/ app.py

# Linting (if you have flake8 installed)
flake8 csvdash/ app.py
```

### 📋 Coding Standards

- **Follow PEP 8** style guidelines
- **Use type hints** for function parameters and return values
- **Write docstrings** for all public functions
- **Keep functions focused** on a single responsibility
- **Add comments** for complex logic
- **Test your changes** before submitting

### 🎯 Areas for Contribution

- **New chart types**: Add more visualization options
- **Enhanced filtering**: More advanced filter types
- **Performance improvements**: Optimize for larger datasets
- **UI enhancements**: Improve the Gradio interface
- **Export formats**: Add PDF, Excel export options
- **Documentation**: Improve examples and guides
- **Testing**: Add comprehensive test suite
- **Bug fixes**: Help resolve reported issues

## ❓ FAQ

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
The tool works well with datasets up to ~500k rows. For larger datasets, consider filtering to specific columns or time ranges for better performance.

### Can I customize the charts?
Currently, charts are auto-generated based on data types. Customization options are planned for future releases.

## 📊 Project Structure

```
csv2dashboard/
├── app.py                 # Main entry point
├── setup.py              # Package installation
├── requirements.txt      # Dependencies
├── csvdash/             # Main package
│   ├── __init__.py      # Package exports
│   ├── cli.py           # Command-line interface
│   ├── config.py        # Configuration settings
│   ├── data_loader.py   # File loading & type inference
│   ├── filters.py       # Data filtering logic
│   ├── analysis.py      # Statistical analysis & charts
│   ├── export.py        # HTML report generation
│   ├── ui.py            # Gradio interface
│   └── utils.py         # Utility functions
└── examples/            # Sample data files
```

## 📋 Requirements

- **Python**: 3.8 or higher
- **Dependencies**: pandas, plotly, gradio, openpyxl
- **Memory**: 2GB+ RAM recommended for large datasets
- **Browser**: Modern web browser for dashboard interface

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Gradio](https://gradio.app/) for the web interface
- Powered by [Plotly](https://plotly.com/) for interactive charts
- Data processing with [Pandas](https://pandas.pydata.org/)
- Excel support via [OpenPyXL](https://openpyxl.readthedocs.io/)

---

**Made with ❤️ for the data community**