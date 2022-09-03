"""
Plotting functions for Gamry data.
"""

import itertools
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gamry.data import filter_signals

# 15 color colorblind friendly palette
COL_SEQ = itertools.cycle(["#000000",
                           "#004949",
                           "#009292",
                           "#ff6db6",
                           "#ffb6db",
                           "#490092",
                           "#006ddb",
                           "#b66dff",
                           "#6db6ff",
                           "#b6dbff",
                           "#920000",
                           "#924900",
                           "#db6d00",
                           "#24ff24",
                           "#ffff6d"])

UNITS = {'V':'V',
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

LAYOUT = dict(
    default=dict(
        font={"size": 12,},
        title={"font": {"size": 18,}},
        legend={"font": {"size": 12,}},
        width=1400,
        height=900,
        margin=dict(l=50, r=50, b=50, t=50)
    ),
    plain=dict(
        font={"size": 18, "color": "#000000"},
        title={"font": {"size": 24, "color": "#000000"}},
        legend={"font": {"size": 14, "color": "#000000"}},
        width=1400,
        height=900,
        margin=dict(l=50, r=50, b=50, t=50),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff"
    )
)

AXES = dict(
    default=dict(),
    plain=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        ticks='outside',
        ticklen=6,
        tickcolor='black',
        mirror=True,
        showgrid=True,
        gridcolor='#aaaaaa',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='#aaaaaa',
    )
)

def _set_layout(fig, layout):
    """Apply correct layout to plot.

    Args:
        fig (plotly.Figure): Figure to adjust.
        layout (str): Layout label.
    """

    fig.update_layout(**LAYOUT[layout])
    fig.update_xaxes(**AXES[layout])
    fig.update_yaxes(**AXES[layout])

def common_plot(signals, fig, x, y, hover_template, title, legend_title, signal_type, layout='default'):
    """General plot function that can be used by multiple signals.

    Args:
        signals (list): Signals.
        fig (pyplot.Figure): Figure to add signal plot to.
        x (str): Dataframe column for x values.
        y (str): Dataframe column for y values.
        hover_template (str): Hover text format.
        title (str): Plot title.
        legend_title (str): Legend title.
        signal_type (str): Type of signal to plot.
        layout (str, optional): Choose different layout format. Defaults to "default".
    """

    for signal in filter_signals(signals, signal_type=signal_type):
        signal.plot(x, y, fig, hover_template)

    _set_layout(fig, layout)
    fig.update_layout(
        legend_title_text=legend_title,
        title=title
    )


def eispot_bode(signals, title, legend_title, db=True, layout='default'):
    """Bode plot of EISPOT signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        db (bool, optional): Plot magnitude as dB. Defaults to True.
        layout (str, optional): Choose different layout format. Defaults to "default".
    """

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04)

    x = 'Freq'
    y1 = '|Z| dB' if db else '|Z|'
    y2 = 'Phase'

    hover_template1 = 'f = %{x:.3f} ' + UNITS[x] + '<br>|Z| = %{y:.1f}' + UNITS[y1]
    hover_template2 = 'f = %{x:.3f} ' + UNITS[x] + '<br>∠Z = %{y:.1f}' + UNITS[y2]

    # Plot both magnitude and phase in correct subplots in same legendgroup so they're connected
    for signal in filter_signals(signals, signal_type='EISPOT'):
        color = next(COL_SEQ)
        signal.plot(x, y1, fig, hover_template1, row=1, col=1, legendgroup=signal.label, color=color)
        signal.plot(x, y2, fig, hover_template2, row=2, col=1, legendgroup=signal.label, showlegend=False, color=color)

    fig.update_layout(
        legend_title_text=legend_title,
        title_text=title,
    )

    fig.update_xaxes(type='log', row=1, col=1)
    fig.update_xaxes(title_text="Frequency (" + UNITS[x] + ')', type='log', row=2, col=1)
    fig.update_yaxes(title_text="Phase (" + UNITS[y2] + ')', row=2, col=1)
    fig.update_yaxes(title_text="Magnitude (" + UNITS[y1] + ')', row=1, col=1)
    if not db:
        fig.update_yaxes(type='log', row=1, col=1)

    XAXES_EXTRA = dict(
        default=dict(),
        plain=dict(
            dtick=1,    # Only show numbers for powers of 10
            minor=dict(ticklen=6, tickcolor="black")
        )
    )

    fig.update_layout(**LAYOUT[layout])
    fig.update_xaxes(row=1, col=1, **AXES[layout], **XAXES_EXTRA[layout])
    fig.update_xaxes(row=2, col=1, **AXES[layout], **XAXES_EXTRA[layout])
    fig.update_yaxes(row=1, col=1, **AXES[layout])
    fig.update_yaxes(row=2, col=1, **AXES[layout])
    fig.show()

