import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff


def grade_chart(df, grades):
    countf = df.copy(deep=True)
    countf = countf.loc[countf['GRADE'].isin(grades)]
    countf = countf.groupby('TEACHERNAME')['GRADE'].value_counts().reset_index(name='Grade Counts')
    gradelist = list(sorted(countf['GRADE'].unique()))
    countf = countf.sort_values(by='Grade Counts', ascending=False)
    fig = px.scatter(countf, x='TEACHERNAME', y='Grade Counts', size='Grade Counts', color='GRADE',
                     custom_data=['GRADE'],
                     category_orders={"GRADE": gradelist},
                     color_discrete_map={
                         "F": "red",
                         "D+": "green",
                         "D-": "chartreuse",
                         "A+": "blue",
                         "A": "aqua",
                         "A-": "cadetblue",
                         "B+": "magenta",
                         "B": "blueviolet",
                         "B-": "darkmagenta",
                         "C+": "mistyrose",
                         "C": "moccasin",
                         "C-": "navajowhite"
                     },
                     title='Grade Counts Per Teacher \
                     Click On a Point to See the Data below')
    fig.update_layout(autosize=True)
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(ticklabelposition='inside top')
    # fig.update(layout_coloraxis_showscale=False)
    graph = dcc.Graph(
        id='f-counts',
        figure=fig
    )
    return graph


def stu_df_counts(df):
    countdf = df.copy(deep=True)
    countdf['GRADE'] = countdf['GRADE'].str.replace('+', '')
    countdf['GRADE'] = countdf['GRADE'].str.replace('-', '')
    countdf['GRADE'] = countdf['GRADE'].str.replace('D', 'F')
    countdf = countdf.loc[countdf['GRADE'].str.contains('F')]
    countdf = countdf['STUDENT_NUMBER'].nunique()
    countdf = str(countdf)
    return "The Number of students with a D or F is : " + countdf


def stu_nc_counts(df):
    countdf = df.copy(deep=True)
    countdf = countdf.loc[countdf['GRADE'].str.contains('NC')]
    countdf = countdf['STUDENT_NUMBER'].nunique()
    countdf = str(countdf)
    return countdf


def stu_grade_graph(df, grades):
    countdf = df.copy(deep=True)
    countdf = countdf.loc[countdf['GRADE'].isin(grades)]
    countdf = countdf.groupby('STUDENT_NUMBER')['GRADE'].value_counts().reset_index(name='Grade Counts')
    gradelist = list(sorted(countdf['GRADE'].unique()))
    countdf = countdf.sort_values(by='Grade Counts', ascending=False)
    fig = px.scatter(countdf, x='STUDENT_NUMBER', y='Grade Counts', size='Grade Counts', color='GRADE',
                     custom_data=['GRADE'],
                     category_orders={"GRADE": gradelist},
                     color_discrete_map={
                         "F": "red",
                         "D+": "green",
                         "D-": "chartreuse",
                         "A+": "blue",
                         "A": "aqua",
                         "A-": "cadetblue",
                         "B+": "magenta",
                         "B": "blueviolet",
                         "B-": "darkmagenta",
                         "C+": "mistyrose",
                         "C": "moccasin",
                         "C-": "navajowhite"
                     },
                     title='Grade Counts Per Student')
    fig.update_layout(autosize=True)
    # fig.update_xaxes(tickangle=45)
    fig.update(layout_coloraxis_showscale=False)
    fig.update_yaxes(ticklabelposition='inside top')
    graph = dcc.Graph(
        id='stu-df-counts',
        figure=fig
    )
    return graph


def incichart(df):
    count = df.copy(deep=True)
    count = count['Behavior'].value_counts().reset_index(name='Behavior Counts')
    count = count.rename(columns={'index': 'Behavior'})
    count = count[['Behavior', 'Behavior Counts']]
    fig = px.scatter(count, x='Behavior', y='Behavior Counts', size='Behavior Counts', title='Behavior Counts',
                     color='Behavior Counts',
                     color_continuous_scale='balance')
    fig.update_layout(autosize=True)
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(ticklabelposition='inside top')
    fig.update(layout_coloraxis_showscale=False)
    graph = dcc.Graph(
        id='behavior-counts',
        figure=fig
    )
    return graph


