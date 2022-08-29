"""
Functions handling Gamry data.
"""

import os, re
from tkinter import Tk, filedialog
from pathlib import Path
from gamry.signal import EISPOT, EISMON, CV, CPC

def load_signals(folderpath=None):
    # Option to not give folder and select it using GUI
    if not folderpath:
        root = Tk()
        root.withdraw()
        folderpath = Path(filedialog.askdirectory(title = 'Select signal folder'))
    filenames = get_filenames(folderpath)
    signals = []

    for filename in filenames:
        signal = create_signal(os.path.join(folderpath, filename))
        if signal:
            signals.append(signal)

    return signals

def get_filenames(folderpath):
    filename_list = []
    for filename in os.listdir(folderpath):
        if filename.endswith('.DTA'):
            filename_list.append(filename)

    return filename_list

def create_signal(filepath):
    with open (filepath) as f:
        next(f)
        data_type = re.search(r'TAG\t(\w+)', next(f)).group(1)

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

def filter_signals(signals, signal_type=None, label=None, **kwargs):
    filtered = []

    for signal in signals:
        if signal_type:
            if not signal.type == signal_type:
                continue

        if label:
            if not label in signal.label:
                continue

        if kwargs:
            for key, val in kwargs.items():
                if not signal.params[key] == val:
                    continue

        filtered.append(signal)

    return filtered
