#!/usr/bin/env python3
"""
Package validation script for eelbrain-plotly-viz.

This script tests that the package is properly structured and functional
according to Python packaging standards.
"""

import sys
import importlib
import subprocess
import os


def test_package_structure():
    """Test that package has proper structure."""
    print("📁 Testing package structure...")
    
    required_files = [
        "pyproject.toml",
        "README.md", 
        "LICENSE",
        "src/eelbrain_plotly_viz/__init__.py",
        "src/eelbrain_plotly_viz/viz_2d.py",
        "src/eelbrain_plotly_viz/sample_data.py",
        "tests/test_basic.py",
        "example.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True


def test_package_imports():
    """Test that package imports work correctly."""
    print("\n📦 Testing package imports...")
    
    try:
        # Test main package import
        import eelbrain_plotly_viz
        print("✅ Main package imports successfully")
        
        # Test specific imports
        from eelbrain_plotly_viz import BrainPlotly2DViz, create_sample_brain_data
        print("✅ Core classes import successfully")
        
        # Test package metadata
        if hasattr(eelbrain_plotly_viz, '__version__'):
            print(f"✅ Package version: {eelbrain_plotly_viz.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_basic_functionality():
    """Test basic package functionality."""
    print("\n🧠 Testing basic functionality...")
    
    try:
        from eelbrain_plotly_viz import BrainPlotly2DViz, create_sample_brain_data
        import numpy as np
        
        # Test sample data creation
        data_dict = create_sample_brain_data(n_sources=20, n_times=10)
        print("✅ Sample data creation works")
        
        # Test visualization creation with sample data
        viz1 = BrainPlotly2DViz()
        print("✅ Visualization with built-in data works")
        
        # Test visualization with numpy data
        data = np.random.rand(10, 5, 3)
        coords = np.random.rand(10, 3) * 0.1
        times = np.linspace(0, 1, 5)
        viz2 = BrainPlotly2DViz(y=data, coords=coords, times=times)
        print("✅ Visualization with numpy data works")
        
        # Test visualization with dict data
        viz3 = BrainPlotly2DViz(y=data_dict)
        print("✅ Visualization with dict data works")
        
        # Test brain projection creation
        projections = viz1.create_2d_brain_projections_plotly(time_idx=0)
        assert 'axial' in projections
        assert 'sagittal' in projections
        assert 'coronal' in projections
        print("✅ Brain projections creation works")
        
        # Test butterfly plot creation
        butterfly = viz1.create_butterfly_plot()
        assert hasattr(butterfly, 'data')
        print("✅ Butterfly plot creation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality error: {e}")
        return False


def test_dependencies():
    """Test that required dependencies are available."""
    print("\n📚 Testing dependencies...")
    
    required_deps = [
        'dash',
        'plotly', 
        'numpy',
        'matplotlib',
        'scipy'
    ]
    
    missing_deps = []
    for dep in required_deps:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep} available")
        except ImportError:
            missing_deps.append(dep)
            print(f"❌ {dep} missing")
    
    # Test optional dependencies
    optional_deps = ['eelbrain']
    for dep in optional_deps:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep} available (optional)")
        except ImportError:
            print(f"ℹ️  {dep} not available (optional)")
    
    return len(missing_deps) == 0


def test_build_system():
    """Test that the package can be built."""
    print("\n🔨 Testing build system...")
    
    try:
        # Check if build tool is available
        subprocess.run([sys.executable, '-m', 'build', '--help'], 
                      capture_output=True, check=True)
        print("✅ Build tool available")
        
        # Test that pyproject.toml is valid
        import tomli
        with open('pyproject.toml', 'rb') as f:
            config = tomli.load(f)
        
        # Check required build-system fields
        if 'build-system' in config:
            build_system = config['build-system']
            if 'requires' in build_system and 'build-backend' in build_system:
                print("✅ pyproject.toml build system properly configured")
            else:
                print("❌ pyproject.toml missing build system configuration")
                return False
        else:
            print("❌ pyproject.toml missing [build-system] section")
            return False
        
        # Check project metadata
        if 'project' in config:
            project = config['project']
            required_fields = ['name', 'version', 'description', 'dependencies']
            missing_fields = [f for f in required_fields if f not in project]
            if missing_fields:
                print(f"❌ pyproject.toml missing project fields: {missing_fields}")
                return False
            else:
                print("✅ pyproject.toml project metadata complete")
        
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Build tool not available")
        return False
    except ImportError:
        print("ℹ️  tomli not available for config validation")
        return True  # Not critical for basic functionality
    except Exception as e:
        print(f"❌ Build system error: {e}")
        return False


def test_example_script():
    """Test that the example script runs without errors."""
    print("\n📋 Testing example script...")
    
    try:
        # Import example script
        import example
        print("✅ Example script imports successfully")
        
        # Test individual example functions
        viz1 = example.example_1_sample_data()
        print("✅ Example 1 (sample data) works")
        
        viz2 = example.example_2_numpy_arrays()
        print("✅ Example 2 (numpy arrays) works")
        
        viz3 = example.example_3_dictionary_data()
        print("✅ Example 3 (dictionary data) works")
        
        viz4 = example.example_4_scalar_data()
        print("✅ Example 4 (scalar data) works")
        
        return True
        
    except Exception as e:
        print(f"❌ Example script error: {e}")
        return False


def main():
    """Run all validation tests."""
    print("🔍 EELBRAIN-PLOTLY-VIZ PACKAGE VALIDATION")
    print("=" * 60)
    
    tests = [
        ("Package Structure", test_package_structure),
        ("Package Imports", test_package_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Dependencies", test_dependencies),
        ("Build System", test_build_system),
        ("Example Script", test_example_script),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print("\n" + "=" * 60)
    if passed == total:
        print(f"🎉 ALL TESTS PASSED! ({passed}/{total})")
        print("✅ Package is ready for distribution!")
        print("\nNext steps:")
        print("1. Update GitHub URLs in pyproject.toml and README.md")
        print("2. Create GitHub repository")
        print("3. Push code to GitHub")
        print("4. Test installation: pip install git+https://github.com/your-username/eelbrain-plotly-viz.git")
        return True
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total} passed)")
        print("Please fix the issues above before distribution.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 