def inci_action_chart(df):
    count = df.copy(deep=True)
    count = count['Action'].value_counts().reset_index(name='Action Counts')
    count = count.rename(columns={'index': 'Action'})
    count = count[['Action', 'Action Counts']]
    fig = px.scatter(count, x='Action', y='Action Counts', size='Action Counts', color='Action Counts',
                     color_continuous_scale='balance',
                     title='Action Counts')
    fig.update_layout(autosize=True)
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(ticklabelposition='inside top')
    fig.update(layout_coloraxis_showscale=False)
    graph = dcc.Graph(
        id='action-counts',
        figure=fig
    )
    return graph


def attendance_code_chart(df, year, school, sped, eth, present):
    filtered_df = df[df['School_Year'].isin(year)]
    filtered_df = filtered_df[filtered_df['SCHOOL'].isin(school)]
    filtered_df = filtered_df[filtered_df['SPECIAL_ED_STUDENT'].isin(sped)]
    filtered_df = filtered_df[filtered_df['ETHNICITY_NAME'].isin(eth)]
    filtered_df = filtered_df[filtered_df['PRESENCE_STATUS_CD'].isin(present)]
    count = filtered_df.copy(deep=True)
    count = count['ATT_CODE'].value_counts().reset_index(name='Code Counts')
    count = count.rename(columns={'index': 'ATT_CODE'})
    count = count[['ATT_CODE', 'Code Counts']]
    fig = px.scatter(count, x='ATT_CODE', y='Code Counts', size='Code Counts', color='Code Counts',
                     color_continuous_scale='balance',
                     title='Code Counts')
    fig.update_layout(autosize=True)
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(ticklabelposition='inside top')
    fig.update(layout_coloraxis_showscale=False)
    graph = dcc.Graph(
        id='code-counts',
        figure=fig
    )
    return graph


def student_attendance_code_chart(df):
    filtered_df = df.copy(deep=True)
    gradedf = filtered_df.copy(deep=True)
    gradedf = gradedf[['STUDENT_NUMBER', 'LASTFIRST', 'CURRENT_GRADE_LEVEL']]
    gradedf = gradedf.drop_duplicates('STUDENT_NUMBER')
    filtered_df = filtered_df.groupby('STUDENT_NUMBER')['ATT_CODE'].value_counts().reset_index(name='Code Counts')
    filtered_df = filtered_df[['STUDENT_NUMBER', 'Code Counts']]
    filtered_df = pd.merge(gradedf, filtered_df, on='STUDENT_NUMBER')
    filtered_df = filtered_df.sort_values(by=['CURRENT_GRADE_LEVEL', 'Code Counts'], ascending=False)
    filtered_df['CURRENT_GRADE_LEVEL'] = filtered_df['CURRENT_GRADE_LEVEL'].astype(str)
    fig = px.scatter(filtered_df, x='STUDENT_NUMBER', y='Code Counts', size='Code Counts', color='CURRENT_GRADE_LEVEL',
                     hover_data=['LASTFIRST'],
                     # color_discrete_sequence='',
                     title='Code Counts')
    fig.update_layout(autosize=True)
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(ticklabelposition='inside top')
    fig.update(layout_coloraxis_showscale=False)
    graph = dcc.Graph(
        id='stu-code-counts',
        figure=fig
    )
    return graph


# distribution charts

def grade_distribution_by_teacher(filtered_df):
    gradelist = list(sorted(filtered_df['GRADE'].unique()))
    fig = px.scatter(filtered_df, x='TEACHERNAME', y='Grade Counts', color='GRADE', marginal_y='box',
                     hover_data=filtered_df.columns,
                     category_orders={"GRADE": gradelist},
                     color_discrete_map={
                         "F": "red",
                         "D+": "green",
                         "D-": "chartreuse",
                         "A+": "blue",
                         "A": "aqua",
                         "A-": "cadetblue",
                         "B+": "magenta",
                         "B": "blueviolet",
                         "B-": "darkmagenta",
                         "C+": "mistyrose",
                         "C": "moccasin",
                         "C-": "navajowhite",
                         "CR": "yellow",
                         "I": "yellowgreen",
                         "NC": "teal",
                         "NM": "tomato"
                     },
                     title='Teacher Grade Distribution (double click on grade to filter to it)')
    graph = dcc.Graph(
        id='teacher-dist-plot',
        figure=fig
    )
    return graph
