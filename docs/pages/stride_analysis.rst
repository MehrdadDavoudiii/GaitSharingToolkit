Stride Analysis
===============

The Stride Analysis module segments continuous gait data into individual strides for per-stride analysis.

.. image:: /_static/images/stride_analysis.png
   :width: 100%
   :alt: Stride Analysis
   :align: center

|

Overview
--------

The output from the C3D Extractor in Excel format serves as the input for stride segmentation. To extract the strides, the following information is used:

- **Gait events**: foot off and heel contact timing
- **Start frame**: the start frame of data capturing (to account for cropping)

This information must be available inside the C3D file.

.. image:: /_static/images/stride_events.png
   :width: 100%
   :alt: Stride Events
   :align: center

|

Output
------

A C3D file can contain several strides recorded for each side (right or left), with multiple variables of kinematics and kinetics. Each stride is saved in a separate sheet of a single Excel file.

.. image:: /_static/images/stride_output.png
   :width: 100%
   :alt: Stride Analysis Output
   :align: center
