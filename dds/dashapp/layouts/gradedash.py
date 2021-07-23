import warnings
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from dashapp.layouts import charts
from dashapp.lib.dash_functions import ausd_colors, generate_table, convert

warnings.simplefilter(action="ignore", category=FutureWarning)
df = pd.read_csv("/home/jdavis/dds/dashapp/data/gradeexport.csv", delimiter=",")
# DF Pre-Processing
df = df.astype(str)
df["GRADE_LEVEL"] = df["GRADE_LEVEL"].astype(int)
df = df.replace("nan", "")
df["COUNSELOR"] = df["COUNSELOR"].str.replace(".0", "")
df["PERIOD"] = df["PERIOD"].str.replace("A", "")
df["PERIOD"] = df["PERIOD"].str.replace("(", "")
df["PERIOD"] = df["PERIOD"].str.replace(")", "")


def init_grade_layout(app):

    layout = html.Div(
        style={"backgroundColor": ausd_colors["black"]},
        children=[
            html.Div(
                [
                    dcc.Tabs(
                        id="tabs",
                        value="tab-1",
                        children=[
                            dcc.Tab(label="Grade Counts", value="tab-1"),
                            dcc.Tab(label="Student Grade Counts", value="tab-2"),
                            dcc.Tab(label="Distribution Analysis", value="tab-3"),
                            dcc.Tab(label="All Grade Data", value="tab-4"),
                        ],
                    ),
                    html.Div(id="tabs-content"),
                ]
            ),
        ],
    )

    @app.callback(Output("tabs-content", "children"), [Input("tabs", "value")])
    def render_content(tab):
        if tab == "tab-1":
            sub_chart = html.Div(
                html.Pre(
                    id="grade-counts-chart",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )
            sub_table = html.Div(
                html.Pre(
                    id="grade-counts-table",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )

            filters = html.Div(
                [
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
                            for i in (["all"]) + list(df["SPED Status"].unique())
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
                        "Grade Level Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="grade-level-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in list(sorted(df["GRADE_LEVEL"].unique()))
                        ],
                        multi=True,
                        # value=[i for i in list(sorted(df['GRADE_LEVEL'].unique()))],
                        clearable=False,
                    ),
                    html.P(
                        "Grade Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="grade-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in list(sorted(df["GRADE"].unique()))
                        ],
                        multi=True,
                        value=["D+", "D-", "F"],
                        clearable=False,
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
            p2 = html.H6(id="df-counts-text", style={"color": ausd_colors["white"]})
            sub_chart = html.Div(
                html.Pre(
                    id="stu-grades-chart",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )
            sub_table = html.Div(
                html.Pre(
                    id="stu-grades-table",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )
            filters = html.Div(
                [
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
                        "SPED Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="stu-sped-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in (["all"]) + list(df["SPED Status"].unique())
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
                        "Grade Level Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="stu-grade-level-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in list(sorted(df["GRADE_LEVEL"].unique()))
                        ],
                        multi=True,
                        value=[i for i in list(sorted(df["GRADE_LEVEL"].unique()))],
                        clearable=False,
                    ),
                    html.P(
                        "Grade Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="stu-grade-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in list(sorted(df["GRADE"].unique()))
                        ],
                        multi=True,
                        value=["D+", "D-", "F"],
                        clearable=False,
                    ),
                ]
            )

            layout = html.Div(
                [
                    dbc.Row(dbc.Col(html.Div([p2]))),
                    dbc.Row(
                        [
                            dbc.Col(filters, width="3"),
                            dbc.Col(sub_chart, width="9"),
                        ]
                    ),
                ]
            )
            return layout, sub_table
        elif tab == "tab-3":
            sub_chart = html.Div(
                html.Pre(
                    id="teacher-dist-chart",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )
            sub_table = html.Div(
                html.Pre(
                    id="teacher-dist-table",
                    style={"backgroundColor": ausd_colors["white"]},
                )
            )
            filters = html.Div(
                [
                    html.P(
                        "School Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="dist-school-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in list(sorted(df["SCHOOL"].unique()))
                        ],
                        value=[i for i in list(sorted(df["SCHOOL"].unique()))],
                        multi=True,
                        clearable=False,
                    ),
                    html.P(
                        "Course Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="course-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in ["all"] + list(sorted(df["COURSE_NAME"].unique()))
                        ],
                        multi=True,
                        placeholder="Select a course (type in box to search)",
                        clearable=False,
                        value=convert("all"),
                    ),
                    html.P(
                        "Grade Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="dist-grade-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in list(sorted(df["GRADE"].unique()))
                        ],
                        multi=True,
                        value=[i for i in list(sorted(df["GRADE"].unique()))],
                        clearable=False,
                    ),
                    html.P(
                        "Teacher Filter",
                        style={"color": ausd_colors["white"]},
                    ),
                    dcc.Dropdown(
                        id="teacher-picker",
                        options=[
                            {"label": i, "value": i}
                            for i in list(sorted(df["TEACHERNAME"].unique()))
                        ],
                        multi=True,
                        placeholder="Select a teacher (type in box to search)",
                        clearable=False,
                        # value=[i for i in list(sorted(df['TEACHERNAME'].unique()))]
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

    # tab 1 callbacks

    @app.callback(
        Output("grade-level-picker", "value"), Input("school-picker", "value")
    )
    def update_gradelevel(school):
        filtered_df = df.copy()
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
        else:
            school = convert(school)
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        return list(sorted(filtered_df["GRADE_LEVEL"].unique()))

    @app.callback(
        Output("grade-counts-chart", "children"),
        [
            Input("school-picker", "value"),
            Input("sped-picker", "value"),
            Input("eth-picker", "value"),
            Input("grade-picker", "value"),
            Input("grade-level-picker", "value"),
        ],
    )
    def update_grade_chart(school, sped, eth, grade, grade_level):
        filtered_df = df.copy()
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
        else:
            school = convert(school)
        if sped == "all":
            sped = list(filtered_df["SPED Status"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPED Status"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        filtered_df = filtered_df[filtered_df["GRADE"].isin(grade)]
        filtered_df = filtered_df[filtered_df["GRADE_LEVEL"].isin(grade_level)]
        return charts.grade_chart(filtered_df, grade)

    @app.callback(
        Output("grade-counts-table", "children"),
        [
            Input("f-counts", "clickData"),
            Input("school-picker", "value"),
            Input("sped-picker", "value"),
            Input("eth-picker", "value"),
            Input("grade-picker", "value"),
            Input("grade-level-picker", "value"),
        ],
    )
    def render_subchart(clickData, school, sped, eth, grade, grade_level):
        filtered_df = df.copy()
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
        else:
            school = convert(school)
        if sped == "all":
            sped = list(filtered_df["SPED Status"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPED Status"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        filtered_df = filtered_df[filtered_df["GRADE"].isin(grade)]
        filtered_df = filtered_df[filtered_df["GRADE_LEVEL"].isin(grade_level)]
        if clickData is not None:
            clickdata = clickData["points"][0]
            teachername = clickdata.get("x")
            grade = clickdata.get("customdata")
            grade = "".join(grade)
            filtered_df = filtered_df[filtered_df["TEACHERNAME"] == teachername]
            filtered_df = filtered_df[filtered_df["GRADE"] == grade]

            # return json.dumps(clickData), print(grade), print(teachername)
            return generate_table(filtered_df)
        else:
            return generate_table(filtered_df)

    # tab 2 callbacks

    @app.callback(
        Output("stu-grade-level-picker", "value"), Input("stu-school-picker", "value")
    )
    def update_gradelevel(school):
        filtered_df = df.copy()
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
        else:
            school = convert(school)
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        return list(sorted(filtered_df["GRADE_LEVEL"].unique()))

    @app.callback(
        Output("df-counts-text", "children"),
        [
            Input("stu-school-picker", "value"),
            Input("stu-sped-picker", "value"),
            Input("stu-eth-picker", "value"),
            Input("stu-grade-level-picker", "value"),
        ],
    )
    def update_stu_df_counts(school, sped, eth, grade_level):
        filtered_df = df.copy()
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
        else:
            school = convert(school)
        if sped == "all":
            sped = list(filtered_df["SPED Status"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPED Status"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        filtered_df = filtered_df[filtered_df["GRADE_LEVEL"].isin(grade_level)]
        return charts.stu_df_counts(filtered_df)

    @app.callback(
        Output("stu-grades-chart", "children"),
        [
            Input("stu-school-picker", "value"),
            Input("stu-sped-picker", "value"),
            Input("stu-eth-picker", "value"),
            Input("stu-grade-picker", "value"),
            Input("stu-grade-level-picker", "value"),
        ],
    )
    def update_stu_grade_chart(school, sped, eth, grade, grade_level):
        filtered_df = df.copy()
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
        else:
            school = convert(school)
        if sped == "all":
            sped = list(filtered_df["SPED Status"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPED Status"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        filtered_df = filtered_df[filtered_df["GRADE"].isin(grade)]
        filtered_df = filtered_df[filtered_df["GRADE_LEVEL"].isin(grade_level)]
        return charts.stu_grade_graph(filtered_df, grade)

    @app.callback(
        Output("stu-grades-table", "children"),
        [
            Input("stu-df-counts", "clickData"),
            Input("stu-school-picker", "value"),
            Input("stu-sped-picker", "value"),
            Input("stu-eth-picker", "value"),
            Input("stu-grade-picker", "value"),
            Input("stu-grade-level-picker", "value"),
        ],
    )
    def render_subchart(clickData, school, sped, eth, grades, grade_level):
        filtered_df = df.copy()
        if school == "all":
            school = list(filtered_df["SCHOOL"].unique())
        else:
            school = convert(school)
        if sped == "all":
            sped = list(filtered_df["SPED Status"].unique())
        else:
            sped = convert(sped)
        if eth == "all":
            eth = list(filtered_df["ETHNICITY_NAME"].unique())
        else:
            eth = convert(eth)
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        filtered_df = filtered_df[filtered_df["SPED Status"].isin(sped)]
        filtered_df = filtered_df[filtered_df["ETHNICITY_NAME"].isin(eth)]
        filtered_df = filtered_df[filtered_df["GRADE"].isin(grades)]
        if clickData is not None:
            clickdata = clickData["points"][0]
            key = clickdata.get("x")
            grade = clickdata.get("customdata")
            grade = "".join(grade)
            filtered_df = filtered_df[filtered_df["STUDENT_NUMBER"] == key]
            filtered_df = filtered_df[filtered_df["GRADE"] == grade]
            filtered_df = filtered_df[filtered_df["GRADE_LEVEL"].isin(grade_level)]
            return generate_table(filtered_df)
        else:
            return generate_table(filtered_df)

    # tab 3 callbacks

    @app.callback(
        Output("teacher-picker", "value"),
        [Input("dist-school-picker", "value"), Input("course-picker", "value")],
    )
    def update_teachers(school, course):
        filtered_df = df.copy()
        filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
        if course == convert("all"):
            return list(sorted(filtered_df["TEACHERNAME"].unique()))
        elif course is not None and course != convert("all"):
            filtered_df = filtered_df[filtered_df["COURSE_NAME"].isin(course)]
            return list(sorted(filtered_df["TEACHERNAME"].unique()))

    @app.callback(
        Output("teacher-dist-chart", "children"),
        [
            Input("teacher-picker", "value"),
            Input("course-picker", "value"),
            Input("dist-grade-picker", "value"),
            Input("dist-school-picker", "value"),
        ],
    )
    def update_teacher_distplot(teachername, course, gradelist, school):
        if course == convert("all"):
            course = list(sorted(df["COURSE_NAME"].unique()))
        if (
            teachername != list("")
            and course != list("")
            and course != convert("all")
            and gradelist != list("")
        ):
            filtered_df = df.copy()
            filtered_df = filtered_df[filtered_df["TEACHERNAME"].isin(teachername)]
            filtered_df = filtered_df[filtered_df["COURSE_NAME"].isin(course)]
            filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
            filtered_df = filtered_df[filtered_df["GRADE"].isin(gradelist)]
            filtered_df = (
                filtered_df.groupby("TEACHERNAME")["GRADE"]
                .value_counts()
                .reset_index(name="Grade Counts")
            )
            filtered_df["Grade Counts"] = filtered_df["Grade Counts"].astype(int)
            filtered_df = filtered_df.sort_values(by="TEACHERNAME", ascending=True)
            return charts.grade_distribution_by_teacher(filtered_df)

    @app.callback(
        Output("teacher-dist-table", "children"),
        [
            Input("teacher-dist-plot", "clickData"),
            Input("teacher-picker", "value"),
            Input("dist-grade-picker", "value"),
            Input("course-picker", "value"),
            Input("dist-school-picker", "value"),
        ],
    )
    def render_subchart(clickdata, teachername, gradelist, course, school):
        if course == convert("all"):
            course = list(sorted(df["COURSE_NAME"].unique()))
        if teachername and course is not None and course != convert("all"):
            filtered_df = df.copy()
            filtered_df = filtered_df[filtered_df["TEACHERNAME"].isin(teachername)]
            filtered_df = filtered_df[filtered_df["COURSE_NAME"].isin(course)]
            filtered_df = filtered_df[filtered_df["SCHOOL"].isin(school)]
            filtered_df = filtered_df[filtered_df["GRADE"].isin(gradelist)]
            filtered_df = filtered_df.sort_values(
                by=["TEACHERNAME", "COURSE_NAME"], ascending=True
            )
            if clickdata is not None:
                clickdata = clickdata["points"][0]
                key = clickdata.get("x")
                grade = clickdata.get("customdata")
                grade = "".join(grade)
                if key == grade:
                    filtered_df = filtered_df[filtered_df["GRADE"] == grade]
                else:
                    filtered_df = filtered_df[filtered_df["TEACHERNAME"] == key]
                    filtered_df = filtered_df[filtered_df["GRADE"] == grade]
                return generate_table(filtered_df)
            else:
                return generate_table(filtered_df)

    return layout
