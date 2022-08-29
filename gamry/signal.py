"""
Parent signal object with children for each test type.
"""

import re
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import plotly.graph_objects as go

class Signal:
    def __init__(self, signal_type, filepath):
        self.type = signal_type
        self.df = None
        self.area = None
        self.label = None
        self.params = {} # Holds parameters like diameter, area, etc

        self._read_note(filepath)
        self._update_attributes(filepath)


    def _read_data(self, filepath, skip_lines=None, skip_list=None):

        if skip_lines:
            skip_list = list(range(skip_lines))
            skip_list.append(skip_lines + 1)

        self.df = pd.read_csv(filepath, sep='\t', header=[0], skiprows=skip_list, encoding='cp1252')
        self._clean_df()

    def _clean_df(self):
        self.df = self.df.drop(columns=['Unnamed: 0', 'Pt', 'IERange', 'Over'], errors='ignore')
        self.df = self.df.rename(columns={'Zphz':'Phase',
                                          'Zimag':'Im(Z)',
                                          'Zreal':'Re(Z)',
                                          'Zmod':'|Z|',
                                          'T':'Time',
                                          'Vf':'E',
                                          'Im':'I'}, errors='ignore')


    def _find_skiplines(self, filepath, search_str):

        cnt = 1
        with open(filepath) as f:
            for line in f:
                if search_str in line:
                    break
                cnt += 1
        return cnt

    def _read_note(self, filepath):

        with open(filepath) as f:
            for _ in range(6):
                next(f)

            line = f.readline()

            if not line.strip() == '':
                key, val = [i.strip() for i in line.split(':')]
                self.params[key.lower()] = val

                for line in f:
                    if line.startswith('PSTAT'):
                        break
                    key, val = [i.strip() for i in line.split(':')]
                    self.params[key.lower()] = val


    def _update_attributes(self, filepath):
        if 'label' in self.params:
            self.label = self.params['label']
        else:
            re_res = re.search(r'\\([^\\]+).DTA', filepath) # take filename as label
            self.label = re_res.group(1)

        if 'area' in self.params:
            self.area = self.params['area'] # has to be given in cm2
        else:
            self.area = np.pi * (0.05 ** 2) # assumes 1mm diameter electrode


    def plot(self, x, y, fig, hover_template, row=None, col=None, legendgroup=None, showlegend=True, color=None):
        if row and col:
            fig.add_trace(go.Scatter(x=self.df[x], y=self.df[y], mode='lines+markers', name=self.label, hovertemplate=hover_template, legendgroup=legendgroup, showlegend=showlegend, line=dict(color=color)), row=row, col=col)
        else:
            fig.add_trace(go.Scatter(x=self.df[x], y=self.df[y], mode='lines+markers', name=self.label, hovertemplate=hover_template))

class EISPOT(Signal):
    def __init__(self, filepath):
        super().__init__("EISPOT", filepath)
        self.rs = None
        self._read_data(filepath)

        self.db_corner_params = self._set_db_corner_freq()
        self.phase_corner_params = self._set_phase_corner_frequency()


    def _read_data(self, filepath):
        # Skip rows before header and one after header containing units
        skip_lines = super()._find_skiplines(filepath, 'ZCURVE')
        super()._read_data(filepath, skip_lines)

        self.rs = self.df['|Z|'].min()
        self.df['|Z| dB'] = 20 * np.log10(self.df['|Z|'] / self.rs)


    def _set_db_corner_freq(self):
        f = interp1d(self.df['|Z| dB'], self.df['Freq'])
        try:
            corner_freq = f(3)
            cap = 1 / (2*np.pi*self.rs*corner_freq)
            cap_area = cap / self.area
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
        f = interp1d(self.df['Phase'], self.df['Freq'])
        try:
            corner_freq = f(-45)
            cap = 1 / (2*np.pi*self.rs*corner_freq)
            cap_area = cap / self.area
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
    def __init__(self, filepath):
        super().__init__("EISMON", filepath)
        self._read_data(filepath)


    def _read_data(self, filepath):
        # Skip rows before header and one after header containing units
        skip_lines = super()._find_skiplines(filepath, 'ZCURVE')
        super()._read_data(filepath, skip_lines)


class CV(Signal):
    def __init__(self, filepath):
        super().__init__("CV", filepath)
        self._read_data(filepath)

    def _find_skiplines(self, filepath):
        cnt = 1
        curve_num = 1
        skip_list = []
        search_str = 'CURVE' + str(curve_num)

        with open(filepath) as f:
            for line in f:
                if search_str in line:
                    skip_list.append(cnt)
                    curve_num += 1
                    search_str = 'CURVE' + str(curve_num)
                cnt += 1

        skip_list.append(cnt)
        return skip_list

    def _read_data(self, filepath):

        skip_rows = self._find_skiplines(filepath)
        self.df_list = []

        for idx, row in enumerate(skip_rows[:-1]):
            skip_list = list(range(row))
            skip_list.append(row + 1)
            skip_list += list(range(skip_rows[idx+1], skip_rows[-1]))

            super()._read_data(filepath, None, skip_list)
            self.df['Curve'] = idx + 1
            self.df_list.append(self.df)

        self.df = pd.concat(self.df_list)
        self._clean_df()
        self.df['I'] = 1E6 * self.df['I']

    def plot(self, fig, curve, hover_template, color=None):

        show_legend = True if curve == 1 else False

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
    def __init__(self, filepath):
        super().__init__("CPC", filepath)
        self._read_data(filepath)

    def _read_data(self, filepath):
        skip_lines = super()._find_skiplines(filepath, 'CURVE')
        super()._read_data(filepath, skip_lines)

        self.df['I'] = 1E6 * self.df['I']
