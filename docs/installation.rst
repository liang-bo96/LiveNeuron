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

Install from PyPI
-----------------

The simplest way to install LiveNeuron is via pip:

.. code-block:: bash

   pip install LiveNeuron

Install from Source
-------------------

To get the latest development version:

.. code-block:: bash

   git clone https://github.com/liang-bo96/LiveNeuron.git
   cd LiveNeuron
   pip install -e .

Development Installation
------------------------

For development, install with additional dependencies:

.. code-block:: bash

   pip install -e ".[dev]"

This includes:

* pytest (testing)
* black (code formatting)
* flake8 (linting)
* mypy (type checking)
* pre-commit (git hooks)

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

