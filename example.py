#!/usr/bin/env python3
"""
Example script demonstrating eelbrain-plotly-viz usage.

This script shows different ways to use the brain visualization package:
1. With built-in sample data
2. With custom numpy arrays
3. With dictionary format data
4. Export static images
5. Jupyter notebook display
"""

import numpy as np
from eelbrain_plotly_viz import BrainPlotly2DViz, create_sample_brain_data


def example_1_sample_data():
    """Example 1: Using built-in sample data."""
    print("📊 Example 1: Using built-in sample data")
    print("-" * 50)
    
    # Create visualization with default sample data
    viz = BrainPlotly2DViz(
        cmap='Hot',
        show_max_only=False,
        arrow_threshold='auto'
    )
    
    print(f"✅ Created visualization with {viz.glass_brain_data.shape[0]} sources")
    print(f"   Time points: {len(viz.time_values)}")
    print(f"   Vector data: {viz.has_vector_data}")
    print(f"   Time range: {viz.time_values[0]:.3f}s to {viz.time_values[-1]:.3f}s")
    
    return viz


def example_2_numpy_arrays():
    """Example 2: Using custom numpy arrays."""
    print("\n📊 Example 2: Using custom numpy arrays")
    print("-" * 50)
    
    # Create synthetic brain data
    n_sources = 100
    n_times = 40
    
    # Vector data: (sources, times, xyz)
    data = np.random.rand(n_sources, n_times, 3) * 2 - 1
    
    # Brain-like coordinates
    coords = np.random.rand(n_sources, 3) * 0.16 - 0.08  # Brain size ~16cm
    
    # Time values
    times = np.linspace(0, 0.8, n_times)
    
    # Create visualization
    viz = BrainPlotly2DViz(
        y=data,
        coords=coords,
        times=times,
        cmap='Viridis',
        arrow_threshold=0.5
    )
    
    print(f"✅ Created visualization with custom data:")
    print(f"   Sources: {n_sources}")
    print(f"   Time points: {n_times}")
    print(f"   Data shape: {data.shape}")
    print(f"   Coords shape: {coords.shape}")
    
    return viz


def example_3_dictionary_data():
    """Example 3: Using dictionary format data."""
    print("\n📊 Example 3: Using dictionary format data")
    print("-" * 50)
    
    # Create sample data using the generator
    data_dict = create_sample_brain_data(
        n_sources=150,
        n_times=60,
        has_vector_data=True,
        random_seed=12345
    )
    
    # Create visualization
    viz = BrainPlotly2DViz(
        y=data_dict,
        cmap='Plasma',
        show_max_only=True,  # Show only mean and max in butterfly plot
        arrow_threshold='all'  # Show all arrows
    )
    
    print(f"✅ Created visualization with dictionary data:")
    print(f"   Sources: {data_dict['n_sources']}")
    print(f"   Time points: {data_dict['n_times']}")
    print(f"   Vector data: {data_dict['has_vector_data']}")
    
    return viz


def example_4_scalar_data():
    """Example 4: Using scalar (non-vector) data."""
    print("\n📊 Example 4: Using scalar data")
    print("-" * 50)
    
    # Create scalar data
    data_dict = create_sample_brain_data(
        n_sources=80,
        n_times=30,
        has_vector_data=False,  # Scalar data only
        random_seed=456
    )
    
    viz = BrainPlotly2DViz(
        y=data_dict,
        cmap='YlOrRd',
        show_max_only=False
        # No arrows for scalar data
    )
    
    print(f"✅ Created scalar data visualization:")
    print(f"   Sources: {data_dict['n_sources']}")
    print(f"   Time points: {data_dict['n_times']}")
    print(f"   Vector data: {data_dict['has_vector_data']}")
    print(f"   Data shape: {data_dict['data'].shape}")
    
    return viz


def example_5_export_images(viz):
    """Example 5: Export static images."""
    print("\n📷 Example 5: Export static images")
    print("-" * 50)
    
    try:
        exported_files = viz.export_images(
            output_dir="./example_output",
            time_idx=15,
            format="png",
            width=1000,
            height=800
        )
        
        print("✅ Successfully exported images:")
        for plot_type, filepath in exported_files.items():
            print(f"   {plot_type}: {filepath}")
            
    except Exception as e:
        print(f"❌ Could not export images: {e}")
        print("   (This may require additional dependencies like kaleido)")


def example_6_jupyter_display(viz):
    """Example 6: Jupyter notebook display."""
    print("\n📱 Example 6: Jupyter notebook display")
    print("-" * 50)
    
    try:
        # This will work in Jupyter notebooks
        viz.show_in_jupyter(time_idx=20)
        print("✅ Displayed in Jupyter notebook")
        
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
    print("   viz.run(host='0.0.0.0', port=8888, debug=True)")
    print()
    print("⚠️  Uncomment the line below to actually start the server:")
    print("   (This will block the script until you stop it with Ctrl+C)")
    
    # Uncomment this line to actually run the server:
    # viz.run()


def main():
    """Run all examples."""
    print("🧠 EELBRAIN PLOTLY VISUALIZATION EXAMPLES")
    print("=" * 60)
    
    # Example 1: Sample data
    viz1 = example_1_sample_data()
    
    # Example 2: Numpy arrays
    viz2 = example_2_numpy_arrays()
    
    # Example 3: Dictionary data
    viz3 = example_3_dictionary_data()
    
    # Example 4: Scalar data
    viz4 = example_4_scalar_data()
    
    # Example 5: Export images (using viz3)
    example_5_export_images(viz3)
    
    # Example 6: Jupyter display
    example_6_jupyter_display(viz3)
    
    # Example 7: Interactive server
    example_7_interactive_server(viz3)
    
    print("\n" + "=" * 60)
    print("✅ ALL EXAMPLES COMPLETED!")
    print("🌐 To see interactive visualization, uncomment viz.run() in example_7")
    print("📁 Check ./example_output/ for exported images")
    print("=" * 60)


if __name__ == "__main__":
    main() 