def eispot_mag(signals, title, legend_title, db=True, layout='default'):
    """Magnitude plot for EISPOT signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        db (bool, optional): Plot magnitude as dB. Defaults to True.
        layout (str, optional): Choose different layout format. Defaults to "default".
    """

    fig = go.Figure()
    x = 'Freq'
    y = '|Z| dB' if db else '|Z|'

    hover_template = 'f=%{x:.3f}' + UNITS[x] + '<br>|Z|=%{y:.1f}' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "EISPOT", layout)

    fig.update_xaxes(title_text="Freq (" + UNITS[x] + ')', type='log')
    fig.update_yaxes(title_text="|Z| (" + UNITS[y] + ')')
    if not db:
        fig.update_yaxes(type='log')
    fig.show()

def eispot_phase(signals, title, legend_title, layout='default'):
    """Phase plot for EISPOT signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        layout (str, optional): Choose different layout format. Defaults to "default".
    """

    fig = go.Figure()
    x = 'Freq'
    y = 'Phase'

    hover_template = 'f=%{x:.3f}' + UNITS[x] + '<br>|Z|=%{y:.1f}' + UNITS[y]

    for signal in filter_signals(signals, signal_type='EISPOT'):
        signal.plot(x, y, fig, hover_template)

    _set_layout(fig, layout)
    fig.update_layout(
        legend_title_text=legend_title,
        title=title
    )

    fig.update_xaxes(title_text="Frequency (" + UNITS[x] + ')', type='log')
    fig.update_yaxes(title_text="Phase (" + UNITS[y] + ')')
    fig.show()

def eispot_nyquist(signals, title, legend_title, layout='default'):
    """Nyquist plot for EISPOT signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        layout (str, optional): Choose different layout format. Defaults to "default".
    """

    fig = go.Figure()
    x = 'Re(Z)'
    y = 'Im(Z)'

    hover_template = 'Re(Z) = %{x:.3f} ' + UNITS[x] + '<br>Im(Z) = %{y:.1f} ' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "EISPOT", layout)

    fig.update_xaxes(title_text="Re(Z) (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Im(Z) (" + UNITS[y] + ')', scaleanchor='x', scaleratio=1)
    fig.show()

def eismon_mag(signals, title, legend_title, layout='default'):
    pass

def eismon_phase(signals, title, legend_title, layout='default'):
    pass

def cv(signals, title, legend_title, layout='default'):
    """Plot CV signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        layout (str, optional): Choose different layout format. Defaults to "default".
    """

    fig = go.Figure()
    x = 'V'
    y = 'I'

    hover_template = '%{text}<br>V = %{x:.3f} ' + UNITS[x] + '<br>I = %{y:.1f} ' + UNITS[y]

    # Plot each cycle of CV signal as separate trace connected using legendgroup so they're identifiable
    for signal in filter_signals(signals, signal_type='CV'):
        color = next(COL_SEQ)
        for curve in set(signal.df['Curve'].values):
            signal.plot(fig, curve, hover_template, color=color)

    _set_layout(fig, layout)
    fig.update_layout(
        legend_title_text=legend_title,
        title_text=title,
    )
    fig.update_xaxes(title_text="Voltage (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Current (" + UNITS[y] + ')')
    fig.show()

def cpc(signals, title, legend_title, layout='default'):
    """Plot CPC signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        layout (str, optional): Choose different layout format. Defaults to "default".
    """

    fig = go.Figure()
    x = 'Time'
    y = 'I'

    hover_template = 't=%{x:.3f}' + UNITS[x] + '<br>I=%{y:.1f}' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "CPC", layout)

    fig.update_xaxes(title_text="Time (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Current (" + UNITS[y] + ')')
    fig.show()
