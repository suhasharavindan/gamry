# Gamry
Gamry is a python package that handles the outputted files from a Gamry electrochemistry instrument.

## Installing Gamry
It is recommended to first create a virtual environment. Next, run the following command in said environment:

```console
pip install git+https://github.com/suhasharavindan/gamry.git
```

To update the package to include new changes, you must uninstall and reinstall the package:

```console
pip uninstall gamry
pip install git+https://github.com/suhasharavindan/gamry.git
```

## Gamry Features
Each data file is used to create a signal object. Using an object allows you to carry the dataframe along with several other attributes under one variable. The main attributes that would be useful are type, label and params.

Params are the notes that are read in from the file. These must be written in a dictionary like format with a newline between each, like below. Automatic unit conversion to defaults is included for singular units, like mm or Hz, not mV/s.

Label : Sample 1 0.5 V 1000 Hz 5 min\
Plating Voltage : 0.5 V\
Plating Frequency : 1000 Hz\
Plating Time: 5 min

The EISPOT signal has additional attributes of db_corner_params and phase_corner_params that hold values related to those corner frequency calculations. These assume a single electrode measured against a reference electrode and the standard equivalent circuit related to that. These are calculated when the object is created or when the area is altered.

Additionally, there are data reading and plotting helper functions. These make it incredibly easy to read in the files and plot the data for visual analysis, as shown in the following section. The plotting functions have an option of theme that allows the use to change the look of the plot - this currently includes 'default' and 'plain' options. They also return the figure to allow post-customization.

Finally, the package also includes data conversion functions that allow the user to manipulate it in other ways. The data can be converted to a ZView compatible file, or all the data can be combined into a tidy dataframe.

## Using Gamry
Here are the majority of use cases for the package. Use the docstrings to help determine how to use them.

Signal properties:
 ```python
signal.type # (str) Signal type
signal.label # (str) Signal name
signal.params # (dict) Parameters read from datafile notes
signal.df # (pandas Dataframe) Signal data
signal.area # (float) Electrode area in cm^2
```

Load Gamry files in a folder into a list:
 ```python
from gamry.data import load_signals

signals = load_signals(folderpath=None, signal_type=None, ignore_notes=False)
    """Read in signals from Gamry exported data.

    Args:
        folderpath (str, optional): Folder with signal files. Defaults to None.
        signal_type (str, optional): Signal type for filtering. Defaults to None.
        ignore_notes (bool, optional): Read notes in Gamry file. Defaults to False.

    Returns:
        list: Signals.
    """
```

Other datafile loading functions that will probably be used less often:
 ```python
from gamry.data import get_filenames, create_signal

get_filenames(folderpath):
    """Filter Gamry files in folder.

    Args:
        folderpath (str): Folder to pull signal files from.

    Returns:
        list: Gamry signal filenames.
    """

create_signal(filepath, signal_type=None, ignore_notes=False):
    """Create proper signal object based on tag in signal file.

    Args:
        filepath (str): Signal file.
        signal_type (str, optional): Signal type for filtering. Defaults to None.
        ignore_notes (bool, optional): Read notes in Gamry file. Defaults to False.

    Returns:
        signal object: Relevant signal object.
    """
```

Plot the EISPOT files in a bode plot:
 ```python
from gamry.plot import eispot_bode

plt = eispot_bode(signals, title, legend_title, db=True, name=None, theme='default')
    """Bode plot of EISPOT signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        db (bool, optional): Plot magnitude as dB. Defaults to True.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure.
    """
```

Other plotting functions and options:
 ```python
plt = eispot_mag(signals, title, legend_title, db=True, name=None, theme='default'):
    """Magnitude plot for EISPOT signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        db (bool, optional): Plot magnitude as dB. Defaults to True.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure.
    """

plt = eispot_phase(signals, title, legend_title, name=None, theme='default'):
    """Phase plot for EISPOT signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure."""

plt = eispot_nyquist(signals, title, legend_title, name=None, theme='default'):
    """Nyquist plot for EISPOT signals."""

plt = eismon_mag(signals, title, legend_title, name=None, theme='default'):
    """Magnitude plot for EISMON signals."""

plt = eismon_phase(signals, title, legend_title, name=None, theme='default'):
    """Phase plot for EISMON signals."""

plt = cv(signals, title, legend_title, name=None, theme='default'):
    """Plot CV signals."""

plt = cpc(signals, title, legend_title, name=None, theme='default'):
    """Plot CPC signals.    """

plt = chronoa(signals, title, legend_title, name=None, theme='default'):
    """Plot CHRONOA signals."""
```

Filter signals based on various parameters:
 ```python
from gamry.data import filter_signals

filtered_signals = filter_signals(signals, signal_type=None, label=None, **param_filters):
    """
    Args:
        signals (list): Signals.
        signal_type (str, optional): Signal type to filter. Defaults to None.
        label (str, optional): Signal label to filter. Defaults to None.
        **param_filters: Arbitrary keyword arguments to filter signal.params.

    Returns:
        list: Filtered signals.
    """
```

Create ZView compatible datafile for further analysis:
 ```python
from gamry.data import convert_zview

convert_zview(signals):
    """
    Args:
        signals (list): Signals.
    """
```

Create tidy dataframe for further analysis:
 ```python
from gamry.data import tidy_dataframe

tidy_df = tidy_dataframe(signals):
    """
    Args:
        signals (list): Signals.

    Returns:
        pandas.DataFrame: Tidy dataframe combining all signals.
    """
```

## Contact
If you would like to contact me, you can reach me at saravind@caltech.edu.