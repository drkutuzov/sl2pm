# SL2PM
A package for tracking particles, red blood cells (RBCs), and blood vessel walls with super-localization from images recorded with two-photon microscopy (2PM). The package is based on the data analysis developed in the manuscript "Super-localization two-photon microscopy for _in vivo_ tracking of particles and surfaces".

## Installation

```
git clone git@github.com:drkutuzov/sl2pm.git
cd sl2pm
pip install -r requirements.txt
```

## Content
Files in `/sl2pm` contain the code for SL2PM. 
Directories in `/examples` contains tutorials on how to analyse data with SL2PM. 
All directories contain Jupyter notebooks with tutorials for how to use sl2pm for a specific task and an example of experimental data (as a numpy array ".npy").

`examples/quantum_dots`: Tracking single quantum dots (QDs) in brain parenchyma.  
`examples/red_blood_cells`: Tracking single RBCs in a capillary.  
`examples/capillaries`: Tracking diameter and center of a capillary.  
`examples/bistable_bias`: Estimating parameters of bistable bias --- artefact present in some detectors (photomultiplier tubes, PMTs) used for 2PM.


## Usage
* Select a folder in `examples` according to the data analysis you need to do.  
* Upload your data (e.g. as a numpy array) to the folder.  
* Make a copy of the Jupyter notebook tutorial.  
* Use the new notebook to analyse your data.  

Note that the tutorial Jyputer notebooks only demonstrate the key parts of the data analysis described in the manuscript "Super-localization two-photon microscopy for _in vivo_ tracking of particles and surfaces".
Parts of the data analysis that can be done with the standard data analysis techniques, which have Python implementation (e.g. numpy, scipy, etc.), are not shown in the tutorials. They need to be implemented by the user based on the specific task at hand.

