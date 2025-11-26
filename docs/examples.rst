Examples
========

This page provides a couple of focused examples without repeating the user guide or API reference.

Export Images
-------------

Save plots to disk without starting the Dash server:

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   viz = EelbrainPlotly2DViz(display_mode="lyr")
   result = viz.export_images(output_dir="./my_brain_plots", time_idx=30, format="png")

   if result["status"] == "success":
       for plot_type, filepath in result["files"].items():
           print(f"{plot_type}: {filepath}")
   else:
       print(f"Export failed: {result['message']}")

Full Workflow
-------------

A short end-to-end script combining customization, export, and interactive run:

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   def main():
       viz = EelbrainPlotly2DViz(
           y=None,
           region="aparc+aseg",
           cmap="Viridis",
           show_max_only=False,
           arrow_threshold="auto",
           layout_mode="horizontal",
           display_mode="lyr",
       )

       # Export a static snapshot
       result = viz.export_images(output_dir="./example_output", time_idx=20, format="png")
       print("Export status:", result["status"])

       # Launch interactive app (external browser by default)
       viz.run()

   if __name__ == "__main__":
       main()
