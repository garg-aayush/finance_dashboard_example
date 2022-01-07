# Import required libraries

# Import the required packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from utils import get_single_stock, check_dir
from pathlib import Path

app = dash.Dash(__name__)
server = app.server

#########################################
# Global variables and constants
#########################################
# port
port = 3000

# dir path to download and save the stock data
datadir = './data/'
# time period
period = '1y'
# file containing all the NS symbols
file_symbols = 'symbols_ns.csv'

# plot parameters
margin = dict(l=25, r=25, t=30, b=5, pad=0)
transition_duration = 300
# yaxis [min, max] -> [perc[0] * stock_min, perc[1] * stock_max]
ylims_perc = [0.95, 1.05]

# xaxis [min, max] : [min_date, max_date]
df = pd.read_csv('sample_stock.csv')
date_range = [df['Date'].min(), df['Date'].max()]
del df

# Create necessary variables and data folder
# load all the symbols in the memory
print('Read all the available NSE symbols from {}'.format(file_symbols))
df_symbols = pd.read_csv(file_symbols)

#########################################
# Helper functions
#########################################


def make_plot_data(df, graph_name='Close', chart_name=['StockPrice'], days=10):

    data = []
    for cname in chart_name:
        if cname == 'StockPrice':
            data.append(go.Scatter(
                                    x=df['Date'],
                                    y=df[graph_name],
                                    name=cname,
                                    line=dict(color="#332f2f", width=1.5)
                                    )
                        )
        if cname == 'Candlestick':
            data.append(go.Candlestick(
                                        x=df['Date'],
                                        open=df['Open'], high=df['High'],
                                        low=df['Low'], close=df['Close'],
                                        name=cname
                                        )
                        )
        if cname == 'SimpleMovingAverage':
            data.append(go.Scatter(
                                    x=df['Date'],
                                    y=df[graph_name].rolling(days).mean(),
                                    name=cname,
                                    line=dict(color="#2424ed",
                                              width=2.5, dash='dot')
                                    )
                        )

    return data


def make_graph(data, xaxis_title='Date', yaxis_limits=[0, 1000],
                xaxis_limits=[], legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.03, orientation='h')):

    fig = go.Figure(data)
    fig.update_layout(margin=margin,
                      transition_duration=transition_duration,
                      xaxis_rangeslider_visible=False,
                      #xaxis_title=xaxis_title,
                      yaxis_range=yaxis_limits,
                      xaxis_range=xaxis_limits,
                      plot_bgcolor="#F9F9F9",
                      paper_bgcolor="#F9F9F9",
                      # showlegend=False,
                      legend=legend
                        )

    fig.update_xaxes(color="#323232",showgrid=True, gridcolor="white")
    fig.update_yaxes(color="#323232",showgrid=True, gridcolor="white")
    return fig


# Create app layout
app.layout= html.Div(
    [
        # dcc.Store(id='aggregate_data'),

        # Title
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'Multiple stocks price analysis',

                        ),
                    ],

                    className='eight columns'
                )
            ],
            id="header",
            className='row',
        ),

        # Options
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            'Stock Price:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='stock-price',
                            options=[{'label': 'Open ', 'value': 'Open'},
                                     {'label': 'Close', 'value': 'Close'},
                                     {'label': 'Low', 'value': 'Low'},
                                     {'label': 'High', 'value': 'High'}
                                     ],
                            value='Close',
                            # labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        )
                    ],
                    className='pretty_container three columns'
                ),

                html.Div(
                    [
                        html.H6(
                            'Chart Type:',
                            className="control_label"
                        ),
                        dcc.Checklist(
                            id='chart-type',
                            options=[{'label': 'Stock Price', 'value': 'StockPrice'},
                                     {'label': 'Candlestick',
                                      'value': 'Candlestick'},
                                     {'label': 'Simple moving average',
                                      'value': 'SimpleMovingAverage'}
                                     ],
                            value=['StockPrice'],
                            # labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        )
                    ],
                    className='pretty_container four columns'
                ),

                html.Div(
                    [
                        html.H6('Moving average Length (in Days):',
                                className="control_label"
                                ),
                        html.Br(),
                        dcc.Slider(id='days',
                                   min=1,
                                   max=50,
                                   marks={i: '{}'.format(i) if i == 1 else str(i)
                                          for i in [1, 5, 10, 20, 30, 40, 50]},
                                   value=10,
                                   className="dcc_control"
                                   )
                    ],
                    className='pretty_container five columns'
                )
            ],
            className='row'
        ),

        # Graphs
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            id="drop_text-1",
                            className="info_text"
                        ),
                        dcc.Dropdown(
                            id='drop-1',
                            options=[{'label': s, 'value': s}
                                     for s in df_symbols['Symbol']
                                     ],
                            value=df_symbols['Symbol'][0],
                        )
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        html.H6(
                            id="drop_text-2",
                            className="info_text"
                        ),
                        dcc.Dropdown(
                            id='drop-2',
                            options=[{'label': s, 'value': s}
                                     for s in df_symbols['Symbol']
                                     ],
                            value=df_symbols['Symbol'][1],
                        )
                    ],
                    className='pretty_container six columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        # dcc.Graph(id='main_graph')
                        dcc.Graph(id='stock-1')
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='stock-2')
                    ],
                    className='pretty_container six columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            id="drop_text-3",
                            className="info_text"
                        ),
                        dcc.Dropdown(
                            id='drop-3',
                            options=[{'label': s, 'value': s}
                                     for s in df_symbols['Symbol']
                                     ],
                            value=df_symbols['Symbol'][2],
                        )
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        html.H6(
                            id="drop_text-4",
                            className="info_text"
                        ),
                        dcc.Dropdown(
                            id='drop-4',
                            options=[{'label': s, 'value': s}
                                     for s in df_symbols['Symbol']
                                     ],
                            value=df_symbols['Symbol'][3],
                        )
                    ],
                    className='pretty_container six columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='stock-3')
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='stock-4')
                    ],
                    className='pretty_container six columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            id="drop_text-5",
                            className="info_text"
                        ),
                        dcc.Dropdown(
                            id='drop-5',
                            options=[{'label': s, 'value': s}
                                     for s in df_symbols['Symbol']
                                     ],
                            value=df_symbols['Symbol'][4],
                        )
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        html.H6(
                            id="drop_text-6",
                            className="info_text"
                        ),
                        dcc.Dropdown(
                            id='drop-6',
                            options=[{'label': s, 'value': s}
                                     for s in df_symbols['Symbol']
                                     ],
                            value=df_symbols['Symbol'][5],
                        )
                    ],
                    className='pretty_container six columns',
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='stock-5')
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='stock-6')
                    ],
                    className='pretty_container six columns',
                ),
            ],
            className='row'
        )
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)

