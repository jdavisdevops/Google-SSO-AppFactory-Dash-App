import dash
from dashapp.layouts.gradedash import init_grade_layout
from dashapp.layouts.incidash import init_inci_layout
from dashapp.layouts.attendash import init_att_layout
from dashapp.layouts.navbar import init_navbar
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


def init_dashboard(server):
    app = dash.Dash(
        server=server,
        url_base_pathname="/dash/",
        # routes_pathname_prefix="/dash/",
        suppress_callback_exceptions=True,
        title="AUSD Dashboards",
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    navbar = init_navbar()
    grade_layout = init_grade_layout(app)
    inci_layout = init_inci_layout(app)
    att_layout = init_att_layout(app)

    app.layout = html.Div([navbar])

    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname):
        if pathname == "/dash/":
            return grade_layout
            
        if pathname == "/dash/incidash/":
            return inci_layout

        elif pathname == "/dash/attendash/":
            return att_layout

    return app
