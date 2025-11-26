Installation
============

Requirements
------------

LiveNeuron requires:

* Python 3.8 or higher
* NumPy >= 1.20.0
* Plotly >= 5.0.0
* Dash >= 2.0.0
* Matplotlib >= 3.3.0
* SciPy >= 1.7.0
* Eelbrain (optional, for full functionality)
* macOS only: libomp (for eelbrain OpenMP extensions) – install via ``brew install libomp`` and ensure the library path is visible (e.g., ``export DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib:$DYLD_LIBRARY_PATH``)

Install from GitHub
-------------------

Install directly from GitHub:

.. code-block:: bash

   pip install git+https://github.com/liang-bo96/LiveNeuron.git

Local Development
-----------------

To install from source for development:

.. code-block:: bash

   git clone https://github.com/liang-bo96/LiveNeuron.git
   cd LiveNeuron
   pip install -e .

Development Installation
------------------------

For development installation, clone the repo and install editable plus the extras you need.

Verify Installation
-------------------

To verify the installation, run:

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz
   print("LiveNeuron installed successfully!")

Troubleshooting
---------------

Common Issues
^^^^^^^^^^^^^

**ImportError: No module named 'eelbrain_plotly_viz'**

Make sure you have installed the package correctly. Try:

.. code-block:: bash

   pip install --upgrade LiveNeuron

**Plotly/Dash version conflicts**

If you encounter version conflicts, try:

.. code-block:: bash

   pip install --upgrade plotly dash

**Missing dependencies**

Some features require Eelbrain. Install it with:

.. code-block:: bash

   pip install eelbrain
