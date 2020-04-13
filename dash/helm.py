import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
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

pro=pd.read_csv('kmean.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

test_png = 'myimage.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

app.layout = html.Div(
    children=[
        html.H1('Helmet Dashboard'),
        html.Div(children='''
        Made by: Celine Kurniajaya
    '''),
        dcc.Tabs(
            children=[
                dcc.Tab(
                    value='Tab1',
                    label='Helmet Customer Segmentation',
                    children=[
                        html.Div([
                            html.Img(src='data:image/png;base64,{}'.format(test_base64))
                        ])
                    ]),
                dcc.Tab(
                    value='Tab2',
                    label='Modification Scatter chart',
                    children=[
                        html.Div(children=dcc.Graph(
                            id='graph-scatter',
                            figure={
                                'data': [
                                    go.Scatter(x=pro[pro['Modification'] == i]['Time Differences'],
                                               y=pro[pro['Modification'] == i]
                                               ['Total Helmet'],
                                               mode='markers',
                                               name='Modification {}'.format(i))
                                    for i in pro['Modification'].unique()
                                ],
                                'layout':
                                go.Layout(
                                    xaxis={'title': 'Time Differences'},
                                    yaxis={'title': 'Total Helmet'},
                                    title='Modification Dash Scatter Visualization',
                                    hovermode='closest')
                            }))
                    ]),
                dcc.Tab(value='Tab3',
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
                                    html.P('Receive Year'),
                                    dcc.Dropdown(value='',
                                                 id='filter-thn',
                                                 options=[{'label': i,'value': i} for i in pro['Receive Year'].unique()])
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
                                    html.P('Cluster'),
                                    dcc.Dropdown(value='',
                                                 id='filter-cluster',
                                                 options=[{'label': i,'value': i} for i in pro['Category'].unique()])
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
                'fontFamily': 'Lucida Console',
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
    State(component_id = 'filter-thn', component_property = 'value'),
    State(component_id = 'filter-year', component_property = 'value'),
    State(component_id = 'filter-cluster', component_property = 'value')
    ]
)

def update_table(n_clicks, row, customer, destination, Year1, Year,Category):
    pro=pd.read_csv('kmean.csv')
    if customer != '':
        pro = pro[pro['Customer'] == customer]
    if destination != '':
        pro = pro[pro['Destination'] == destination]
    if Year1 != '':
       pro = pro[pro['Receive Year'] == Year1]
    if Year != '':
       pro = pro[pro['Delivery Year'] == Year]
    if Category != '':
       pro = pro[pro['Category'] == Category]
    children = [generate_table(pro, page_size = row)]
    return children

if __name__ == '__main__':
    app.run_server(debug=True)