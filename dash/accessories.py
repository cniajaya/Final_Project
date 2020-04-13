import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import seaborn as sns
import dash_table
from dash.dependencies import Input, Output, State


def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
    )

pro=pd.read_csv('accecsv.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1('Helmet Accessories Dashboard'),
        html.Div(children='''
        Created by: Celine Kurniajaya
    '''),
        dcc.Tabs(
            children=[
                dcc.Tab(
                    value='Tab1',
                    label='Customer Accessories Graph Example',
                    children=[
                        html.Div([
                            dcc.Graph(id='example-graph',
                                      figure={
                                          'data': [{
                                              'x': pro['Customer'],
                                              'y': pro['Other'],
                                              'type': 'bar',
                                              'name': 'Customer'}],
                                          'layout': {
                                              'title':
                                              'Helmet Accessories Customer Dash Data Visualization'
                                          }
                                      })
                        ])
                    ]),
                dcc.Tab(
                    value='Tab2',
                    label='Accessories Destination Graph Example',
                    children=[
                        html.Div([
                            dcc.Graph(id='example-graph2',
                                      figure={
                                          'data': [{
                                              'x': pro['Destination'],
                                              'y': pro['Other'],
                                              'type': 'violin',
                                              'name': 'Destination'
                                          }],
                                          'layout': {
                                              'title':
                                              'Helmet Accessories Destination Dash Data Visualization'
                                          }
                                      })
                        ])
                    ]),
                dcc.Tab(
                    value='Tab3',
                    label='Accessories Model/Type Graph Example',
                    children=[
                        html.Div([
                            dcc.Graph(id='example-graph3',
                                      figure={
                                          'data': [{
                                              'x': pro['Model/Type'],
                                              'y': pro['Other'],
                                              'type': 'violin',
                                              'name': 'Model/Type'
                                          }],
                                          'layout': {
                                              'title':
                                              'Helmet Accessories Model Dash Data Visualization'
                                          }
                                      })
                        ])
                    ]),
                dcc.Tab(
                    value='Tab4',
                    label='Accessories Year Graph Example',
                    children=[
                        html.Div([
                            dcc.Graph(id='example-graph4',
                                      figure={
                                          'data': [{
                                              'x': pro['Receive Year'],
                                              'y': pro['Other'],
                                              'type': 'bar',
                                              'name': 'Receive Year'}],
                                          'layout': {
                                              'title':
                                              'Accessories Year Dash Data Visualization'
                                          }
                                      })
                        ])
                    ]),
                dcc.Tab(value='Tab5',
                        label='Data Frame Grand Total',
                        children=[
                            html.Div(children=[
                                html.Div([
                                    html.P('Customer'),
                                    dcc.Dropdown(value='',
                                                 id='filter-customer',
                                                 options=[{'label': i,'value': i} for i in pro['Customer'].unique()])
                                ],
                                         className='col-3'),
                                
                                html.Div([
                                    html.P('Destination'),
                                    dcc.Dropdown(value='',
                                                 id='filter-destination',
                                                 options=[{'label': i,'value': i} for i in pro['Destination'].unique()])
                                ],
                                         className='col-3'),
                                html.Div([
                                    html.P('Model/Type'),
                                    dcc.Dropdown(value='',
                                                 id='filter-model',
                                                 options=[{'label': i,'value': i} for i in pro['Model/Type'].unique()])
                                ],
                                         className='col-3'),
                                html.Div([
                                    html.P('Delivery Year'),
                                    dcc.Dropdown(value='',
                                                 id='filter-year',
                                                 options=[{'label': i,'value': i} for i in pro['Delivery Year'].unique()])
                                ],
                                        className='col-3'),
                                html.Div([
                                    html.P('Receive Year'),
                                    dcc.Dropdown(value='',
                                                 id='filter-year2',
                                                 options=[{'label': i,'value': i} for i in pro['Receive Year'].unique()])
                                ],
                                        className='col-3'),
                            ],
                                     className='row'),
                            html.Br(),
                            html.Div([
                                html.P('Max Rows:'),
                                dcc.Input(id ='filter-row',
                                          type = 'number', 
                                          value = 10)
                            ], className = 'row col-3'),

                            html.Div(children =[
                                    html.Button('search',id = 'filter')
                             ],className = 'row col-4'),
                             
                            html.Div(id='div-table',
                                     children=[generate_table(pro)])
                        ])
            ],
            ## Tabs Content Style
            content_style={
                'fontFamily': 'Arial',
                'borderBottom': '1px solid #d6d6d6',
                'borderLeft': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'padding': '44px'
            })
    ],
    #Div Paling luar Style
    style={
        'maxWidth': '1200px',
        'margin': '0 auto'
    })


@app.callback(
    Output(component_id = 'div-table', component_property = 'children'),
    [Input(component_id = 'filter', component_property = 'n_clicks')],
    [State(component_id = 'filter-row', component_property = 'value'),
    State(component_id = 'filter-customer', component_property = 'value'),
    State(component_id = 'filter-destination', component_property = 'value'),
    State(component_id = 'filter-model', component_property = 'value'),
    State(component_id = 'filter-year', component_property = 'value'),
    State(component_id = 'filter-year2', component_property = 'value')
    ]
)

def update_table(n_clicks, row, customer, destination, model, Year, year2):
    pro=pd.read_csv('accecsv.csv')
    if customer != '':
        pro = pro[pro['Customer'] == customer]
    if destination != '':
        pro = pro[pro['Destination'] == destination]
    if model != '':
       pro = pro[pro['Model/Type'] == model]
    if Year != '':
       pro = pro[pro['Delivery Year'] == Year]
    if year2 != '':
       pro = pro[pro['Receive Year'] == year2]
    children = [generate_table(pro, page_size = row)]
    return children

if __name__ == '__main__':
    app.run_server(debug=True)