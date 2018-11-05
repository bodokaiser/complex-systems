from dash.dependencies import Input, Output

import dash_html_components as html
import dash_core_components as core

from plotly import graph_objs as go

from dynamic import roessler_naive
from dynamic import roessler_rk4

layout = html.Div(children=[
    html.H1(children='Roessler dynamics'),

    html.Div(className='sliders-5', children=[
        html.Div(children=[
            html.Label(id='roessler-label-n'),
            core.Slider(id='roessler-slider-n', included=False, min=1,
                        max=10000, step=1, value=1000),
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-impl', children='Implementation'),
            core.Dropdown(id='roessler-option-impl', options=[
                {'label': 'Naive', 'value': 'naive'},
                {'label': '4th order Runge Kutta', 'value': 'rk4'}
            ], value='naive')
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-x0', children='X0'),
            core.Input(id='roessler-input-x0', type='number',
                       inputmode='numeric', value=1.0, step=0.1)
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-y0', children='Y0'),
            core.Input(id='roessler-input-y0', type='number',
                       inputmode='numeric', value=1.0, step=0.1)
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-z0', children='Z0'),
            core.Input(id='roessler-input-z0', type='number',
                       inputmode='numeric', value=1.0, step=0.1)
        ])
    ]),

    html.Div(children=[
        core.Graph(id='roessler-graph')
    ]),

    html.Div(className='sliders-4', children=[
        html.Div(children=[
            html.Label(id='roessler-label-a'),
            core.Slider(id='roessler-slider-a', included=False, min=-1.0,
                        max=1.0, step=0.01, value=0.0),
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-b'),
            core.Slider(id='roessler-slider-b', included=False, min=-1.0,
                        max=1.0, step=0.01, value=0.0)
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-c'),
            core.Slider(id='roessler-slider-c', included=False, min=-1.0,
                        max=1.0, step=0.01, value=0.0)
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-h'),
            core.Slider(id='roessler-slider-h', included=False,
                        min=1e-6, max=1e-3, step=1e-6, value=1e-6)
        ])
    ])
])


def update_label_n(value):
  return f'N = {value}'


def update_label_h(value):
  return f'Δt = {value}'


def update_label_a(value):
  return f'a = {value}'


def update_label_b(value):
  return f'b = {value}'


def update_label_c(value):
  return f'c = {value}'


def update_label_d(value):
  return f'd = {value}'


def update_figure(x0, y0, z0, a, b, c, N, h, impl):
  if impl == 'naive':
    x, y, z = roessler_naive(x0, y0, z0, a, b, c, N, h)
  if impl == 'rk4':
    x, y, z = roessler_rk4(x0, y0, z0, a, b, c, N, h)

  return {
      'data': [
          go.Scatter3d(x=x, y=y, z=y, mode='markers',
                       marker=dict(color='#444'))
      ],
      'layout': {
          'xaxis': {'title': 'x'},
          'yaxis': {'title': 'y'},
          'zaxis': {'title': 'z'}
      }
  }


def connect(app):
  app.callback(Output('roessler-label-n', 'children'), [
      Input('roessler-slider-n', 'value')
  ])(update_label_n)

  app.callback(Output('roessler-label-h', 'children'), [
      Input('roessler-slider-h', 'value')
  ])(update_label_h)

  app.callback(Output('roessler-label-a', 'children'), [
      Input('roessler-slider-a', 'value')
  ])(update_label_a)

  app.callback(Output('roessler-label-b', 'children'), [
      Input('roessler-slider-b', 'value')
  ])(update_label_b)

  app.callback(Output('roessler-label-c', 'children'), [
      Input('roessler-slider-c', 'value')
  ])(update_label_c)

  app.callback(Output('roessler-graph', 'figure'), [
      Input('roessler-input-x0', 'value'),
      Input('roessler-input-y0', 'value'),
      Input('roessler-input-z0', 'value'),
      Input('roessler-slider-a', 'value'),
      Input('roessler-slider-b', 'value'),
      Input('roessler-slider-c', 'value'),
      Input('roessler-slider-n', 'value'),
      Input('roessler-slider-h', 'value'),
      Input('roessler-option-impl', 'value')
  ])(update_figure)
