"""
Example 1 - Storing Data in the Browser with a Hidden Div
Refer to: https://dash.plotly.com/sharing-data-between-callbacks
"""
# NOTE: This is really dumb.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def your_expensive_clean_or_compute_step(df):
    raise NotImplementedError()

def create_figure(dff):
    raise NotImplementedError()

def create_table(dff):
    raise NotImplementedError()

global_df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Table(id='table'),
    dcc.Dropdown(id='dropdown'),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])

@app.callback(Output('intermediate-value', 'children'), Input('dropdown', 'value'))
def clean_data(value):
    # some expensive clean data step
    cleaned_df = your_expensive_clean_or_compute_step(value)

    # more generally, this line would be
    # json.dumps(cleaned_df)
    return cleaned_df.to_json(date_format='iso', orient='split')

@app.callback(Output('graph', 'figure'), Input('intermediate-value', 'children'))
def update_graph(jsonified_cleaned_data):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    dff = pd.read_json(jsonified_cleaned_data, orient='split')

    figure = create_figure(dff)
    return figure

@app.callback(Output('table', 'children'), Input('intermediate-value', 'children'))
def update_table(jsonified_cleaned_data):
    dff = pd.read_json(jsonified_cleaned_data, orient='split')
    table = create_table(dff)
    return table


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
