#!/usr/bin/env python3
"""
Example script demonstrating LiveNeuron usage.

This script shows different ways to use the brain visualization package:
1. With built-in MNE sample data
2. With different visualization options  
3. Export static images
4. Jupyter notebook display
"""

import numpy as np
from eelbrain_plotly_viz import EelbrainPlotly2DViz
try:
    from eelbrain import datasets, NDVar
    EELBRAIN_AVAILABLE = True
except ImportError:
    EELBRAIN_AVAILABLE = False
    print("Note: eelbrain not available, using built-in sample data only")


def example_1_sample_data():
    """Example 1: Using built-in MNE sample data."""
    print("📊 Example 1: Using built-in MNE sample data")
    print("-" * 50)
    
    # Create visualization with default sample data
    viz = EelbrainPlotly2DViz(
        y=None,  # Use built-in sample data
        region=None,  # Use full brain
        cmap='Hot',
        show_max_only=False,
        arrow_threshold='auto'
    )
    
    print(f"✅ Created visualization with {viz.glass_brain_data.shape[0]} sources")
    print(f"   Time points: {len(viz.time_values)}")
    print(f"   Vector data: {viz.glass_brain_data.ndim == 3}")
    print(f"   Time range: {viz.time_values[0]:.3f}s to {viz.time_values[-1]:.3f}s")
    print(f"   Brain region: {viz.region_of_brain}")
    
    return viz


def example_2_region_filtering():
    """Example 2: Using specific brain region."""
    print("\n📊 Example 2: Using specific brain region")
    print("-" * 50)
    
    # Create visualization with specific brain region
    viz = EelbrainPlotly2DViz(
        y=None,
        region='aparc+aseg',  # Use parcellation
        cmap='Viridis',
        show_max_only=True,  # Show only mean and max traces
        arrow_threshold=0.5
    )
    
    print(f"✅ Created visualization with region filtering:")
    print(f"   Sources: {viz.glass_brain_data.shape[0]}")
    print(f"   Time points: {len(viz.time_values)}")
    print(f"   Brain region: {viz.region_of_brain}")
    print(f"   Colormap: {viz.cmap}")
    
    return viz


def example_3_eelbrain_data():
    """Example 3: Using eelbrain NDVar data."""
    print("\n📊 Example 3: Using eelbrain NDVar data")
    print("-" * 50)
    
    if not EELBRAIN_AVAILABLE:
        print("⚠️  Skipping: eelbrain not available")
        return example_1_sample_data()
    
    try:
        # Load eelbrain data
        data_ds = datasets.get_mne_sample(src='vol', ori='vector')
        y = data_ds['src']  # This is an NDVar
        
        # Create visualization with custom data
        viz = EelbrainPlotly2DViz(
            y=y,  # Pass NDVar directly
            cmap='Plasma',
            show_max_only=False,
            arrow_threshold='auto'
        )
        
        print(f"✅ Created visualization with eelbrain NDVar:")
        print(f"   Original data dimensions: {y.dimnames}")
        print(f"   Data shape: {y.shape}")
        print(f"   Sources: {viz.glass_brain_data.shape[0]}")
        print(f"   Time points: {len(viz.time_values)}")
        
        return viz
        
    except Exception as e:
        print(f"❌ Could not load eelbrain data: {e}")
        return example_1_sample_data()


def example_4_custom_colormap():
    """Example 4: Using custom colormap."""
    print("\n📊 Example 4: Using custom colormap")
    print("-" * 50)
    
    # Custom colormap
    custom_cmap = [
        [0, 'rgba(255,255,0,0.5)'],    # Yellow with 50% transparency
        [0.5, 'rgba(255,165,0,0.8)'],  # Orange with 80% transparency
        [1, 'rgba(255,0,0,1.0)']       # Red with full opacity
    ]
    
    viz = EelbrainPlotly2DViz(
        y=None,
        region=None,
        cmap=custom_cmap,
        show_max_only=True,
        arrow_threshold=None  # Show all arrows
    )
    
    print(f"✅ Created visualization with custom colormap:")
    print(f"   Custom colormap: {len(custom_cmap)} colors")
    print(f"   Arrow threshold: None (all arrows shown)")
    print(f"   Butterfly mode: max only")
    
    return viz


