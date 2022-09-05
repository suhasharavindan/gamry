"""
Parent signal object with children for each test type.
"""

import re
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import plotly.graph_objects as go
from gamry.units import factor_conversion

def find_skiplines(filepath, search_str):
    """Find first line of data.

    Args:
        filepath (str): Signal file.
        search_str (str): Search term to determine where start of data is.

    Returns:
        int: Row to skip file until.
    """

    cnt = 1
    with open(filepath) as f:
        for line in f:
            if re.match(search_str, line):
                break
            cnt += 1
    return cnt

class Signal:
    """Parent signal object."""

    def __init__(self, signal_type, filepath):
        """Initialize parent signal object.

        Args:
            signal_type (str): Signal type.
            filepath (str): Signal file.
        """

        self.type = signal_type
        self.df = None
        self._area = None
        self.label = None
        self.params = {} # Holds arbitrary parameters that are saved in the file notes

        self._read_note(filepath)
        self._update_attributes(filepath)

    @property
    def area(self):
        """Electrode area.

        Returns:
            float: Area in cm2.
        """
        return self._area

    @area.setter
    def area(self, value):
        """Sets electrode area.

        Args:
            value (float): Area in cm2.
        """
        self._area = value

    def _read_data(self, filepath, skip_lines=None, skip_list=None):
        """Read data from signal file.

        Args:
            filepath (str): Signal file.
            skip_lines (int, optional): Skip file until this line. Defaults to None.
            skip_list (list, optional): Pre-calculated lines to skip. Defaults to None.
        """

        if skip_lines:
            skip_list = list(range(skip_lines))
            skip_list.append(skip_lines + 1)

        self.df = pd.read_csv(filepath, sep='\t', header=[0], skiprows=skip_list, encoding='cp1252')
        self._clean_df()

    def _clean_df(self):
        """Clean up dataframe by dropping and rename columns."""

        self.df = self.df.drop(columns=['Unnamed: 0', 'Pt', 'IERange', 'Over'], errors='ignore')
        self.df = self.df.rename(columns={'Zphz':'Phase',
                                          'Zimag':'Im(Z)',
                                          'Zreal':'Re(Z)',
                                          'Zmod':'|Z|',
                                          'T':'Time',
                                          'Vf':'E',
                                          'Im':'I'}, errors='ignore')

    def _read_note(self, filepath):
        """Read signal file for any notes to add to params.

        Args:
            filepath (str): Signal file.
        """

        with open(filepath) as f:

            # Start reading file from 7th line
            for _ in range(6):
                next(f)

            # Loop and collect parameters
            line = f.readline()

            if not line.strip() == '':
                key, val = [i.strip() for i in line.split(':')]
                self.params[key.lower()] = val

                for line in f:
                    # Stop looping on first line without parameter
                    if line.startswith('PSTAT'):
                        break
                    key, val = [i.strip() for i in line.split(':')]
                    self.params[key.lower()] = val

        self._clean_params()


    def _clean_params(self):
        """Converts numbers and corrects units in param values."""

        for key, val in self.params.items():
            if converted_num := factor_conversion(val):
                self.params[key] = converted_num


    def _update_attributes(self, filepath):
        """Update object attributes to have default values if none are provided in signal file note.

        Args:
            filepath (str): Signal file.
        """

        if 'label' in self.params:
            self.label = self.params['label']
        else:
            re_res = re.search(r'\\([^\\]+).DTA', filepath) # Take filename as label
            self.label = re_res.group(1)

        if 'area' in self.params:
            self._area = self.params['area']
        else:
            if 'radius' in self.params:
                self._area = np.pi * self.params['radius'] ** 2
            elif 'diameter' in self.params:
                self._area = np.pi * (self.params['diameter'] / 2) ** 2
            else:
                self._area = np.pi * (0.05 ** 2) # Assumes 1mm diameter electrode


    def plot(self, x, y, fig, hover_template, row=None, col=None, legendgroup=None, showlegend=True, color=None, mode='lines+markers'):
        """Plot signal with option for subplots.

        Args:
            x (str): Dataframe column for x values.
            y (str): Dataframe column for y values.
            fig (plotly.Figure): Figure to add signal to.
            hover_template (str): Hover text format.
            row (int, optional): Subplot row. Defaults to None.
            col (int, optional): Subplot column. Defaults to None.
            legendgroup (str, optional): Name of legend group. Defaults to None.
            showlegend (bool, optional): Option to show legend. Defaults to True.
            color (str, optional): Signal plot color. Defaults to None.
        """

        if row and col:
            fig.add_trace(go.Scatter(
                x=self.df[x],
                y=self.df[y],
                mode=mode,
                name=self.label,
                hovertemplate=hover_template,
                legendgroup=legendgroup,
                showlegend=showlegend,
                line=dict(color=color)), row=row, col=col)
        else:
            fig.add_trace(go.Scatter(
                x=self.df[x],
                y=self.df[y],
                mode=mode,
                name=self.label,
                hovertemplate=hover_template))

