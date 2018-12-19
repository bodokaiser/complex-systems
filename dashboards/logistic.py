import numpy as np

from dash import Dash
from dash.dependencies import Input, Output

import dash_html_components as html
import dash_core_components as core

from plotly import graph_objs as go

from dynamics import logistic_map


app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Logistic map'),

    html.Div(className='sliders-3', children=[
        html.Div(children=[
            html.Label(id='label-n', children='N'),
            core.Input(id='input-n', type='number',
                       inputmode='numeric', value=100, step=1)
        ]),
        html.Div(children=[
            html.Label(id='label-r', children='r'),
            core.Input(id='input-r', type='number',
                       inputmode='numeric', value=1.0, step=0.1)
        ]),
        html.Div(children=[
            html.Label(id='label-x0', children='x0'),
            core.Input(id='input-x0', type='number',
                       inputmode='numeric', value=1.0, step=0.1)
        ]),
    ]),

    html.Div(children=[
        core.Graph(id='graph')
    ])
])


@app.callback(Output('graph', 'figure'), [
    Input('input-x0', 'value'),
    Input('input-r', 'value'),
    Input('input-n', 'value')
])
def update_figure(x0, r, N):
  x = logistic_map(x0, r, N)
  n = np.arange(0, len(x))

  return go.Figure(
      data=[
          go.Scatter(x=n, y=x, mode='markers')
      ],
      layout=go.Layout(
          xaxis=dict(title='n'),
          yaxis=dict(title='x_n')
      )
  )


if __name__ == '__main__':
  app.run_server(debug=True)
