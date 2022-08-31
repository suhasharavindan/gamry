# Gamry
Gamry is a python package that handles the outputted files from a Gamry electrochemistry instrument.

## Installing Gamry
It is recommended to first create a virtual environment. Next, run the following command in said environment:

```console
pip install git+https://github.com/suhasharavindan/gamry.git
```

## Gamry Features
Each data file is used to create a signal object. Using an object allows you to carry the dataframe along with several other attirbutes under one variable. The main attributes that would be useful are type, label and params.

Params are the notes that are read in from the file. These must be written in a dictionary like format with a newline between each, like below:

Plating Voltage : 0.5\
Plating Frequency : 1000

The EISPOT signal has additional attributes of db_corner_params and phase_corner_params that hold values related to those corner frequency calculations. These assume a single electrode measured against a reference electrode and the standard equivalent circuit related to that. These are calculated when the object is created.

Additionally, there are data reading and plotting helper functions. These make it incredibly easy to read in the files and plot the data for visual analysis, as shown below.

## Using Gamry
Here are the majority of use cases for the package. There are other functions, such as the CV plotting function, that generally follow the format of one of the examples below. Use the docstrings to help determine how to use them.

Load all the Gamry files in a folder:
 ```python
from gamry.data import load_signals
signals = load_signals()
```

Load only the EISPOT files in a folder:
 ```python
from gamry.data import load_signals
signals = load_signals(signal_type='EISPOT')
```

Plot the EISPOT files in a bode plot:
 ```python
from gamry.plot import eispot_bode
eispot_bode(signals, 'Graph Title', 'Legend Title')
```

Filter signals to CVs with "sample1" in the label and a 0.5V plating voltage listed in the params:
 ```python
from gamry.data import filter_signals
filter_signals(signals, 'CV', 'sample1', {'Plating Voltage':'0.5'})
```

Create ZView compatible datafile for further analysis:
 ```python
from gamry.data import convert_zview
convert_zview(signals)
```

## Contact
If you would like to contact me, you can reach me at saravind@caltech.edu.