"""
Plotting functions for Gamry data.
"""

import itertools
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

COL_SEQ = itertools.cycle(px.colors.qualitative.Alphabet)

UNITS = {'E':'V',
         'I':'μA',
         'Q':'C',
         'Scan Rate':'mV/s',
         'Phase':'°',
         'Im(Z)':'Ω',
         'Re(Z)':'Ω',
         '|Z|':'Ω',
         '|Z| dB': 'dB',
         'Freq':'Hz',
         'Time':'s',
         'Plating Voltage':'V',
         'Plating Time':'min',
         'Plating Freq':'Hz',
         'Plating Duty Cycle':'%'}

def common_plot(signals, fig, x, y, hover_template, title, legend_title, signal_type):
    for signal in signals:
        if signal.type == signal_type:
            signal.plot(x, y, fig, hover_template)

    if legend_title == 'Sample':
        legend_title_text = legend_title
    else:
        legend_title_text = legend_title + ' (' + UNITS[legend_title] + ')'

    fig.update_layout(
        width=1400,
        height=700,
        legend_title_text=legend_title_text,
        margin=dict(l=50, r=50, b=50, t=50),
        title=title
    )

def eispot_bode(signals, title, legend_title, db=True):

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    x = 'Freq'
    y1 = '|Z| dB' if db else '|Z|'
    y2 = 'Phase'

    hover_template1 = 'f = %{x:.3f} ' + UNITS[x] + '<br>|Z| = %{y:.1f}' + UNITS[y1]
    hover_template2 = 'f = %{x:.3f} ' + UNITS[x] + ',<br>∠Z = %{y:.1f}' + UNITS[y2]

    for signal in signals:
        if signal.type == "EISPOT":
            color = next(COL_SEQ)
            signal.plot(x, y1, fig, hover_template1, row=1, col=1, legendgroup=signal.label, color=color)
            signal.plot(x, y2, fig, hover_template2, row=2, col=1, legendgroup=signal.label, showlegend=False, color=color)

    if legend_title == 'Sample':
        legend_title_text = legend_title
    else:
        legend_title_text = legend_title + ' (' + UNITS[legend_title] + ')'

    fig.update_layout(
        width=1400,
        height=900,
        legend_title_text=legend_title_text,
        margin=dict(l=50, r=50, b=50, t=50),
        title_text=title
    )

    fig.update_xaxes(type='log', row=1, col=1)
    fig.update_xaxes(title_text="Frequency (" + UNITS[x] + ')', type='log', row=2, col=1)
    fig.update_yaxes(title_text="Phase (" + UNITS[y2] + ')', row=2, col=1)
    if db:
        fig.update_yaxes(title_text="Magnitude (" + UNITS[y1] + ')', row=1, col=1)
    else:
        fig.update_yaxes(title_text="Magnitude (" + UNITS[y1] + ')', type='log', row=1, col=1)
    fig.show()

def eispot_mag(signals, title, legend_title, db=True):

    fig = go.Figure()
    x = 'Freq'
    y = '|Z| dB' if db else '|Z|'

    hover_template = 'f=%{x:.3f}' + UNITS[x] + ', |Z|=%{y:.1f}' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "EISPOT")

    fig.update_xaxes(title_text="Freq (" + UNITS[x] + ')', type='log')
    if db:
        fig.update_yaxes(title_text="|Z| (" + UNITS[y] + ')')
    else:
        fig.update_yaxes(title_text="|Z| (" + UNITS[y] + ')', type='log')
    fig.show()

def eispot_phase(signals, title, legend_title):

    fig = go.Figure()
    x = 'Freq'
    y = 'Phase'

    hover_template = 'f=%{x:.3f}' + UNITS[x] + ', |Z|=%{y:.1f}' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "EISPOT")

    fig.update_xaxes(title_text="Frequency (" + UNITS[x] + ')', type='log')
    fig.update_yaxes(title_text="Phase (" + UNITS[y] + ')')
    fig.show()

def eismon_mag(signals, title, legend_title):
    pass

def eismon_phase(signals, title, legend_title):
    pass

def cv(signals, title, legend_title):
    fig = go.Figure()
    x = 'E'
    y = 'I'

    hover_template = '%{text}<br>V = %{x:.3f} ' + UNITS[x] + '<br>I = %{y:.1f} ' + UNITS[y]

    for signal in signals:
        if signal.type == "CV":
            color = next(COL_SEQ)
            for curve in set(signal.df['Curve'].values):
                signal.plot(fig, curve, hover_template, color=color)

    if legend_title == 'Sample':
        legend_title_text = legend_title
    else:
        legend_title_text = legend_title + '( ' + UNITS[legend_title] + ')'

    fig.update_layout(
        width=1400,
        height=900,
        legend_title_text=legend_title_text,
        margin=dict(l=50, r=50, b=50, t=50),
        title_text=title
    )

    fig.update_xaxes(title_text="Voltage (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Current (" + UNITS[y] + ')')
    fig.show()

def cpc(signals, title, legend_title):
    fig = go.Figure()
    x = 'Time'
    y = 'I'

    hover_template = 'f=%{x:.3f}' + UNITS[x] + ', |Z|=%{y:.1f}' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "CPC")

    fig.update_xaxes(title_text="Time (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Current (" + UNITS[y] + ')')
    fig.show()
