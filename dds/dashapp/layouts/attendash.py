import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from dashapp.layouts import charts
from dashapp.lib.dash_functions import ausd_colors, convert, generate_table

df = pd.read_csv("/home/jdavis/dds/dashapp/data/attendanceexport.csv", delimiter=",")
df["STUDENT_NUMBER"] = df["STUDENT_NUMBER"].astype(str)
df["ATT_DATE"] = pd.to_datetime(df["ATT_DATE"]).dt.date
df["ATT_DATE"] = df["ATT_DATE"].astype(str)
df["ETHNICITY_NAME"] = df["ETHNICITY_NAME"].astype(str)


def init_att_layout(app):
    layout = html.Div(
        style={"backgroundColor": ausd_colors["black"]},
        children=[
            html.Div(
                [
                    dcc.Tabs(
                        id="attentabs",
                        value="tab-1",
                        children=[
                            dcc.Tab(label="Attendance by Code", value="tab-1"),
                            dcc.Tab(label="Attendance by Student", value="tab-2"),
                            dcc.Tab(label="All Attendance Data", value="tab-3"),
                        ],
                    ),
                    html.Div(id="attentabs-content"),
                ]
            ),
        ],
    )

    @app.callback(
        Output("attentabs-content", "children"), [Input("attentabs", "value")]
    )
    def render_content(tab):
        tab_header = dcc.Markdown("""Date Filter &#8595""")
        hover_message = dcc.Markdown("""School Site Filter &#8595""")
        # p = dbc.Row([dbc.Col(html.H5(tab_header, style={"color": ausd_colors['white']})),
        #              dbc.Col(html.H5(hover_message, style={"color": ausd_colors['white'], 'textAlign': 'right'}))])
        if tab == "tab-1":
            sub_chart = html.Div(
                html.Pre(
                    id="code-counts-chart",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )
            sub_table = html.Div(
                html.Pre(
                    id="code-counts-table",
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
                        id="year-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(df["School_Year"].unique())
                        ],
                        value=str(df["School_Year"].max()),
                    ),
                    html.P(
                        "Date Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.DatePickerRange(
                        id="code-counts-datepicker",
                        # min_date_allowed=least_recent_date,
                        # max_date_allowed=most_recent_date,
                        # start_date=least_recent_date,
                        # end_date=most_recent_date,
                        # persistence_type='session'
                    ),
                    html.P(
                        "School Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="school-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(sorted(df["SCHOOL"].unique()))
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
                    html.P(
                        "Present Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="present-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(df["PRESENCE_STATUS_CD"].unique())
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
                    id="stu-code-counts-chart",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )
            sub_table = html.Div(
                html.Pre(
                    id="stu-code-counts-table",
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
                        id="stu-year-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(df["School_Year"].unique())
                        ],
                        value=str(df["School_Year"].max()),
                    ),
                    html.P(
                        "Date Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.DatePickerRange(id="stu-code-counts-datepicker"),
                    html.P(
                        "School Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="stu-school-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(sorted(df["SCHOOL"].unique()))
                        ],
                        value="all",
                    ),
                    html.P(
                        "Code Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="stu-code-picker",
                        # options=[{'label': i, 'value': i} for i in (['all']) + list(df['ATT_CODE'].unique())],
                        value="all",
                    ),
                    html.P(
                        "SPED Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="stu-sped-picker",
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
                        id="stu-eth-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"])
                            + list(sorted(df["ETHNICITY_NAME"].unique()))
                        ],
                        value="all",
                    ),
                    html.P(
                        "Present Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="stu-present-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(df["PRESENCE_STATUS_CD"].unique())
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
            Output("code-counts-datepicker", "min_date_allowed"),
            Output("code-counts-datepicker", "max_date_allowed"),
            Output("code-counts-datepicker", "start_date"),
            Output("code-counts-datepicker", "end_date"),
        ],
        Input("year-picker", "value"),
    )
    def update_datepicker(year):
        if year == "all":
            filtered_df = df.copy()
            min_date_allowed = str(filtered_df["ATT_DATE"].min())
            max_date_allowed = str(filtered_df["ATT_DATE"].max())
            start_date = min_date_allowed
            end_date = max_date_allowed
            return min_date_allowed, max_date_allowed, start_date, end_date
        else:
            filtered_df = df[df["School_Year"] == year]
            min_date_allowed = str(filtered_df["ATT_DATE"].min())
            max_date_allowed = str(filtered_df["ATT_DATE"].max())
            start_date = min_date_allowed
            end_date = max_date_allowed
            return min_date_allowed, max_date_allowed, start_date, end_date

    @app.callback(
        Output("code-counts-chart", "children"),
        [
            Input("year-picker", "value"),
            Input("school-picker", "value"),
            Input("sped-picker", "value"),
            Input("eth-picker", "value"),
            Input("present-picker", "value"),
            Input("code-counts-datepicker", "start_date"),
            Input("code-counts-datepicker", "end_date"),
        ],
    )
    def update_code_counts(year, school, sped, eth, present, start_date, end_date):
        filtered_df = df.loc[
            (df["ATT_DATE"] >= start_date) & (df["ATT_DATE"] < end_date)
        ]
        if year == "all":
            year = list(filtered_df["School_Year"].unique())
        else:
            year = convert(year)
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
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
        if present == "all":
            present = list(filtered_df["PRESENCE_STATUS_CD"].unique())
        else:
            present = convert(present)
        return charts.attendance_code_chart(
            filtered_df, year, school, sped, eth, present
        )

    @app.callback(
        Output("code-counts-table", "children"),
        [
            Input("code-counts", "clickData"),
            Input("year-picker", "value"),
            Input("school-picker", "value"),
            Input("sped-picker", "value"),
            Input("eth-picker", "value"),
            Input("present-picker", "value"),
            Input("code-counts-datepicker", "start_date"),
            Input("code-counts-datepicker", "end_date"),
        ],
    )
    def render_subchart(
        clickData, year, school, sped, eth, present, start_date, end_date
    ):
        filtered_df = df.loc[
            (df["ATT_DATE"] >= start_date) & (df["ATT_DATE"] < end_date)
        ]
        if year == "all":
            year = list(filtered_df["School_Year"].unique())
        else:
            year = convert(year)
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
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
        if present == "all":
            present = list(filtered_df["PRESENCE_STATUS_CD"].unique())
        else:
            present = convert(present)
        filtered_df = filtered_df[filtered_df["School_Year"].isin(year)]
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPECIAL_ED_STUDENT"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        filtered_df = filtered_df[filtered_df["PRESENCE_STATUS_CD"].isin(present)]
        filtered_df = filtered_df.sort_values(by="ATT_DATE", ascending=False)
        if clickData is not None:
            jsondump = clickData["points"][0]
            key = jsondump.get("x")
            filtered_df = filtered_df[filtered_df["ATT_CODE"] == key]
            return generate_table(filtered_df)
        else:
            return generate_table(filtered_df)

    # Tab 2 Callbacks

    @app.callback(
        [
            Output("stu-code-counts-datepicker", "min_date_allowed"),
            Output("stu-code-counts-datepicker", "max_date_allowed"),
            Output("stu-code-counts-datepicker", "start_date"),
            Output("stu-code-counts-datepicker", "end_date"),
        ],
        Input("stu-year-picker", "value"),
    )
    def update_datepicker(year):
        if year == "all":
            filtered_df = df.copy()
            min_date_allowed = str(filtered_df["ATT_DATE"].min())
            max_date_allowed = str(filtered_df["ATT_DATE"].max())
            start_date = min_date_allowed
            end_date = max_date_allowed
            return min_date_allowed, max_date_allowed, start_date, end_date
        else:
            filtered_df = df[df["School_Year"] == year]
            min_date_allowed = str(filtered_df["ATT_DATE"].min())
            max_date_allowed = str(filtered_df["ATT_DATE"].max())
            start_date = min_date_allowed
            end_date = max_date_allowed
            return min_date_allowed, max_date_allowed, start_date, end_date

    @app.callback(
        Output("stu-code-picker", "options"),
        [
            Input("stu-present-picker", "value"),
            Input("stu-year-picker", "value"),
            Input("stu-school-picker", "value"),
            Input("stu-sped-picker", "value"),
            Input("stu-eth-picker", "value"),
            Input("stu-code-counts-datepicker", "start_date"),
            Input("stu-code-counts-datepicker", "end_date"),
        ],
    )
    def update_code_dropdown(present, year, school, sped, eth, start_date, end_date):
        filtered_df = df.loc[
            (df["ATT_DATE"] >= start_date) & (df["ATT_DATE"] < end_date)
        ]
        if year == "all":
            year = list(filtered_df["School_Year"].unique())
        else:
            year = convert(year)
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
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
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPECIAL_ED_STUDENT"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        if present == "Present":
            filtered_df = filtered_df[filtered_df["PRESENCE_STATUS_CD"] == "Present"]
            return [
                {"label": i, "value": i}
                for i in (["all"]) + list(filtered_df["ATT_CODE"].unique())
            ]
        elif present == "Absent":
            filtered_df = filtered_df[filtered_df["PRESENCE_STATUS_CD"] == "Absent"]
            return [
                {"label": i, "value": i}
                for i in (["all"]) + list(filtered_df["ATT_CODE"].unique())
            ]
        else:
            return [
                {"label": i, "value": i}
                for i in (["all"]) + list(filtered_df["ATT_CODE"].unique())
            ]

    @app.callback(
        Output("stu-code-counts-chart", "children"),
        [
            Input("stu-year-picker", "value"),
            Input("stu-school-picker", "value"),
            Input("stu-code-picker", "value"),
            Input("stu-sped-picker", "value"),
            Input("stu-eth-picker", "value"),
            Input("stu-present-picker", "value"),
            Input("stu-code-counts-datepicker", "start_date"),
            Input("stu-code-counts-datepicker", "end_date"),
        ],
    )
    def update_code_counts(
        year, school, code, sped, eth, present, start_date, end_date
    ):
        filtered_df = df.loc[
            (df["ATT_DATE"] >= start_date) & (df["ATT_DATE"] < end_date)
        ]
        if year == "all":
            year = list(filtered_df["School_Year"].unique())
        else:
            year = convert(year)
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
        else:
            school = convert(school)
        if code == "all":
            code = list(filtered_df["ATT_CODE"].unique())
        else:
            code = convert(code)
        if sped == "all":
            sped = list(filtered_df["SPECIAL_ED_STUDENT"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        if present == "all":
            present = list(filtered_df["PRESENCE_STATUS_CD"].unique())
        else:
            present = convert(present)
        filtered_df = filtered_df[filtered_df["School_Year"].isin(year)]
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        filtered_df = filtered_df[filtered_df["ATT_CODE"].isin(code)]
        filtered_df = filtered_df[filtered_df["SPECIAL_ED_STUDENT"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        filtered_df = filtered_df[filtered_df["PRESENCE_STATUS_CD"].isin(present)]
        return charts.student_attendance_code_chart(filtered_df)

    @app.callback(
        Output("stu-code-counts-table", "children"),
        [
            Input("stu-code-counts", "clickData"),
            Input("stu-year-picker", "value"),
            Input("stu-school-picker", "value"),
            Input("stu-code-picker", "value"),
            Input("stu-sped-picker", "value"),
            Input("stu-eth-picker", "value"),
            Input("stu-present-picker", "value"),
            Input("stu-code-counts-datepicker", "start_date"),
            Input("stu-code-counts-datepicker", "end_date"),
        ],
    )
    def render_subchart(
        clickData, year, school, code, sped, eth, present, start_date, end_date
    ):
        filtered_df = df.loc[
            (df["ATT_DATE"] >= start_date) & (df["ATT_DATE"] < end_date)
        ]
        if year == "all":
            year = list(filtered_df["School_Year"].unique())
        else:
            year = convert(year)
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
        else:
            school = convert(school)
        if code == "all":
            code = list(filtered_df["ATT_CODE"].unique())
        else:
            code = convert(code)
        if sped == "all":
            sped = list(filtered_df["SPECIAL_ED_STUDENT"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        if present == "all":
            present = list(filtered_df["PRESENCE_STATUS_CD"].unique())
        else:
            present = convert(present)
        filtered_df = filtered_df[filtered_df["School_Year"].isin(year)]
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        filtered_df = filtered_df[filtered_df["ATT_CODE"].isin(code)]
        filtered_df = filtered_df[filtered_df["SPECIAL_ED_STUDENT"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        filtered_df = filtered_df[filtered_df["PRESENCE_STATUS_CD"].isin(present)]
        filtered_df = filtered_df.sort_values(
            by=["ATT_DATE", "ATT_CODE"], ascending=False
        )
        if clickData is not None:
            jsondump = clickData["points"][0]
            key = jsondump.get("x")
            filtered_df = filtered_df[filtered_df["STUDENT_NUMBER"] == key]
            return generate_table(filtered_df)
        else:
            return generate_table(filtered_df)

    return layout
