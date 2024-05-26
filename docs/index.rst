.. mockup documentation master file, created by
   sphinx-quickstart on Mon Aug 28 14:09:15 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SL2PM
==================================
A package for tracking particles, red blood cells (RBCs), and blood vessel walls with super-localization from images recorded with two-photon microscopy (2PM).
The package is based on the data analysis developed in the manuscript:
"Super-localization two-photon microscopy for in vivo tracking of nanoparticles, red blood cells, and capillary walls"
The data analysis in SL2PM is data-driven, i.e., you need to check if underlying assumptions of SL2PM analysis are satisfied in your data before you apply any functions from SL2PM. This is why we suggest using SL2PM with Jupyter notebooks, where you can explore your data step-by-step (following our examples) and tailor SL2PM analysis to your data, if needed.

To get started to SL2PM, explore the tutorials for different usecases

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference/modules

.. toctree::
   :maxdepth: 2
   :caption: Fitting bistable bias
   
   tutorial/bistable_bias/bistable_bias_example

.. toctree::
   :maxdepth: 2
   :caption: Calibrating PSF
   
   tutorial/capillaries/calibration_example

.. toctree::
   :maxdepth: 2
   :caption: Calibrating photo-multiplier tubes
   
   tutorial/pmt_calibration/pmt_calibration_example

   .. toctree::
   :maxdepth: 2
   :caption: Tracking a single quantum dot
   
   tutorial/quantum_dots/qd_example

   .. toctree::
   :maxdepth: 2
   :caption: Tracking a single red blood cell
   
   tutorial/red_blood_cells/rbc_example

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
