from dash.dependencies import Input, Output

import dash_html_components as html
import dash_core_components as core

from scipy.signal import argrelmax

from dynamic import roessler_naive
from dynamic import roessler_rk4

layout = html.Div(children=[
    html.H1(children='Roessler dynamics'),

    html.Div(className='sliders-5', children=[
        html.Div(children=[
            html.Label(id='roessler-label-n'),
            core.Slider(id='roessler-slider-n', included=False, min=1,
                        max=100000, step=1, value=1000),
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-impl', children='Implementation'),
            core.Dropdown(id='roessler-option-impl', options=[
                {'label': 'Naive', 'value': 'naive'},
                {'label': 'Runge Kutta', 'value': 'rk4'}
            ], value='naive')
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-x0', children='X0'),
            core.Input(id='roessler-input-x0', type='number',
                       inputmode='numeric', value=0.2, step=0.1)
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-y0', children='Y0'),
            core.Input(id='roessler-input-y0', type='number',
                       inputmode='numeric', value=0.3, step=0.1)
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-z0', children='Z0'),
            core.Input(id='roessler-input-z0', type='number',
                       inputmode='numeric', value=0.1, step=0.1)
        ])
    ]),

    html.Div(children=[
        core.Graph(id='roessler-graph')
    ]),

    html.Div(className='sliders-5', children=[
        html.Div(children=[
            html.Label(id='roessler-label-h'),
            core.Slider(id='roessler-slider-h', included=False,
                        min=1e-3, max=1e-1, step=1e-3, value=1e-3)
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-a', children='a'),
            core.Input(id='roessler-input-a', step=0.01, value=0.2,
                       type='number', inputmode='numeric')
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-b', children='b'),
            core.Input(id='roessler-input-b', step=0.01, value=0.2,
                       type='number', inputmode='numeric')
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-c', children='c'),
            core.Input(id='roessler-input-c', step=0.01, value=5.7,
                       type='number', inputmode='numeric')
        ]),
        html.Div(children=[
            html.Label(id='roessler-label-view', children='View'),
            core.Dropdown(id='roessler-option-view', options=[
                {'label': 'XY Plane', 'value': 'xy'},
                {'label': '1D Map', 'value': 'map'}
            ], value='xy')
        ])
    ])
])


def update_label_n(value):
  return f'N = {value}'


def update_label_h(value):
  return f'Δt = {value}'


def update_figure(x0, y0, z0, a, b, c, N, h, impl, view):
  if impl == 'naive':
    x, y, z = roessler_naive(x0, y0, z0, a, b, c, N, h)
  if impl == 'rk4':
    x, y, z = roessler_rk4(x0, y0, z0, a, b, c, N, h)

  if view == 'xy':
    u, v = x, y

    utitle = 'x'
    vtitle = 'y'
  if view == 'map':
    u = x[argrelmax(x, order=1)[0]][:-1]
    v = x[argrelmax(x, order=1)[0]][1:]

    utitle = 'x_{i}'
    vtitle = 'x_{i+1}'

  return {
      'data': [
          {
              'x': x, 'y': y, 'z': y,
              'type': 'scatter3d',
              'mode': 'markers',
              'marker': {'color': '#444', 'size': 2}
          },
          {
              'x': u, 'y': v,
              'type': 'scatter',
              'mode': 'markers',
              'marker': {'color': '#444', 'size': 2}
          }
      ],
      'layout': {
          'scene': {
              'domain': {
                  'x': [0, 0.6],
                  'y': [0, 1.0]
              },
              'xaxis': {'title': 'x'},
              'yaxis': {'title': 'y'},
              'camera': {
                  'up': {'x': 0, 'y': 1, 'z': 0},
                  'center': {'x': 0, 'y': 0, 'z': 0},
                  'eye': {'x': 0.1, 'y': -2.5, 'z': 0.1}
              }
          },
          'xaxis': {
              'title': utitle,
              'anchor': 'y',
              'domain': [0.6, 1.0]
          },
          'yaxis': {
              'title': vtitle,
              'anchor': 'x',
              'domain': [0.2, 0.8]
          },
          'height': 560,
          'showlegend': False
      }
  }


def connect(app):
  app.callback(Output('roessler-label-n', 'children'), [
      Input('roessler-slider-n', 'value')
  ])(update_label_n)

  app.callback(Output('roessler-label-h', 'children'), [
      Input('roessler-slider-h', 'value')
  ])(update_label_h)

  app.callback(Output('roessler-graph', 'figure'), [
      Input('roessler-input-x0', 'value'),
      Input('roessler-input-y0', 'value'),
      Input('roessler-input-z0', 'value'),
      Input('roessler-input-a', 'value'),
      Input('roessler-input-b', 'value'),
      Input('roessler-input-c', 'value'),
      Input('roessler-slider-n', 'value'),
      Input('roessler-slider-h', 'value'),
      Input('roessler-option-impl', 'value'),
      Input('roessler-option-view', 'value')
  ])(update_figure)
