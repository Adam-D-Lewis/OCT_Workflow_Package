# Galvos

This package contains modules to prepare and handle OCT data

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
numpy
scipy
matplotlib


```
Give examples
```

## Module Desription
This project contains several modules.  Each is described below.

### Pipe_And_Filter_Autosection
This module takes frequency domain OCT data and a location data file (galvo data), and sections the OCT data by location according to
the parameters specified in the OCTScanConfig file.  The data is then ready to be opened by the visualization software (add link).

```
See the autosection_all_bin_files_in_path for an example script which will search recursively in a directory for every OCT file
(.bin) and will then section the data and save the sectioned data in a folder named "cut" in preparation to be read by the visualization
software (LabView or ImageJ).
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```
## Authors

* **Adam Lewis** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

