import dash_html_components as html
import dash_core_components as core


layout = html.Div(children=[
    html.Ul(children=[
        html.Li(children=[
            core.Link('Romance', href='/romance'),
        ]),
        html.Li(children=[
            core.Link('Rössler', href='/roessler')
        ])
    ])
])


def connect(app):
  pass
