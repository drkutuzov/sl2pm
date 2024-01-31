# SL2PM
A package for tracking particles, red blood cells (RBCs), and blood vessel walls with super-localization from images recorded with two-photon microscopy (2PM). The package is based on the data analysis developed in the manuscript:  

> Kutuzov N., Lauritzen M., and Flyvbjerg H. 
> Super-localization two-photon microscopy for _in vivo_ tracking of particles and surfaces.

## Installation

```
git clone git@github.com:drkutuzov/sl2pm.git
cd sl2pm
pip install -r requirements.txt
```

## Content
`/sl2pm` contains the code for SL2PM.  
`/examples` contains folders with specific examples of data analysis with SL2PM. Each folder contains Jupyter notebooks tutorials and examples of experimental data (as numpy arrays).

`examples/quantum_dots`: Tracking single quantum dots (QDs) in brain parenchyma.  
`examples/red_blood_cells`: Tracking single RBCs in a capillary.  
`examples/capillaries`: Tracking diameter and center of a capillary.  
`examples/bistable_bias`: Estimating parameters of bistable bias – artefact present in some detectors (photomultiplier tubes, PMTs) used for 2PM.

## Usage
* Select a folder in `examples` based on the data analysis you need.  
* Upload your data (e.g. as a numpy array) to the folder.  
* Make a copy of the Jupyter notebook tutorial or make a new notebook.  
* Use the notebook to analyse your data using the tutorial as a guide.  

Note that the tutorial Jyputer notebooks only demonstrate the key parts of the data analysis described in the manuscript "Super-localization two-photon microscopy for _in vivo_ tracking of particles and surfaces".
Parts of the data analysis that can be done with the standard data analysis techniques, which have Python implementation (e.g. numpy, scipy, etc.), are not shown in the tutorials. They need to be implemented by the user based on the specific task at hand.

