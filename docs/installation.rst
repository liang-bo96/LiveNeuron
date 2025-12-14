Installation
============

Requirements
------------

LiveNeuro requires:

* Python 3.8 or higher
* NumPy >= 1.20.0
* Plotly >= 5.0.0
* Dash >= 2.0.0
* Matplotlib >= 3.3.0
* SciPy >= 1.7.0
* Eelbrain
* Kaleido >= 0.2.0 (for image export)

The recommended procedure is to create an environment through `mamba` 
(see  https://eelbrain.readthedocs.io/en/stable/installing.html) 
and then install LiveNeuro through `pip`.
Install from GitHub
-------------------

Install directly from GitHub:

.. code-block:: bash

   pip install https://github.com/liang-bo96/LiveNeuro/archive/refs/heads/main.zip

Local Development
-----------------

To install from source for development:

.. code-block:: bash

   git clone https://github.com/liang-bo96/LiveNeuro.git
   cd LiveNeuro
   pip install -e .

Verify Installation
-------------------

To verify the installation, run:

.. code-block:: python

   from liveneuro import LiveNeuro
   print("LiveNeuro installed successfully!")

Troubleshooting
---------------

Common Issues
^^^^^^^^^^^^^

**ImportError: No module named 'liveneuro'**

Make sure you have installed the package correctly. Try:

.. code-block:: bash

   pip install --upgrade "https://github.com/liang-bo96/LiveNeuro/archive/refs/heads/main.zip"

**Plotly/Dash version conflicts**

If you encounter version conflicts, try:

.. code-block:: bash

   pip install --upgrade plotly dash

**Missing dependencies**

Some features require Eelbrain.

.. code-block:: bash

   mamba install -c conda-forge eelbrain

See the official Eelbrain install guide for more details: https://eelbrain.readthedocs.io/en/stable/installing.html
