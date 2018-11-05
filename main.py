from dash import Dash
from dash.dependencies import Input, Output

import dash_html_components as html
import dash_core_components as core

from interface import index
from interface import romance


app = Dash(__name__)

app.layout = html.Div([
    core.Location(id='route', refresh=False),
    html.Div(className='container', children=[
        html.Div(id='content')
    ])
])

app.config.suppress_callback_exceptions = True

index.connect(app)
romance.connect(app)


@app.callback(Output('content', 'children'), [Input('route', 'pathname')])
def route(pathname):
  if pathname == '/':
    return index.layout

  if pathname == '/romance':
    return romance.layout


if __name__ == '__main__':
  app.run_server(debug=True)
