# Galvos

This package contains modules to prepare and handle OCT data

## Getting Started

### Prerequisites
numpy
scipy
matplotlib

## Module Description
This project contains several modules.  Each is described below.

### Pipe_And_Filter_Autosection
This module takes frequency domain OCT data and a location data file (galvo data), and sections the OCT data by location according to
the parameters specified in the OCTScanConfig file.  The data is then ready to be opened by the visualization software (add link).

See the autosection_all_bin_files_in_path for an example script which will search recursively in a directory for every OCT file
(.bin) and will then section the data and save the sectioned data in a folder named "cut" in preparation to be read by the visualization
software (LabView or ImageJ).

### writeXMLBuildFile
This module provides a python interface to create XML files usable by the EC1000 Galvo Controller by Cambridge Technologies which command the mirror position which directs a laser.  It has low level functions (single mark or jump command) as well as slightly higher level functions as well (draw a square or circle, etc.)

There is also some support for reading and plotting the commands in the xml files, though there are still some bugs at the moment.

### Curvature_Correction
The OCT imaging data has an artificial curvature (not present in the physical system being imaged), and this module is being created to attempt to do a software correction of the data.  Currently in development.

## Authors

* **Adam Lewis** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

