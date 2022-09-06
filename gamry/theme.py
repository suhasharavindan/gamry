"""
Functions and constants related to plotting themes.
"""

import itertools

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

def set_theme(fig, theme):
    """Apply correct layout to plot.

    Args:
        fig (plotly.Figure): Figure to adjust.
        theme (str): Layout label.
    """

    fig.update_layout(**LAYOUT[theme])
    fig.update_xaxes(**AXES[theme])
    fig.update_yaxes(**AXES[theme])
