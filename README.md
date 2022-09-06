# Gamry
Gamry is a python package that handles the outputted files from a Gamry electrochemistry instrument.

## Installing Gamry
It is recommended to first create a virtual environment. Next, run the following command in said environment:

```console
pip install git+https://github.com/suhasharavindan/gamry.git
```

## Gamry Features
Each data file is used to create a signal object. Using an object allows you to carry the dataframe along with several other attirbutes under one variable. The main attributes that would be useful are type, label and params.

Params are the notes that are read in from the file. These must be written in a dictionary like format with a newline between each, like below. Automatic unit conversion to defaults is included for singular units, like mm or Hz, not mV/s.

Label : Sample 1 0.5 V 1000 Hz 5 min\
Plating Voltage : 0.5 V\
Plating Frequency : 1000 Hz\
Plating Time: 5 min

The EISPOT signal has additional attributes of db_corner_params and phase_corner_params that hold values related to those corner frequency calculations. These assume a single electrode measured against a reference electrode and the standard equivalent circuit related to that. These are calculated when the object is created or when the area is altered.

Additionally, there are data reading and plotting helper functions. These make it incredibly easy to read in the files and plot the data for visual analysis, as shown in the following section. The plotting functions have an option of layout that allows the use to change the theme of the plot - this includes 'default' and 'plain'. They also return the figure to allow post-customization.

Finally, the package also includes data conversion functions that allow the user to manipulate it in other ways. The data can be converted to a ZView compatible file, or all the data can be combined into a tidy dataframe.

## Using Gamry
Here are the majority of use cases for the package. There are other functions, such as the CV plotting function, that generally follow the format of one of the examples below. Use the docstrings to help determine how to use them.

Load all the Gamry files in a folder into a list:
 ```python
from gamry.data import load_signals
signals = load_signals()
```

Load only the EISPOT files in a folder into a list:
 ```python
from gamry.data import load_signals
signals = load_signals(signal_type='EISPOT')
```

Plot the EISPOT files in a bode plot:
 ```python
from gamry.plot import eispot_bode
eispot_bode(signals, 'Graph Title', 'Legend Title').show()
```

Plot the EISPOT files in a bode plot using a plain format:
 ```python
from gamry.plot import eispot_bode
eispot_bode(signals, 'Graph Title', 'Legend Title', layout='plain').show()
```

Filter signals to CVs with "sample1" in the label and a 0.5V plating voltage listed in the params:
 ```python
from gamry.data import filter_signals
CV_s1_05V = filter_signals(signals, 'CV', 'sample1', {'Plating Voltage':'0.5'})
```

Create ZView compatible datafile for further analysis:
 ```python
from gamry.data import convert_zview
convert_zview(signals)
```

Create tidy dataframe for further analysis:
 ```python
from gamry.data import tidy_dataframe
tidy_df = tidy_dataframe(signals)
```

## Contact
If you would like to contact me, you can reach me at saravind@caltech.edu.