class EISPOT(Signal):
    """Potentiometric EIS signal.

    Args:
        Signal (Signal): Parent signal object.
    """

    def __init__(self, filepath):
        """Initialize EISPOT object.

        Args:
            filepath (str): Signal file.
        """

        super().__init__("EISPOT", filepath)
        skip_lines = find_skiplines(filepath, 'ZCURVE')
        super()._read_data(filepath, skip_lines)

        self.rs = self.df['|Z|'].min() # Series resistance
        self.df['|Z| dB'] = 20 * np.log10(self.df['|Z|'] / self.rs)

        self.db_corner_params = self._set_db_corner_freq()
        self.phase_corner_params = self._set_phase_corner_frequency()

    @Signal.area.setter
    def area(self, value):
        """Sets area and recalculates corner frequencies.

        Args:
            value (float): Area in cm2.
        """
        self._area = value
        self._set_db_corner_freq()
        self._set_phase_corner_frequency()

    def _set_db_corner_freq(self):
        """Calculate corner frequency using 3dB point.

        Returns:
            dict: Corner frequency properties.
        """

        # Use interpolation to find value.
        f = interp1d(self.df['|Z| dB'], self.df['Freq'])
        try:
            corner_freq = f(3)
            cap = 1 / (2*np.pi*self.rs*corner_freq)
            cap_area = cap / self._area
            factor = cap_area / 20E-6 # F/cm2
        except ValueError:
            corner_freq = None
            cap = None
            cap_area = None
            factor = None

        return {'freq':corner_freq,
                'cap':cap,
                'cap/area':cap_area,
                'factor':factor}


    def _set_phase_corner_frequency(self):
        """Calculate corner frequency using 45 degree point.

        Returns:
            dict: Corner frequency properties.
        """

        # User interpolation to find value.
        f = interp1d(self.df['Phase'], self.df['Freq'])
        try:
            corner_freq = f(-45)
            cap = 1 / (2*np.pi*self.rs*corner_freq)
            cap_area = cap / self._area
            factor = cap_area / 20E-6 # F/cm2
        except ValueError:
            corner_freq = None
            cap = None
            cap_area = None
            factor = None

        return {'freq':corner_freq,
                'cap':cap,
                'cap/area':cap_area,
                'factor':factor}


class EISMON(Signal):
    """Single frequency EIS signal object.

    Args:
        Signal (Signal): Parent signal object.
    """

    def __init__(self, filepath):
        """Initialize EISMON object.

        Args:
            filepath (str): Signal file.
        """

        super().__init__("EISMON", filepath)

        skip_lines = find_skiplines(filepath, 'ZCURVE')
        super()._read_data(filepath, skip_lines)


class CV(Signal):
    """Cyclic voltammetry signal object.

    Args:
        Signal (Signal): Parent signal object.
    """

    def __init__(self, filepath):
        """Initialize CV object.

        Args:
            filepath (str): Signal file.
        """

        super().__init__("CV", filepath)
        self._read_data(filepath)

    def find_skiplines(self, filepath):
        """Determine lines to skip in file.

        Args:
            filepath (str): Signal file.
        """

        cnt = 1
        curve_num = 1
        skip_list = []
        search_str = 'CURVE' + str(curve_num)

        # Break apart each cycle and get the corresponding rows
        with open(filepath) as f:
            for line in f:
                if search_str in line:
                    skip_list.append(cnt)
                    curve_num += 1
                    search_str = 'CURVE' + str(curve_num)
                cnt += 1

        skip_list.append(cnt) # Inlcude end of file
        return skip_list

    def _read_data(self, filepath):
        """Read data from file.

        Args:
            filepath (str): Signal file.
        """

        skip_rows = self.find_skiplines(filepath)
        df_list = []

        # Read data between rows found in find_skiplines
        for idx, row in enumerate(skip_rows[:-1]):
            skip_list = list(range(row))
            skip_list.append(row + 1)
            skip_list += list(range(skip_rows[idx+1], skip_rows[-1]))
            super()._read_data(filepath, None, skip_list)

            # Include extra column specifying cycle number
            self.df['Curve'] = idx + 1
            df_list.append(self.df)

        # Combine all separate curves into one dataframe
        self.df = pd.concat(df_list)
        self._clean_df()
        self.df['I'] = 1E6 * self.df['I']

    def plot(self, fig, curve, hover_template, color=None):
        """Plot CV signal.

        Args:
            fig (plotly.Figure): Figure to add plot trace to.
            curve (int): CV cycle number.
            hover_template (str): Hover text format.
            color (str, optional): Plot trace color. Defaults to None.
        """

        show_legend = True if curve == 1 else False

        # Plot specific curve
        fig.add_trace(go.Scatter(x=self.df[self.df['Curve'] == curve]['E'],
                                 y=self.df[self.df['Curve'] == curve]['I'],
                                 mode='lines',
                                 legendgroup=self.label,
                                 name=self.label,
                                 text=['Curve ' + str(curve)] * len(self.df[self.df['Curve'] == curve]['E'].values),
                                 hovertemplate=hover_template,
                                 line=dict(color=color),
                                 showlegend=show_legend))


class CPC(Signal):
    """Controlled potential coulometry signal object.

    Args:
        Signal (Signal): Parent signal object.
    """

    def __init__(self, filepath):
        """Initialize CPC object.

        Args:
            filepath (str): Signal file.
        """

        super().__init__("CPC", filepath)

        skip_lines = find_skiplines(filepath, 'CURVE')
        self._read_data(filepath, skip_lines)

        self.df['I'] = 1E6 * self.df['I']


class CHRONOA(Signal):
    """Chronoamperometry signal object.

    Args:
        Signal (Signal): Parent signal object.
    """

    def __init__(self, filepath):
        """Initialize CHRONOA object.

        Args:
            filepath (str): Signal file.
        """

        super().__init__("CHRONOA", filepath)

        skip_lines = find_skiplines(filepath, "CURVE")
        self._read_data(filepath, skip_lines)

        self.df['I'] = 1E6 * self.df['I']
