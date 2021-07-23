import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from dashapp.layouts import charts
from dashapp.lib.dash_functions import ausd_colors, convert, generate_table

df = pd.read_csv("/home/jdavis/dds/dashapp/data/incidentexport.csv", delimiter=",")
df = df.drop("PARTICIPANT_NUMBER", 1)
df["INCIDENT_DATE"] = pd.to_datetime(df["INCIDENT_DATE"]).dt.date
df["ETHNICITY_NAME"] = df["ETHNICITY_NAME"].astype(str)


def init_inci_layout(app):
    app.layout = html.Div(
        style={"backgroundColor": ausd_colors["black"]},
        children=[
            html.Div(
                [
                    dcc.Tabs(
                        id="incitabs",
                        value="tab-1",
                        children=[
                            dcc.Tab(label="Incidents by Behavior", value="tab-1"),
                            dcc.Tab(label="Incidents by Action", value="tab-2"),
                            dcc.Tab(label="Behavior Intervention", value="tab-3"),
                        ],
                    ),
                    html.Div(id="incitabs-content"),
                ]
            ),
        ],
    )

    @app.callback(Output("incitabs-content", "children"), Input("incitabs", "value"))
    def render_content(tab):
        if tab == "tab-1":
            sub_chart = html.Div(
                html.Pre(
                    id="inci-chart", style={"backgroundColor": ausd_colors["white"]}
                )
            )
            sub_table = html.Div(
                html.Pre(
                    id="inci-table", style={"backgroundColor": ausd_colors["white"]}
                )
            )
            filters = html.Div(
                [
                    html.P(
                        "Year Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="year-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(df["School_Year"].unique())
                        ],
                        value="all",
                    ),
                    html.P(
                        "Date Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.DatePickerRange(id="date-picker"),
                    html.P(
                        "School Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="school-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"])
                            + list(sorted(df["Incident School"].unique()))
                        ],
                        value="all",
                    ),
                    html.P(
                        "SPED Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="sped-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(df["SPECIAL_ED_STUDENT"].unique())
                        ],
                        value="all",
                    ),
                    html.P(
                        "Ethnicity Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="eth-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"])
                            + list(sorted(df["ETHNICITY_NAME"].unique()))
                        ],
                        value="all",
                    ),
                ]
            )

            layout = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(filters, width="3"),
                            dbc.Col(sub_chart, width="9"),
                        ]
                    )
                ]
            )
            return layout, sub_table

        elif tab == "tab-2":
            sub_chart = html.Div(
                html.Pre(
                    id="inci-action-chart",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )
            sub_table = html.Div(
                html.Pre(
                    id="inci-action-table",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )
            filters = html.Div(
                [
                    html.P(
                        "Year Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="action-year-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(df["School_Year"].unique())
                        ],
                        value="all",
                    ),
                    html.P(
                        "Date Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.DatePickerRange(id="action-date-picker"),
                    html.P(
                        "School Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="action-school-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"])
                            + list(sorted(df["Incident School"].unique()))
                        ],
                        value="all",
                    ),
                    html.P(
                        "SPED Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="action-sped-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(df["SPECIAL_ED_STUDENT"].unique())
                        ],
                        value="all",
                    ),
                    html.P(
                        "Ethnicity Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="action-eth-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"])
                            + list(sorted(df["ETHNICITY_NAME"].unique()))
                        ],
                        value="all",
                    ),
                ]
            )

            layout = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(filters, width="3"),
                            dbc.Col(sub_chart, width="9"),
                        ]
                    )
                ]
            )
            return layout, sub_table

        else:
            return generate_table(df)

    @app.callback(
        [
            Output("date-picker", "min_date_allowed"),
            Output("date-picker", "max_date_allowed"),
            Output("date-picker", "start_date"),
            Output("date-picker", "end_date"),
        ],
        Input("year-picker", "value"),
    )
    def update_datepicker(year):
        if year == "all":
            filtered_df = df.copy()
            min_date_allowed = str(filtered_df["INCIDENT_DATE"].min())
            max_date_allowed = str(
                filtered_df["INCIDENT_DATE"].max() + pd.Timedelta(days=1)
            )
            start_date = min_date_allowed
            end_date = max_date_allowed
            return min_date_allowed, max_date_allowed, start_date, end_date
        else:
            filtered_df = df[df["School_Year"] == year]
            min_date_allowed = str(filtered_df["INCIDENT_DATE"].min())
            max_date_allowed = str(
                filtered_df["INCIDENT_DATE"].max() + pd.Timedelta(days=1)
            )
            start_date = min_date_allowed
            end_date = max_date_allowed
            return min_date_allowed, max_date_allowed, start_date, end_date

    @app.callback(
        Output("inci-chart", "children"),
        [
            Input("year-picker", "value"),
            Input("school-picker", "value"),
            Input("sped-picker", "value"),
            Input("eth-picker", "value"),
            Input("date-picker", "start_date"),
            Input("date-picker", "end_date"),
        ],
    )
    def update_incident_chart(year, school, sped, eth, start_date, end_date):
        filtered_df = df.copy()
        filtered_df["INCIDENT_DATE"] = filtered_df["INCIDENT_DATE"].astype(str)
        filtered_df = filtered_df.loc[
            (filtered_df["INCIDENT_DATE"] >= start_date)
            & (filtered_df["INCIDENT_DATE"] < end_date)
        ]
        if year == "all":
            year = list(filtered_df["School_Year"].unique())
        else:
            year = convert(year)
        if school == "all":
            school = list(filtered_df["Incident School"].unique())
        else:
            school = convert(school)
        if sped == "all":
            sped = list(filtered_df["SPECIAL_ED_STUDENT"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        filtered_df = filtered_df[filtered_df["School_Year"].isin(year)]
        filtered_df = filtered_df[filtered_df["Incident School"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPECIAL_ED_STUDENT"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        return charts.incichart(filtered_df)

    @app.callback(
        Output("inci-table", "children"),
        [
            Input("behavior-counts", "clickData"),
            Input("year-picker", "value"),
            Input("school-picker", "value"),
            Input("sped-picker", "value"),
            Input("eth-picker", "value"),
            Input("date-picker", "start_date"),
            Input("date-picker", "end_date"),
        ],
    )
    def render_subtable(clickData, year, school, sped, eth, start_date, end_date):
        filtered_df = df.copy()
        filtered_df["INCIDENT_DATE"] = filtered_df["INCIDENT_DATE"].astype(str)
        filtered_df = filtered_df.loc[
            (filtered_df["INCIDENT_DATE"] >= start_date)
            & (filtered_df["INCIDENT_DATE"] < end_date)
        ]
        if year == "all":
            year = list(filtered_df["School_Year"].unique())
        else:
            year = convert(year)
        if school == "all":
            school = list(filtered_df["Incident School"].unique())
        else:
            school = convert(school)
        if sped == "all":
            sped = list(filtered_df["SPECIAL_ED_STUDENT"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        filtered_df = filtered_df[filtered_df["School_Year"].isin(year)]
        filtered_df = filtered_df[filtered_df["Incident School"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPECIAL_ED_STUDENT"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        if clickData is not None:
            behavior = clickData["points"][0]
            key = behavior.get("x")
            filtered_df = filtered_df[filtered_df["Behavior"] == key]
            filtered_df = filtered_df.sort_values(by="STUDENT_NUMBER", ascending=False)
            return generate_table(filtered_df)
        else:
            return generate_table(filtered_df)

    # Tab 2 Callbacks

    @app.callback(
        [
            Output("action-date-picker", "min_date_allowed"),
            Output("action-date-picker", "max_date_allowed"),
            Output("action-date-picker", "start_date"),
            Output("action-date-picker", "end_date"),
        ],
        Input("action-year-picker", "value"),
    )
    def update_datepicker(year):
        if year == "all":
            filtered_df = df.copy()
            min_date_allowed = str(filtered_df["INCIDENT_DATE"].min())
            max_date_allowed = str(
                filtered_df["INCIDENT_DATE"].max() + pd.Timedelta(days=1)
            )
            start_date = min_date_allowed
            end_date = max_date_allowed
            return min_date_allowed, max_date_allowed, start_date, end_date
        else:
            filtered_df = df[df["School_Year"] == year]
            min_date_allowed = str(filtered_df["INCIDENT_DATE"].min())
            max_date_allowed = str(
                filtered_df["INCIDENT_DATE"].max() + pd.Timedelta(days=1)
            )
            start_date = min_date_allowed
            end_date = max_date_allowed
            return min_date_allowed, max_date_allowed, start_date, end_date

    @app.callback(
        Output("inci-action-chart", "children"),
        [
            Input("action-year-picker", "value"),
            Input("action-school-picker", "value"),
            Input("action-sped-picker", "value"),
            Input("action-eth-picker", "value"),
            Input("action-date-picker", "start_date"),
            Input("action-date-picker", "end_date"),
        ],
    )
    def update_action_chart(year, school, sped, eth, start_date, end_date):
        filtered_df = df.copy()
        filtered_df["INCIDENT_DATE"] = filtered_df["INCIDENT_DATE"].astype(str)
        filtered_df = filtered_df.loc[
            (filtered_df["INCIDENT_DATE"] >= start_date)
            & (filtered_df["INCIDENT_DATE"] < end_date)
        ]
        if year == "all":
            year = list(filtered_df["School_Year"].unique())
        else:
            year = convert(year)
        if school == "all":
            school = list(filtered_df["Incident School"].unique())
        else:
            school = convert(school)
        if sped == "all":
            sped = list(filtered_df["SPECIAL_ED_STUDENT"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        filtered_df = filtered_df[filtered_df["School_Year"].isin(year)]
        filtered_df = filtered_df[filtered_df["Incident School"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPECIAL_ED_STUDENT"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        return charts.inci_action_chart(filtered_df)

    @app.callback(
        Output("inci-action-table", "children"),
        [
            Input("action-counts", "clickData"),
            Input("action-year-picker", "value"),
            Input("action-school-picker", "value"),
            Input("action-sped-picker", "value"),
            Input("action-eth-picker", "value"),
            Input("action-date-picker", "start_date"),
            Input("action-date-picker", "end_date"),
        ],
    )
    def render_subtable(clickData, year, school, sped, eth, start_date, end_date):
        filtered_df = df.copy()
        filtered_df["INCIDENT_DATE"] = filtered_df["INCIDENT_DATE"].astype(str)
        filtered_df = filtered_df.loc[
            (filtered_df["INCIDENT_DATE"] >= start_date)
            & (filtered_df["INCIDENT_DATE"] < end_date)
        ]
        if year == "all":
            year = list(filtered_df["School_Year"].unique())
        else:
            year = convert(year)
        if school == "all":
            school = list(filtered_df["Incident School"].unique())
        else:
            school = convert(school)
        if sped == "all":
            sped = list(filtered_df["SPECIAL_ED_STUDENT"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        filtered_df = filtered_df[filtered_df["School_Year"].isin(year)]
        filtered_df = filtered_df[filtered_df["Incident School"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPECIAL_ED_STUDENT"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        if clickData is not None:
            action = clickData["points"][0]
            key = action.get("x")
            filtered_df = filtered_df[filtered_df["Action"] == key]
            filtered_df = filtered_df.sort_values(by="STUDENT_NUMBER", ascending=False)
            return generate_table(filtered_df)
        else:
            return generate_table(filtered_df)

    return app.layout
