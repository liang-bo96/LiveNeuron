from . import BrainPlotly2DViz, EelbrainPlotly2DViz, create_sample_brain_data

__all__ = ["EelbrainPlotly2DViz", "BrainPlotly2DViz", "create_sample_brain_data"]


if __name__ == "__main__":
    try:
        # Method 2: Use default MNE sample data with region filtering
        viz_2d = EelbrainPlotly2DViz(
            region="aparc+aseg",
            cmap="Reds",
            show_max_only=False,
            arrow_threshold=None,  # Show all arrows
            layout_mode="vertical",
            display_mode="lzry",
            arrow_scale=0.5,  # Shorter arrows for better visibility
        )

        # For regular Python scripts or external browser:
        viz_2d.run()

    except Exception as e:
        print(f"Error starting 2D visualization app: {e}")
        import traceback

        traceback.print_exc()
