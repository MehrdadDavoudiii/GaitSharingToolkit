Anonymizer
==========

The Anonymizer module removes personally identifiable information from clinical PDF reports, enabling safe data sharing.

.. image:: /_static/images/anonymizer_window.png
   :width: 100%
   :alt: Anonymizer Window
   :align: center

|

Overview
--------

To share clinical outputs (e.g., with generic LLMs or other centres), patient data must first be anonymized, especially the patient reports. After selecting the file, the location and name of the anonymized file can be specified.

How It Works
------------

The process works by extracting text from PDFs and searching for sensitive keywords from a predefined list. The list is provided in **German, French, Italian, and English**.

.. image:: /_static/images/anonymizer_terms.png
   :width: 100%
   :alt: Redaction Terms Manager
   :align: center

|

Sensitive terms can be added or edited by clicking the **Manage Redaction Terms** button.

Redaction Modes
---------------

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Mode
     - Description
   * - **Standard**
     - Covers only the exact detected word in the list
   * - **Enhanced**
     - Aggressively covers the area around the word (recommended for clinical purposes)
