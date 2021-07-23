from dash.dependencies import Input, Output
import dash_table

ausd_colors = {
    'dark-blue-grey': 'rgb(62, 64, 76)',
    'medium-blue-grey': 'rgb(77, 79, 91)',
    'superdark-green': 'rgb(41, 56, 55)',
    'dark-green': 'rgb(57, 81, 85)',
    'medium-green': 'rgb(93, 113, 120)',
    'light-green': 'rgb(186, 218, 212)',
    'pink-red': 'rgb(255, 101, 131)',
    'dark-pink-red': 'rgb(247, 80, 99)',
    'white': 'rgb(251, 251, 252)',
    'light-grey': 'rgb(208, 206, 206)',
    'bright-red': 'rgb(255,3,3)',
    'dark-red': 'rgb(186,0,0)',
    'black': 'rgb(0,0,0)',
    'background': '#111111',
    'text': '#7FDBFF'
}

def convert(string):
    li = list(string.split('`'))
    return li


def generate_table(df, max_rows=100):
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns],
        data=df.to_dict('records'),
        style_header={'backgroundColor': ausd_colors['black']},
        style_cell={
            'backgroundColor': ausd_colors['black'],
            'color': 'white'
        },
        style_data={
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            "whiteSpace": 'normal',
            'height': 'auto',
            'color': 'white',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_filter={
            'backgroundColor': 'white',
            'color': 'black',
        },
        filter_action="native",
        sort_action="native",
        column_selectable="multi",
        row_selectable="multi",
        selected_columns=[],
        selected_rows=[],
        page_size=100,

        style_table={'minHeight': '600px', 'maxHeight': '1000px',
                     'height': '1000px', 'overflowY': 'scroll'},
        fixed_rows={'headers': True},
        export_format='xlsx',
        export_headers='display'
    )

def generate_stu_subtable(df, value):
    dff = df.copy(deep=True)
    dff = dff[dff['STUDENT_NUMBER'] == value]
    dff = dff.sort_values(by='GRADE', ascending=False)
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i, "selectable": True, "deletable": True} for i in dff.columns],
        data=dff.to_dict('records'),
        style_header={'backgroundColor': ausd_colors['black']},
        style_cell={
            'backgroundColor': ausd_colors['black'],
            'color': 'white'
        },
        style_data={
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            "whiteSpace": 'normal',
            'height': 'auto',
            'color': 'white',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_filter={
            'backgroundColor': 'white',
            'color': 'black',
        },
        filter_action="native",
        sort_action="native",
        column_selectable="multi",
        row_selectable="multi",
        selected_columns=[],
        selected_rows=[],
        page_size=100,

        style_table={'minHeight': '600px', 'maxHeight': '1000px',
                     'height': '1000px', 'overflowY': 'scroll'},
        fixed_rows={'headers': True},
        export_format='xlsx',
        export_headers='display'
    )