Building Documentation
======================

This directory contains the Sphinx documentation for LiveNeuron.

Local Build
-----------

To build the documentation locally:

1. Install documentation dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

2. Build HTML documentation:

   .. code-block:: bash

      make html

3. View the documentation:

   .. code-block:: bash

      open _build/html/index.html

Read the Docs
-------------

The documentation is automatically built and hosted on Read the Docs at:
https://liveneuron.readthedocs.io

The build is triggered automatically on every push to the main branch.

Configuration
-------------

* ``.readthedocs.yaml``: Read the Docs configuration
* ``conf.py``: Sphinx configuration
* ``requirements.txt``: Documentation build dependencies

Documentation Structure
-----------------------

* ``index.rst``: Main documentation page
* ``installation.rst``: Installation instructions
* ``user_guide.rst``: Comprehensive user guide (recommended starting point)
* ``api_reference.rst``: Complete API reference
* ``examples.rst``: Practical examples
* ``changelog.rst``: Version history and release notes

Rebuilding
----------

To clean and rebuild:

.. code-block:: bash

   make clean
   make html

For other formats:

.. code-block:: bash

   make latexpdf  # PDF via LaTeX
   make epub      # EPUB ebook format


