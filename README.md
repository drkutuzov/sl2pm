# SL2PM
A package for tracking particles, red blood cells (RBCs), and microvessel walls with super-localization from images recorded with two-photon microscopy (2PM). 

To get started with SL2PM, explore tutorials for tracking quantum dots, 
red blood cells, and capillaries. 
For example, if you are interested in measuring diameter of a capillary, made visible with fluorescently-labeled plasma (e.g. with FITC-dextran), see `tutorial/capillaries/track_capillary.ipynb` notebook.  

All tracking algorithms require calibration of the microscope's photomultiplier tubes (`tutorial/pmt_calibration/PMT_calibration.ipynb`) and, for tracking capillaries, calibration of the microscope's point-spread function (`tutorial/capillaries/PSF_calibration.ipynb`).

The data analysis in SL2PM is data-driven, i.e., you need to check if underlying assumptions of SL2PM analysis are satisfied 
in your data before you apply any function from SL2PM.
This is why we suggest using SL2PM with Jupyter notebooks, where you can explore your data step-by-step (following our examples) and tailor SL2PM analysis to your data, if needed. 

The documentation can be found at [https://sl2pm.readthedocs.io/en/latest/index.html](https://sl2pm.readthedocs.io/en/latest/index.html)

## Installation

Install from the PyPi distribution

```
pip install sl2pm
```

Or from the source

```
git clone git@github.com:drkutuzov/sl2pm.git
cd sl2pm
pip install -e .
```

## Content
`src/sl2pm` contains the code for SL2PM.  
`docs/tutorial` contains folders with examples of data analysis with SL2PM. Each folder contains Jupyter notebooks tutorials and examples of experimental data (as numpy arrays).

`docs/tutorial/quantum_dots`: Tracking single quantum dots (QDs) in the brain parenchyma.  
`docs/tutorial/red_blood_cells`: Tracking single RBCs in a brain capillary.  
`docs/tutorial/capillaries`: Tracking diameter and center of a brain capillary and calibration of the microscope's PSF.  
`docs/tutorial/pmt_calibration`: Calibrating photomultiplier tubes (PMTs) for SL2PM.  
`docs/tutorial/bistable_bias`: Estimating parameters of bistable bias – artefact sometimes present in the output of PMTs.

## Usage
* Select a folder in `docs/tutorial` based on the data analysis you need.  
* Upload your data (e.g. as a numpy array) to the folder.  
* Make a copy of the Jupyter notebook tutorial or make a new one.  
* Use the notebook to analyse your data using the tutorial as a guide.  