###################################################
# callbacks
###################################################
# call back, stock-1
@ app.callback(
    Output('stock-1', 'figure'),
    [Input('drop-1', 'value'),
     Input('stock-price', 'value'),
     Input('chart-type', 'value'),
     Input('days', 'value')
     ]
)
def update_figure(symbol, graph_name, chart_name, days_num):
    df = get_single_stock(symbol, period=period, datadir=datadir)

    # make plot data
    data = make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits = [ylims_perc[0]*df['Low'].min(), ylims_perc[1]*df['High']]
    return make_graph(data, yaxis_limits=yaxis_limits, xaxis_limits=date_range)

# call back, stock-2
@ app.callback(
    Output('stock-2', 'figure'),
    [Input('drop-2', 'value'),
     Input('stock-price', 'value'),
     Input('chart-type', 'value'),
     Input('days', 'value')
     ]
)
def update_figure(symbol, graph_name, chart_name, days_num):
    df=get_single_stock(symbol, period=period, datadir=datadir)
    
    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits= [ylims_perc[0]*df['Low'].min(), ylims_perc[1]*df['High']]
    return make_graph(data, yaxis_limits=yaxis_limits, xaxis_limits=date_range)


# call back, stock-3
@ app.callback(
    Output('stock-3', 'figure'),
    [Input('drop-3', 'value'),
     Input('stock-price', 'value'),
     Input('chart-type', 'value'),
     Input('days', 'value')
     ]
)
def update_figure(symbol, graph_name, chart_name, days_num):
    df=get_single_stock(symbol, period=period, datadir=datadir)

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits= [ylims_perc[0]*df['Low'].min(), ylims_perc[1]*df['High']]
    return make_graph(data, yaxis_limits=yaxis_limits, xaxis_limits=date_range)


# call back, stock-4
@ app.callback(
    Output('stock-4', 'figure'),
    [Input('drop-4', 'value'),
     Input('stock-price', 'value'),
     Input('chart-type', 'value'),
     Input('days', 'value')
     ]
)
def update_figure(symbol, graph_name, chart_name, days_num):
    df=get_single_stock(symbol, period=period, datadir=datadir)

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits= [ylims_perc[0]*df['Low'].min(), ylims_perc[1]*df['High']]
    return make_graph(data, yaxis_limits=yaxis_limits, xaxis_limits=date_range)


# call back, stock-5
@ app.callback(
    Output('stock-5', 'figure'),
    [Input('drop-5', 'value'),
     Input('stock-price', 'value'),
     Input('chart-type', 'value'),
     Input('days', 'value')
     ]
)
def update_figure(symbol, graph_name, chart_name, days_num):
    df=get_single_stock(symbol, period=period, datadir=datadir)

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits= [ylims_perc[0]*df['Low'].min(), ylims_perc[1]*df['High']]
    return make_graph(data, yaxis_limits=yaxis_limits, xaxis_limits=date_range)


# call back, stock-6
@ app.callback(
    Output('stock-6', 'figure'),
    [Input('drop-6', 'value'),
     Input('stock-price', 'value'),
     Input('chart-type', 'value'),
     Input('days', 'value')
     ]
)
def update_figure(symbol, graph_name, chart_name, days_num):
    df=get_single_stock(symbol, period=period, datadir=datadir)

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits= [ylims_perc[0]*df['Low'].min(), ylims_perc[1]*df['High']]
    return make_graph(data, yaxis_limits=yaxis_limits, xaxis_limits=date_range)


# Main
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True, port=3000)
