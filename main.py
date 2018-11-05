from dash import Dash
from dash.dependencies import Input, Output

import dash_html_components as html
import dash_core_components as core

from plotly import graph_objs as go
from plotly import tools

from dynamics import romance

app = Dash(__name__)

app.layout = html.Div(className='container', children=[
    html.H1(children='Romance dynamics'),

    html.Div(className='sliders-4', children=[
        html.Div(children=[
            html.Label(id='labeln'),
            core.Slider(id='slidern', included=False, min=1,
                        max=10000, step=1, value=1000),
        ]),
        html.Div(children=[
            html.Label(id='labelr0', children='R0'),
            core.Input(id='inputr0', type='number',
                       inputmode='numeric', value=1.0, step=0.1)
        ]),
        html.Div(children=[
            html.Label(id='labelj0', children='J0'),
            core.Input(id='inputj0', type='number',
                       inputmode='numeric', value=1.0, step=0.1)
        ]),
        html.Div(children=[
            html.Label(id='labelt'),
            core.Slider(id='slidert', included=False,
                        min=1e-3, max=1.0, step=1e-3, value=1e-3)
        ])
    ]),

    html.Div(children=[
        core.Graph(id='graph')
    ]),

    html.Div(className='sliders-4', children=[
        html.Div(children=[
            html.Label(id='labela'),
            core.Slider(id='slidera', included=False, min=-10.0, max=10.0,
                        step=0.1, value=0.5),
        ]),
        html.Div(children=[
            html.Label(id='labelb'),
            core.Slider(id='sliderb', included=False, min=-10.0, max=10.0,
                        step=0.1, value=0.5)
        ]),
        html.Div(children=[
            html.Label(id='labelc'),
            core.Slider(id='sliderc', included=False, min=-10.0, max=10.0,
                        step=0.1, value=0.5)
        ]),
        html.Div(children=[
            html.Label(id='labeld'),
            core.Slider(id='sliderd', included=False, min=-10.0, max=10.0,
                        step=0.1, value=0.5)
        ])
    ])
])


@app.callback(Output('labeln', 'children'), [Input('slidern', 'value')])
def update_labeln(value):
  return f'N = {value}'


@app.callback(Output('labelt', 'children'), [Input('slidert', 'value')])
def update_labelt(value):
  return f'Δt = {value}'


@app.callback(Output('labela', 'children'), [Input('slidera', 'value')])
def update_labela(value):
  return f'a = {value}'


@app.callback(Output('labelb', 'children'), [Input('sliderb', 'value')])
def update_labelb(value):
  return f'b = {value}'


@app.callback(Output('labelc', 'children'), [Input('sliderc', 'value')])
def update_labelc(value):
  return f'c = {value}'


@app.callback(Output('labeld', 'children'), [Input('sliderd', 'value')])
def update_labeld(value):
  return f'd = {value}'


@app.callback(Output('graph', 'figure'), [
    Input('inputr0', 'value'),
    Input('inputj0', 'value'),
    Input('slidera', 'value'),
    Input('sliderb', 'value'),
    Input('sliderc', 'value'),
    Input('sliderd', 'value'),
    Input('slidern', 'value'),
    Input('slidert', 'value')
])
def update_figure(R0, J0, a, b, c, d, N, dt):
  R, J = romance(R0, J0, a, b, c, d, N, dt)

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


if __name__ == '__main__':
  app.run_server(debug=True)
