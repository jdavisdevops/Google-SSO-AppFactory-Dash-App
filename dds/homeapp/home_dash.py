import dash
from dash.dependencies import Output
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Div import Div
from flask_login import current_user
from dash.dependencies import Input, Output

user = current_user


def init_home_dashboard(server):
    app = dash.Dash(
        server=server,
        url_base_pathname="/home/",
        suppress_callback_exceptions=False,
        title="AUSD Data Gateway",
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    profile_photo = html.Div(
        [html.Img(style={"height": "10%", "width": "10%"}, id="user-photo")]
    )

    jumbotron = dbc.Jumbotron(
        [
            dbc.Container(
                [
                    html.H1(
                        id="welcome-name",
                        className="display-3",
                    ),
                    html.Div(profile_photo),
                    html.P(
                        "We have a suite of dashboards to help you find the insights you need :) ",
                        className="lead",
                    ),
                    html.P(
                        "Let us know if you have any ideas you'd like to see included here.",
                        className="lead",
                    ),
                ],
                fluid=True,
            )
        ],
        fluid=True,
    )

    base_nav = dbc.Nav(
        [
            dbc.NavItem(
                dbc.NavLink(
                    "AUSD Data Dash", active=True, href="/dash/", external_link=True
                )
            ),
            dbc.NavItem(
                dbc.NavLink(
                    "PowerSchool",
                    href="https://powerschool.ausd.net/admin",
                    external_link=True,
                    target="blank",
                )
            ),
            dbc.NavItem(dbc.NavLink("Your Data", href="/data", external_link=True)),
            dbc.NavItem(dbc.NavLink("Future?", disabled=True, href="#")),
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem("Star Reading Scores"),
                    dbc.DropdownMenuItem("Star Math Scores"),
                    dbc.DropdownMenuItem("Star Reports"),
                ],
                label="Star Renaissance",
                nav=True,
            ),
        ]
    )

    ausd_photo = html.Div(
        [
            html.Img(
                src=r"https://i.ytimg.com/vi/95Rr7JCcQec/maxresdefault.jpg",
                style={"height": "50%", "width": "50%"},
            )
        ]
    )

    # photos = html.Div(
    #     [
    #         dbc.Row(
    #             [
    #                 dbc.Col(ausd_photo, width="auto"),
    #                 dbc.Col(profile_photo, width="auto"),
    #             ]
    #         )
    #     ]
    # )

    app.layout = html.Div([ausd_photo, base_nav, jumbotron])

    @app.callback(Output("user-photo", "src"), [Input("user-photo", "id")])
    def show_user_photo(input1):
        if current_user.is_authenticated:
            return current_user.profile_pic

    @app.callback(Output("welcome-name", "children"), [Input("welcome-name", "id")])
    def hi_name(input1):
        if current_user.is_authenticated:
            first_name = current_user.first_name
            return f"Hi {first_name} welcome to the AUSD Data Gateway!"

    # @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    # def display_page(pathname):
    #     if pathname == "/dash/":
    #         return grade_layout

    #     if pathname == "/dash/incidash/":
    #         return inci_layout

    #     elif pathname == "/dash/attendash/":
    #         return att_layout

    return app
