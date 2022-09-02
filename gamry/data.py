"""
Functions handling Gamry data.
"""

import os, re
import pandas as pd
from tkinter import Tk, filedialog
from pathlib import Path
from gamry.signal import EISPOT, EISMON, CV, CPC

def load_signals(folderpath=None, signal_type=None):
    """Read in signals from Gamry exported data.

    Args:
        folderpath (str, optional): Folder with signal files. Defaults to None.
        signal_type (str, optional): Signal type for filtering. Defaults to None.

    Returns:
        list: Signals.
    """

    # Option to not give folder and select it using GUI
    if not folderpath:
        root = Tk()
        root.withdraw()
        folderpath = Path(filedialog.askdirectory(title='Select signal folder'))

    filenames = get_filenames(folderpath)
    signals = []
    for filename in filenames:
        signal = create_signal(os.path.join(folderpath, filename), signal_type)
        if signal:
            signals.append(signal)

    return signals

def get_filenames(folderpath):
    """Filter Gamry files in folder.

    Args:
        folderpath (str): Folder to pull signal files from.

    Returns:
        list: Gamry signal filenames.
    """

    # Files that end with .DTA are Gamry signal files
    filename_list = []
    for filename in os.listdir(folderpath):
        if filename.endswith('.DTA'):
            filename_list.append(filename)

    return filename_list

def create_signal(filepath, signal_type=None):
    """Create proper signal object based on tag in signal file.

    Args:
        filepath (str): Signal file.
        signal_type (str, optional): Signal type for filtering. Defaults to None.

    Returns:
        signal object: Relevant signal project.
    """

    # Read tag in file to know signal type
    with open (filepath) as f:
        next(f)
        data_type = re.search(r'TAG\t(\w+)', next(f)).group(1)

    if signal_type:
        if data_type == signal_type:
            return _load_object(filepath, data_type)
    else:
        return _load_object(filepath, data_type)

def _load_object(filepath, data_type):
    """Load correct signal object depending on signal type.

    Args:
        filepath (str): Signal file.
        data_type (str): Signal type.

    Returns:
        Signal: Signal object.
    """
    if data_type == 'EISPOT':
        return EISPOT(filepath)
    elif data_type == 'EISMON':
        return EISMON(filepath)
    elif data_type == 'CV':
        return CV(filepath)
    elif data_type == 'CPC':
        return CPC(filepath)
    else:
        return None

def filter_signals(signals, signal_type=None, label=None, **param_filters):
    """Filter signals based on conditions.

    Args:
        signals (list): Signals.
        signal_type (str, optional): Signal type to filter. Defaults to None.
        label (str, optional): Signal label to filter. Defaults to None.
        **param_filters: Arbitrary keyword arguments to filter params.

    Returns:
        list: Filtered signals.
    """

    filtered = []

    # Skip adding files to list if doesn't meet provided conditions.
    for signal in signals:
        if signal_type:
            if not signal.type == signal_type:
                continue

        if label:
            if not label in signal.label:
                continue

        if param_filters:
            for key, val in param_filters.items():
                if key in signal.params.keys():
                    if not signal.params[key] == val:
                        continue
                else:
                    continue

        filtered.append(signal)

    return filtered

def convert_zview(signals):
    """Generate EISPOT files that are compatible with ZView.

    Args:
        signals (list): Signals.
    """

    folder = Path(Path().absolute() / 'ZView')
    folder.mkdir(parents=True, exist_ok=True)

    for signal in filter_signals(signals, 'EISPOT'):
        signal.df[['Freq', 'Re(Z)', 'Im(Z)']].to_csv(
            folder / (signal.label + '.txt'),
            sep='\t',
            index=None,
            header=False
        )

def tidy_dataframe(signals):
    """Create tidy dataframe from list of signals.

    Args:
        signals (list): Signals.

    Returns:
        pandas.DataFrame: Tidy dataframe combining all signals.
    """

    tidy_df = pd.DataFrame()

    for signal in signals:
        df = signal.df

        # Add label, type and params as own columns
        df['Label'] = signal.label
        df['Type'] = signal.type
        for key, val in signal.params.items():
            df[key] = val

        tidy_df = pd.concat([tidy_df, df], ignore_index=True)

    return tidy_df
