"""
Plotting functions for Gamry data.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gamry.data import filter_signals
from gamry.units import UNITS
from gamry.theme import set_theme, COL_SEQ

def common_plot(signals, fig, x, y, hover_template, title, legend_title, signal_type, name=None, theme='default', mode='lines+markers'):
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
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".
        mode (str, optional): Plot trace mode. Defaults to "lines+markers".
    """

    for signal in filter_signals(signals, signal_type=signal_type):
        signal.plot(x, y, fig, hover_template, name=name, mode=mode)

    set_theme(fig, theme)
    fig.update_layout(
        legend_title_text=legend_title,
        title=title
    )


def eispot_bode(signals, title, legend_title, db=True, name=None, theme='default'):
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

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04)

    x = 'Freq'
    y1 = '|Z| dB' if db else '|Z|'
    y2 = 'Phase'

    hover_template1 = 'f = %{x:.3f} ' + UNITS[x] + '<br>|Z| = %{y:.1f} ' + UNITS[y1]
    hover_template2 = 'f = %{x:.3f} ' + UNITS[x] + '<br>∠Z = %{y:.1f}' + UNITS[y2]

    # Plot both magnitude and phase in correct subplots in same legendgroup so they're connected
    for signal in filter_signals(signals, signal_type='EISPOT'):
        # Set name of trace to label or param value
        if not name:
            name_val = signal.label
        else:
            name_val = str(signal.params[name.lower()])

        color = next(COL_SEQ)
        signal.plot(x, y1, fig, hover_template1, row=1, col=1, legendgroup=name_val, color=color)
        signal.plot(x, y2, fig, hover_template2, row=2, col=1, legendgroup=name_val, showlegend=False, color=color)

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
        default=dict(
        ),
        plain=dict(
            dtick=1,    # Only show numbers for powers of 10
            minor=dict(ticklen=6, tickcolor="black")
        )
    )

    set_theme(fig, theme)
    fig.update_xaxes(**XAXES_EXTRA.get(theme.lower()))

    return fig

def eispot_mag(signals, title, legend_title, db=True, name=None, theme='default'):
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

    fig = go.Figure()
    x = 'Freq'
    y = '|Z| dB' if db else '|Z|'

    hover_template = 'f = %{x:.3f}' + UNITS[x] + '<br>|Z| = %{y:.1f} ' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "EISPOT", name=name, theme=theme)

    XAXES_EXTRA = dict(
        default=dict(
        ),
        plain=dict(
            dtick=1,    # Only show numbers for powers of 10
            minor=dict(ticklen=6, tickcolor="black")
        )
    )
    fig.update_xaxes(**XAXES_EXTRA.get(theme.lower()))

    fig.update_xaxes(title_text="Frequency (" + UNITS[x] + ')', type='log')
    fig.update_yaxes(title_text="Magnitude (" + UNITS[y] + ')')
    if not db:
        fig.update_yaxes(type='log')

    return fig

def eispot_phase(signals, title, legend_title, name=None, theme='default'):
    """Phase plot for EISPOT signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure.
    """

    fig = go.Figure()
    x = 'Freq'
    y = 'Phase'

    hover_template = 'f = %{x:.3f}' + UNITS[x] + '<br>∠Z = %{y:.1f}' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "EISPOT", name=name, theme=theme)

    set_theme(fig, theme)
    fig.update_layout(
        legend_title_text=legend_title,
        title=title
    )

    fig.update_xaxes(title_text="Frequency (" + UNITS[x] + ')', type='log')
    fig.update_yaxes(title_text="Phase (" + UNITS[y] + ')')

    return fig

def eispot_nyquist(signals, title, legend_title, name=None, theme='default'):
    """Nyquist plot for EISPOT signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure.
    """

    fig = go.Figure()
    x = 'Re(Z)'
    y = 'Im(Z)'

    hover_template = 'Re(Z) = %{x:.3f} ' + UNITS[x] + '<br>Im(Z) = %{y:.1f} ' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "EISPOT", name=name, theme=theme)

    fig.update_xaxes(title_text="Real Impedance (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Imaginary Impedance (" + UNITS[y] + ')', scaleanchor='x', scaleratio=1)

    return fig

def eismon_mag(signals, title, legend_title, name=None, theme='default'):
    """Magnitude plot for EISMON signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure.
    """

    fig = go.Figure()
    x = 'Time'
    y = '|Z|'

    hover_template = 't = %{x:.3f} ' + UNITS[x] + '<br>|Z| = %{y:.1f} ' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "EISPOT", name=name, theme=theme)

    fig.update_xaxes(title_text="Time (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Magnitude (" + UNITS[y] + ')')

    return fig

def eismon_phase(signals, title, legend_title, name=None, theme='default'):
    """Phase plot for EISMON signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure.
    """

    fig = go.Figure()
    x = 'Time'
    y = 'Phase'

    hover_template = 't = %{x:.3f} ' + UNITS[x] + '<br>∠Z = %{y:.1f}' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "EISPOT", name=name, theme=theme)

    fig.update_xaxes(title_text="Time (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Phase (" + UNITS[y] + ')')

    return fig

def cv(signals, title, legend_title, name=None, theme='default'):
    """Plot CV signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure.
    """

    fig = go.Figure()
    x = 'V'
    y = 'I'

    hover_template = '%{text}<br>V = %{x:.3f} ' + UNITS[x] + '<br>I = %{y:.1f} ' + UNITS[y]

    # Plot each cycle of CV signal as separate trace connected using legendgroup so they're identifiable
    for signal in filter_signals(signals, signal_type='CV'):
        color = next(COL_SEQ)
        for curve in set(signal.df['Curve'].values):
            signal.plot(fig, curve, hover_template, name=name, color=color)

    set_theme(fig, theme)
    fig.update_layout(
        legend_title_text=legend_title,
        title_text=title,
    )
    fig.update_xaxes(title_text="Voltage (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Current (" + UNITS[y] + ')')

    return fig

def cpc(signals, title, legend_title, name=None, theme='default'):
    """Plot CPC signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure.
    """

    fig = go.Figure()
    x = 'Time'
    y = 'I'

    hover_template = 't = %{x:.3f} ' + UNITS[x] + '<br>I = %{y:.1f} ' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "CPC", name=name, theme=theme)

    fig.update_xaxes(title_text="Time (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Current (" + UNITS[y] + ')')

    return fig

def chronoa(signals, title, legend_title, name=None, theme='default'):
    """Plot CHRONOA signals.

    Args:
        signals (list): Signals.
        title (str): Plot title.
        legend_title (str): Legend title.
        name (str, optional): Param key to get label for trace. Defaults to None.
        theme (str, optional): Plot theme. Defaults to "default".

    Returns:
        plotly.graph_objects.Figure: Plot figure.
    """

    fig = go.Figure()
    x = 'Time'
    y = 'I'

    hover_template = 't = %{x:.3f} ' + UNITS[x] + '<br>I = %{y:.1f} ' + UNITS[y]

    common_plot(signals, fig, x, y, hover_template, title, legend_title, "CHRONOA", name=name, theme=theme, mode='lines')

    fig.update_xaxes(title_text="Time (" + UNITS[x] + ')')
    fig.update_yaxes(title_text="Current (" + UNITS[y] + ')')

    return fig
