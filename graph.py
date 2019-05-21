import plotly as py
import plotly.graph_objs as go
import numpy as np
import webview
# import ipywidgets as widgets
# from scipy import special

x = np.linspace(0, np.pi, 10)

layout = go.Layout(
    # title='SIMPLE EXAMPLE',
    yaxis=dict(
        title='volts'
    ),
    xaxis=dict(
        title='nanoseconds'
    )
)

trace1 = go.Scatter(
    x=x,
    y=np.sin(x),
    mode='lines',
    name='sin(x)',
    line=dict(
        shape='spline'
    )
)


fig = go.Figure(data=[trace1], layout=layout)
# py.offline.plot(fig)

config = {
    'displayModeBar': False,
    'scrollZoom': False,
    'editable': False
}

py.offline.plot(fig, filename='graph.html', auto_open=False,
                config=config)
webview.create_window('Look at this graph', 'graph.html')


# div = py.offline.plot(fig, include_plotlyjs=False,
#                       output_type='div', config=config)
# print(div)
