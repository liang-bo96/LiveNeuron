#!/usr/bin/env python3
"""
Start the interactive visualization with real-time mode enabled.
This demonstrates the real-time hover feature we implemented.
"""

from eelbrain_plotly_viz import EelbrainPlotly2DViz

def main():
    print("🧠 Starting Interactive Brain Visualization with Real-time Mode")
    print("=" * 60)
    
    # Create visualization with real-time mode enabled
    viz = EelbrainPlotly2DViz(realtime=True)
    
    print("✅ Created visualization with:")
    print(f"   • {viz.glass_brain_data.shape[0]} brain sources")
    print(f"   • {len(viz.time_values)} time points")
    print(f"   • Real-time mode: ENABLED")
    print()
    print("🎯 Real-time Features:")
    print("   • Hover over butterfly plot → brain updates in real-time")
    print("   • Click on butterfly plot → locks time point for inspection")
    print("   • Toggle real-time mode with checkbox")
    print()
    print("🌐 Starting web server at http://127.0.0.1:8050")
    print("📱 Open your browser and navigate to the URL above")
    print()
    print("⚠️  Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the interactive server
    viz.run(debug=True)

if __name__ == "__main__":
    main()
