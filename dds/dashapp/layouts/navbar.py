import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


def init_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Grade Dashboard", href="/dash/")),
            dbc.NavItem(dbc.NavLink("Incident Dashboard", href="/dash/incidash/")),
            dbc.NavItem(dbc.NavLink("Attendance Dashboard", href="/dash/attendash/")),
            dbc.NavItem(dbc.NavLink("AUSD Data Gateway Home", href="/home/", external_link=True)),
            # dbc.DropdownMenu(
            #     children=[
            #         dbc.DropdownMenuItem("Incident Dashboard", href="/incidash"),
            #         dbc.DropdownMenuItem("Page 3", href="#"),
            #     ],
            #     nav=True,
            #     in_navbar=True,
            #     label="More",
            # ),
        ],
        brand="AUSD Data Dash",
        color="rgb(186,0,0)",
        dark=True,
    )

    layout = html.Div(
        [
            navbar,
            dcc.Location(id="url", refresh=True),
            html.Div(id="page-content"),
        ]
    )

    return layout
