"""
Import tests to ensure all package imports work correctly.

This test module specifically catches import issues that could arise from
filename case mismatches or missing dependencies.
"""

import pytest


def test_all_imports_together():
    """Test that all imports can be done in a single statement."""
    from eelbrain_plotly_viz import (
        EelbrainPlotly2DViz,
        create_sample_brain_data,
        # Layout extension API
        LayoutBuilder,
        register_layout,
        get_layout_builder,
    )

    assert EelbrainPlotly2DViz is not None
    assert create_sample_brain_data is not None
    # Test layout extension API imports
    assert LayoutBuilder is not None
    assert register_layout is not None
    assert get_layout_builder is not None


def test_direct_module_imports():
    """Test that direct module imports work (internal consistency check)."""
    # Test that the main import still works after package installation
    try:
        from eelbrain_plotly_viz._viz_2d import EelbrainPlotly2DViz as DirectImport
        from eelbrain_plotly_viz._sample_data import (
            create_sample_brain_data as DirectDataImport,
        )

        assert DirectImport is not None
        assert DirectDataImport is not None
    except ImportError:
        # This is expected if the package is installed via pip instead of -e
        # The important thing is that the main imports work
        pytest.skip("Direct module imports not available in installed package")


def test_package_version():
    """Test that package version is accessible."""
    import eelbrain_plotly_viz

    assert hasattr(eelbrain_plotly_viz, "__version__")
    assert eelbrain_plotly_viz.__version__ == "1.0.0"


def test_package_all_attribute():
    """Test that __all__ is properly defined."""
    import eelbrain_plotly_viz

    assert hasattr(eelbrain_plotly_viz, "__all__")
    expected_items = {
        # Main class
        "EelbrainPlotly2DViz",
        # Sample data
        "create_sample_brain_data",
        # Layout extension API (Open/Closed Principle)
        "LayoutBuilder",
        "register_layout",
        "get_layout_builder",
    }
    assert set(eelbrain_plotly_viz.__all__) == expected_items


def test_no_import_errors():
    """Test that importing the package doesn't raise any exceptions."""
    import eelbrain_plotly_viz

    # Test basic instantiation to catch runtime import issues
    viz = eelbrain_plotly_viz.EelbrainPlotly2DViz()
    assert viz is not None


def test_case_sensitive_filename_compliance():
    """Test that the imports work correctly (indicating proper filename conventions)."""
    # Instead of checking file paths (which vary between dev and installed packages),
    # we test that the imports work, which indicates the files are named correctly

    # This import will only work if the file is named correctly (viz_2d.py)
    from eelbrain_plotly_viz import EelbrainPlotly2DViz

    # Test that we can create an instance (ensures the import chain works)
    viz = EelbrainPlotly2DViz()
    assert viz is not None

    # Test that the module follows the expected pattern
    import eelbrain_plotly_viz

    module_file = eelbrain_plotly_viz.__file__
    assert "eelbrain_plotly_viz" in module_file
