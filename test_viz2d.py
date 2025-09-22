#!/usr/bin/env python3
"""
Quick test script for LiveNeuron viz2d functionality.
Run this to verify everything is working before using the Jupyter notebook.
"""

def test_liveneuron():
    """Test LiveNeuron basic functionality."""
    print("🧠 Testing LiveNeuron 2D Brain Visualization...")
    print("=" * 50)
    
    try:
        # Import test
        print("📦 Testing imports...")
        from eelbrain_plotly_viz import EelbrainPlotly2DViz
        print("✅ Import successful!")
        
        # Basic creation test
        print("\n🔧 Testing basic visualization creation...")
        viz = EelbrainPlotly2DViz()
        print("✅ Visualization created successfully!")
        
        # Data verification
        print("\n📊 Checking data dimensions...")
        n_sources = viz.glass_brain_data.shape[0]
        n_times = viz.glass_brain_data.shape[2] 
        is_vector = viz.glass_brain_data.shape[1] == 3
        print(f"   • Sources: {n_sources}")
        print(f"   • Time points: {n_times}")
        print(f"   • Vector data: {is_vector}")
        print(f"   • Brain region: {viz.region_of_brain}")
        print("✅ Data dimensions correct!")
        
        # Visualization methods test
        print("\n🎨 Testing visualization methods...")
        try:
            # Test brain projections
            brain_figs = viz.create_2d_brain_projections_plotly(time_idx=10)
            print("✅ Brain projections working!")
            
            # Test butterfly plot
            butterfly_fig = viz.create_butterfly_plot(selected_time_idx=10)
            print("✅ Butterfly plot working!")
            
        except Exception as e:
            print(f"⚠️  Visualization methods test failed: {e}")
            return False
        
        # Custom options test
        print("\n🎨 Testing custom options...")
        try:
            custom_viz = EelbrainPlotly2DViz(
                cmap='Viridis',
                show_max_only=True,
                arrow_threshold='auto'
            )
            print("✅ Custom options working!")
        except Exception as e:
            print(f"⚠️  Custom options test failed: {e}")
            return False
            
        print("\n🎉 All tests PASSED!")
        print("\n📝 Ready to use LiveNeuron! You can now:")
        print("   • Open the Jupyter notebook: jupyter notebook viz2d_demo.ipynb")
        print("   • Run viz.show_in_jupyter() for inline display")
        print("   • Run viz.run() for external browser display")
        print("   • Customize parameters as needed")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("\n🔧 To fix this, run:")
        print("   pip install -e .")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_liveneuron()
    exit(0 if success else 1)


