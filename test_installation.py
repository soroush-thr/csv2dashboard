#!/usr/bin/env python3
"""
Test script to verify CSV2Dashboard installation and functionality.
Run this script to ensure everything is working correctly.
"""

import sys
import os
import traceback

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ plotly imported successfully")
    except ImportError as e:
        print(f"❌ plotly import failed: {e}")
        return False
    
    try:
        import gradio as gr
        print("✅ gradio imported successfully")
    except ImportError as e:
        print(f"❌ gradio import failed: {e}")
        return False
    
    try:
        from csvdash import load_table, infer_types, launch_ui, export_html
        print("✅ csvdash package imported successfully")
    except ImportError as e:
        print(f"❌ csvdash package import failed: {e}")
        return False
    
    return True

def test_data_loading():
    """Test data loading functionality."""
    print("\n📊 Testing data loading...")
    
    try:
        from csvdash import load_table, infer_types
        
        # Test with sample data if it exists
        sample_file = "examples/sales.csv"
        if os.path.exists(sample_file):
            df = load_table(sample_file)
            print(f"✅ Loaded sample data: {len(df)} rows × {len(df.columns)} columns")
            
            types = infer_types(df)
            print(f"✅ Detected column types: {types}")
            
            return True
        else:
            print("⚠️  Sample data not found, skipping data loading test")
            return True
            
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality without UI."""
    print("\n🔧 Testing basic functionality...")
    
    try:
        from csvdash import load_table, infer_types, apply_filters, summaries_and_figs
        
        # Create a simple test DataFrame
        import pandas as pd
        test_data = {
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'city': ['New York', 'London', 'Tokyo']
        }
        df = pd.DataFrame(test_data)
        
        # Test type inference
        types = infer_types(df)
        print(f"✅ Type inference: {types}")
        
        # Test filtering
        filtered_df = apply_filters(df, types, "", {}, {}, {})
        print(f"✅ Filtering: {len(filtered_df)} rows after filtering")
        
        # Test analysis
        summaries = summaries_and_figs(df, types)
        print(f"✅ Analysis: Generated {len(summaries['figs']['numeric'])} numeric charts")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 CSV2Dashboard Installation Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Loading Test", test_data_loading),
        ("Basic Functionality Test", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! CSV2Dashboard is ready to use.")
        print("\n💡 Try running: python app.py examples/sales.csv")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