def example_5_export_images(viz):
    """Example 5: Export static images."""
    print("\n📷 Example 5: Export static images")
    print("-" * 50)
    
    try:
        result = viz.export_images(
            output_dir="./example_output",
            time_idx=15,
            format="png"
        )
        
        if result["status"] == "success":
            print("✅ Successfully exported images:")
            for plot_type, filepath in result["files"].items():
                print(f"   {plot_type}: {filepath}")
        else:
            print(f"❌ Export failed: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Could not export images: {e}")
        print("   (This may require additional dependencies like kaleido)")


def example_6_jupyter_display(viz):
    """Example 6: Jupyter notebook display."""
    print("\n📱 Example 6: Jupyter notebook display")
    print("-" * 50)
    
    try:
        # This will work in Jupyter notebooks
        print("To display in Jupyter, use:")
        print("   viz.show_in_jupyter(width=1200, height=900)")
        print()
        print("✅ Jupyter display method available")
        
    except Exception as e:
        print(f"ℹ️  Jupyter display not available: {e}")
        print("   (This only works in Jupyter notebook environments)")


def example_7_interactive_server(viz):
    """Example 7: Interactive web server."""
    print("\n🌐 Example 7: Interactive web server")
    print("-" * 50)
    
    print("To run interactive visualization:")
    print("   viz.run()")
    print("   Then visit: http://127.0.0.1:8050")
    print()
    print("Custom server options:")
    print("   viz.run(port=8888, debug=True)")
    print("   viz.run(mode='inline')  # For Jupyter")
    print("   viz.run(mode='jupyterlab')  # For JupyterLab")
    print()
    print("⚠️  Uncomment the line below to actually start the server:")
    print("   (This will block the script until you stop it with Ctrl+C)")
    
    # Uncomment this line to actually run the server:
    # viz.run()


def example_8_different_options():
    """Example 8: Showcase different visualization options."""
    print("\n🎨 Example 8: Different visualization options")
    print("-" * 50)
    
    options = [
        {
            'name': 'Hot colormap, all arrows',
            'params': {'cmap': 'Hot', 'arrow_threshold': None, 'show_max_only': False}
        },
        {
            'name': 'Viridis colormap, auto threshold',
            'params': {'cmap': 'Viridis', 'arrow_threshold': 'auto', 'show_max_only': True}
        },
        {
            'name': 'YlOrRd colormap, custom threshold',
            'params': {'cmap': 'YlOrRd', 'arrow_threshold': 0.1, 'show_max_only': False}
        }
    ]
    
    vizs = []
    for i, option in enumerate(options):
        print(f"   Creating visualization {i+1}: {option['name']}")
        viz = EelbrainPlotly2DViz(y=None, region=None, **option['params'])
        vizs.append(viz)
    
    print(f"✅ Created {len(vizs)} visualizations with different options")
    return vizs[0]  # Return the first one


def main():
    """Run all examples."""
    print("🧠 EELBRAIN PLOTLY VISUALIZATION EXAMPLES")
    print("=" * 60)
    
    # Example 1: Sample data
    viz1 = example_1_sample_data()
    
    # Example 2: Region filtering
    viz2 = example_2_region_filtering()
    
    # Example 3: Eelbrain data
    viz3 = example_3_eelbrain_data()
    
    # Example 4: Custom colormap
    viz4 = example_4_custom_colormap()
    
    # Example 5: Export images (using viz1)
    example_5_export_images(viz1)
    
    # Example 6: Jupyter display
    example_6_jupyter_display(viz1)
    
    # Example 7: Interactive server
    example_7_interactive_server(viz1)
    
    # Example 8: Different options
    viz8 = example_8_different_options()
    
    print("\n" + "=" * 60)
    print("✅ ALL EXAMPLES COMPLETED!")
    print("🌐 To see interactive visualization, uncomment viz.run() in example_7")
    print("📁 Check ./example_output/ for exported images")
    print("\n💡 Key features of EelbrainPlotly2DViz:")
    print("   • Interactive 2D brain projections (axial, sagittal, coronal)")
    print("   • Butterfly plot with source time series")
    print("   • Support for vector data with directional arrows")
    print("   • Customizable colormaps and thresholds")
    print("   • Jupyter notebook integration")
    print("   • Image export capabilities")
    print("=" * 60)


if __name__ == "__main__":
    main() 