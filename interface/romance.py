from dash.dependencies import Input, Output

import dash_html_components as html
import dash_core_components as core

from plotly import graph_objs as go
from plotly import tools

from dynamic import romance_naive

layout = html.Div(children=[
    html.H1(children='Romance dynamics'),

    html.Div(className='sliders-4', children=[
        html.Div(children=[
            html.Label(id='romance-label-n'),
            core.Slider(id='romance-slider-n', included=False, min=1,
                        max=10000, step=1, value=1000),
        ]),
        html.Div(children=[
            html.Label(id='romance-label-r0', children='R0'),
            core.Input(id='romance-input-r0', type='number',
                       inputmode='numeric', value=1.0, step=0.1)
        ]),
        html.Div(children=[
            html.Label(id='romance-label-j0', children='J0'),
            core.Input(id='romance-input-j0', type='number',
                       inputmode='numeric', value=1.0, step=0.1)
        ]),
        html.Div(children=[
            html.Label(id='romance-label-h'),
            core.Slider(id='romance-slider-h', included=False,
                        min=1e-3, max=1.0, step=1e-3, value=1e-3)
        ])
    ]),

    html.Div(children=[
        core.Graph(id='romance-graph')
    ]),

    html.Div(className='sliders-4', children=[
        html.Div(children=[
            html.Label(id='romance-label-a'),
            core.Slider(id='romance-slider-a', included=False, min=-10.0,
                        max=10.0, step=0.1, value=0.5),
        ]),
        html.Div(children=[
            html.Label(id='romance-label-b'),
            core.Slider(id='romance-slider-b', included=False, min=-10.0,
                        max=10.0, step=0.1, value=0.5)
        ]),
        html.Div(children=[
            html.Label(id='romance-label-c'),
            core.Slider(id='romance-slider-c', included=False, min=-10.0,
                        max=10.0, step=0.1, value=0.5)
        ]),
        html.Div(children=[
            html.Label(id='romance-label-d'),
            core.Slider(id='romance-slider-d', included=False, min=-10.0,
                        max=10.0, step=0.1, value=0.5)
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


def update_figure(R0, J0, a, b, c, d, N, h):
  R, J = romance_naive(R0, J0, a, b, c, d, N, h)

  dRdt = a * R + b * J
  dJdt = c * R + d * J

  trace1 = go.Scatter(x=R, y=J, mode='markers', marker=dict(color='#444'))
  trace2 = go.Scatter(x=R, y=dRdt, mode='markers', marker=dict(color='#444'))
  trace3 = go.Scatter(x=J, y=dJdt, mode='markers', marker=dict(color='#444'))

  figure = tools.make_subplots(
      cols=3, subplot_titles=('Romeo & Julian', 'Romeo', 'Julian'))

  figure.append_trace(trace1, 1, 1)
  figure.append_trace(trace2, 1, 2)
  figure.append_trace(trace3, 1, 3)

  figure['layout'].update(height=400, width=1000, showlegend=False)
  figure['layout']['xaxis1'].update(title='R')
  figure['layout']['yaxis1'].update(title='J')
  figure['layout']['xaxis2'].update(title='R')
  figure['layout']['yaxis2'].update(title='dR/dt')
  figure['layout']['xaxis3'].update(title='J')
  figure['layout']['yaxis3'].update(title='dJ/dt')

  return figure


def connect(app):
  app.callback(Output('romance-label-n', 'children'), [
      Input('romance-slider-n', 'value')
  ])(update_label_n)

  app.callback(Output('romance-label-h', 'children'), [
      Input('romance-slider-h', 'value')
  ])(update_label_h)

  app.callback(Output('romance-label-a', 'children'), [
      Input('romance-slider-a', 'value')
  ])(update_label_a)

  app.callback(Output('romance-label-b', 'children'), [
      Input('romance-slider-b', 'value')
  ])(update_label_b)

  app.callback(Output('romance-label-c', 'children'), [
      Input('romance-slider-c', 'value')
  ])(update_label_c)

  app.callback(Output('romance-label-d', 'children'), [
      Input('romance-slider-d', 'value')
  ])(update_label_d)

  app.callback(Output('romance-graph', 'figure'), [
      Input('romance-input-r0', 'value'),
      Input('romance-input-j0', 'value'),
      Input('romance-slider-a', 'value'),
      Input('romance-slider-b', 'value'),
      Input('romance-slider-c', 'value'),
      Input('romance-slider-d', 'value'),
      Input('romance-slider-n', 'value'),
      Input('romance-slider-h', 'value')
  ])(update_figure)
