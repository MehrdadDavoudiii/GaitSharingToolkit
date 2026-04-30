Installation
============

Requirements
------------

The toolkit has been developed with **Python 3.13**. Although Python 3.14 is available, the ``ezc3d`` library does not yet provide pre-built wheels for this version. Therefore, Python 3.13 is recommended to ensure full compatibility with all dependencies.

.. code-block:: bash

   pip install -r requirements.txt

Core Dependencies
~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Package
     - Purpose
   * - PySide6
     - Graphical user interface (Qt framework)
   * - numpy
     - Numerical computations
   * - scipy
     - Stride interpolation and signal processing
   * - openpyxl
     - Excel file reading and writing

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

These packages enable additional features. The toolkit degrades gracefully without them.

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Package
     - Purpose
   * - PyMuPDF
     - PDF parsing and anonymization
   * - ezc3d
     - C3D file reading
   * - openai
     - AI Interpreter (ChatGPT integration)
   * - python-docx
     - DOCX report export
   * - Pillow
     - Image processing utilities

Running the Toolkit
-------------------

After installing the requirements, launch the application:

.. code-block:: bash

   python GaitSharing_main.py

The main window will open with the sidebar navigation on the left, providing access to all modules.
