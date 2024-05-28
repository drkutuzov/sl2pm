.. mockup documentation master file, created by
   sphinx-quickstart on Mon Aug 28 14:09:15 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SL2PM
==================================
A package for tracking particles, red blood cells (RBCs), and microvessel walls with super-localization from images recorded with two-photon microscopy (2PM). 

To get started with SL2PM, explore tutorials for tracking quantum dots, 
red blood cells, and capillaries. 
For example, if you are interested in measuring diameter of a capillary, made visible with fluorescently-labeled plasma (e.g. with FITC-dextran), see `Tracking a capillary` demo.  

All tracking algorithms require calibration of the microscope's photomultiplier tubes (`Calibrating photomultiplier tubes (PMTs)`) and, for tracking capillaries, calibration of the microscope's point-spread function (`Calibrating point-spread function (PSF)`).

The data analysis in SL2PM is data-driven, i.e., you need to check if underlying assumptions of SL2PM analysis are satisfied 
in your data before you apply any functions from SL2PM.
This is why we suggest using SL2PM with Jupyter notebooks, where you can explore your data step-by-step (following our examples) and tailor SL2PM analysis to your data, if needed. 

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference/modules

.. toctree::
   :maxdepth: 2
   :caption: Tracking a quantum dot
   
   tutorial/quantum_dots/track_qd

.. toctree::
   :maxdepth: 2
   :caption: Tracking a red blood cell

   tutorial/red_blood_cells/track_rbc

.. toctree::
   :maxdepth: 2
   :caption: Tracking a capillary

   tutorial/capillaries/track_capillary

.. toctree::
   :maxdepth: 2
   :caption: Calibrating point-spread function (PSF)
   
   tutorial/capillaries/PSF_calibration

.. toctree::
   :maxdepth: 2
   :caption: Calibrating photomultiplier tubes (PMTs)
   
   tutorial/pmt_calibration/PMT_calibration

.. toctree::
   :maxdepth: 2
   :caption: Removing artefact from output of photomultiplier tubes
   
   tutorial/bistable_bias/bistable_bias_example


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
