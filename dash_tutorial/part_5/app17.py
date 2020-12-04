"""
Example 2 - Computing Aggregations Upfront
Refer to: https://dash.plotly.com/sharing-data-between-callbacks
"""
# NOTE: This is also quite dumb.

import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def your_expensive_clean_or_compute_step(df):
    raise NotImplementedError()

def create_figure_1(dff):
    raise NotImplementedError()

def create_figure_2(dff):
    raise NotImplementedError()

def create_figure_3(dff):
    raise NotImplementedError()

global_df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Table(id='table'),
    dcc.Dropdown(id='dropdown'),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})
])

@app.callback(
    Output('intermediate-value', 'children'),
    Input('dropdown', 'value'))
def clean_data(value):
    # an expensive query step
    cleaned_df = your_expensive_clean_or_compute_step(value)

    # a few filter steps that compute the data
    # as it's needed in the future callbacks
    df_1 = cleaned_df[cleaned_df['fruit'] == 'apples']
    df_2 = cleaned_df[cleaned_df['fruit'] == 'oranges']
    df_3 = cleaned_df[cleaned_df['fruit'] == 'figs']

    datasets = {
        'df_1': df_1.to_json(orient='split', date_format='iso'),
        'df_2': df_2.to_json(orient='split', date_format='iso'),
        'df_3': df_3.to_json(orient='split', date_format='iso'),
    }

    return json.dumps(datasets)

@app.callback(
    Output('graph', 'figure'),
    Input('intermediate-value', 'children'))
def update_graph_1(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets['df_1'], orient='split')
    figure = create_figure_1(dff)
    return figure

@app.callback(
    Output('graph', 'figure'),
    Input('intermediate-value', 'children'))
def update_graph_2(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets['df_2'], orient='split')
    figure = create_figure_2(dff)
    return figure

@app.callback(
    Output('graph', 'figure'),
    Input('intermediate-value', 'children'))
def update_graph_3(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    dff = pd.read_json(datasets['df_3'], orient='split')
    figure = create_figure_3(dff)
    return figure


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
