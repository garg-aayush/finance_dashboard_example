# App to view particular stock price over the last 1 year

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from utils import download_single_stock, write_csv, make_abspath
from pathlib import Path

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__)

# read all the stocks data in dict of dfs
datadir = './data/'
margin = dict(l=25, r=25, t=30, b=5, pad=0)
transition_duration = 300

df = pd.read_csv(datadir + 'sample_stock.csv')
date_range = [df['Date'].min(), df['Date'].max()]
print(date_range)
del df

# read all symbols
df_symbols = pd.read_csv(datadir + 'symbols_ns.csv')

# make helper functions


def fig_update_layout(fig):
    fig.update_layout(
        margin=dict(l=20, r=25, t=30, b=5, pad=10, height=400))


def get_single_stock(symbol, period='1y', datadir='./data/'):
    # filename
    stock_file = datadir + symbol + '.NS'

    # make absolute path
    stock_file = make_abspath(stock_file)

    # check if the file exists
    if Path(stock_file).exists():
        print('Load {}'.format(stock_file))
        df = pd.read_csv(stock_file)
    else:
        print('Download {} stock data'.format(symbol))
        df = download_single_stock(symbol + '.NS', period=period)
        # print(df.head())
        write_csv(df, stock_file)
        df = pd.read_csv(stock_file)

    return df


def make_fig(df_dict, name='', x="Date", y="Close"):
    fig = px.line(df_dict[name], x=x, y=y, title=name)
    return fig


# def make_line_graph(df, x="Date", y="Close"):
#     fig = px.line(df, x=x, y=y)
#     fig.update_layout(margin=margin,
#                       transition_duration=transition_duration)
#     return fig

def make_line_graph(df, x="Date", y="Close"):
    data = go.Scatter(x=df[x], y=df[y])
    fig = go.Figure(data)
    fig.update_layout(margin=margin,
                      transition_duration=transition_duration,
                      xaxis_rangeslider_visible=False,
                      xaxis_title='Date')
    return fig


def make_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'], high=df['High'],
                                         low=df['Low'], close=df['Close'],
                                         )
                          ])
    fig.update_layout(margin=margin,
                      transition_duration=transition_duration,
                      xaxis_rangeslider_visible=False,
                      xaxis_title='Date')
    return fig


def make_plot_data(df, graph_name='Close', chart_name=['StockPrice'], days=10):
    data = []
    for cname in chart_name:
        if cname == 'StockPrice':
            data.append(go.Scatter(
                x=df['Date'], y=df[graph_name], name=cname, line=dict(color='black', width=1)))
        if cname == 'Candlestick':
            data.append(go.Candlestick(x=df['Date'],
                                        open=df['Open'], high=df['High'],
                                        low=df['Low'], close=df['Close'],
                                        name=cname
                                        )
                        )
        if cname == 'SimpleMovingAverage':
            data.append(go.Scatter(
                x=df['Date'], y=df[graph_name].rolling(days).mean(), name=cname, line=dict(color='blue', width=1.5, dash='dot')))
    return data


def make_graph(data, yaxis_limits=[0, 1000], xaxis_limits=[]):
    fig = go.Figure(data)
    fig.update_layout(margin=margin,
                      transition_duration=transition_duration,
                      xaxis_rangeslider_visible=False,
                      xaxis_title='Date',
                      yaxis_range=yaxis_limits,
                      xaxis_range=xaxis_limits,
                      # showlegend=False,
                      legend=dict(yanchor="top",
                                y=0.99,
                                xanchor="left",
                                x=0.03)
                        )
    return fig

###################################################
# App layout
###################################################


app.layout = html.Div(className='row', children=[

    html.Div([
        html.Div([
            html.H5('Multiple stocs price view'),
        ], style={'width': '100%', 'display': 'inline-block'}
        )
    ]),

    html.Div([
        html.Div([
            # html.H4('Multiple Price stock view'),
            # html.Hr(),
            html.Label("Stock price"),
            dcc.RadioItems(
                id='stock-price',
                options=[{'label': 'Open ', 'value': 'Open'},
                         {'label': 'Close', 'value': 'Close'},
                         {'label': 'Low', 'value': 'Low'},
                         {'label': 'High', 'value': 'High'}
                         ],
                value='Close',
                labelStyle={'display': 'inline-block', 'margin-right': '5px'},
                inputStyle={'margin-right': '5px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding-bottom': '-30px'}
        ),

        html.Div([
            # html.H4('Multiple Price stock view'),
            # html.Hr(),
            html.Label("Chart Type"),
            dcc.Checklist(
                id='chart-type',
                options=[{'label': 'Stock Price', 'value': 'StockPrice'},
                         {'label': 'Candlestick', 'value': 'Candlestick'},
                         {'label': 'Simple moving average',
                             'value': 'SimpleMovingAverage'}
                         ],
                value=['StockPrice'],
                labelStyle={'display': 'inline-block',
                            'margin-right': '5px'},
                inputStyle={'margin-right': '5px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding-bottom': '-30px'}
        ),

        html.Div([
            html.Label('Moving average Length (in Days)'),
            dcc.Slider(
                id='days',
                min=1,
                max=50,
                marks={i: 'Label {}'.format(i) if i == 1 else str(i)
                        for i in [1,5,10,20,30,40,50]},
                value=10
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding-bottom': '-30px'}
        ),

        #html.Hr()
    ]),


    html.Div([
        dcc.Dropdown(
            id='drop-1',
            options=[{'label': s, 'value': s}
                     for s in df_symbols['Symbol']
                     ],
            value=df_symbols['Symbol'][0],
        )
    ],
        style={'width': '32%', 'display': 'inline-block', 'padding': '5px 3px'}
    ),

    html.Div([
        dcc.Dropdown(
            id='drop-2',
            options=[{'label': s, 'value': s}
                     for s in df_symbols['Symbol']
                     ],
            value=df_symbols['Symbol'][1],
        )
    ],
        style={'width': '32%', 'display': 'inline-block', 'padding': '5px 3px'}
    ),


    html.Div([
        dcc.Dropdown(
            id='drop-3',
            options=[{'label': s, 'value': s}
                     for s in df_symbols['Symbol']
                     ],
            value=df_symbols['Symbol'][2],
        )
    ],
        style={'width': '32%', 'display': 'inline-block', 'padding': '5px 3px'}
    ),

    html.Div([
        dcc.Graph(id='stock-1')
    ], style={'width': '32%', 'display': 'inline-block', }),

    html.Div([
        dcc.Graph(id='stock-2')
    ], style={'width': '32%', 'display': 'inline-block', }),

    html.Div([
        dcc.Graph(id='stock-3')
    ], style={'width': '32%', 'display': 'inline-block', }),


    html.Div([
        dcc.Dropdown(
            id='drop-4',
            options=[{'label': s, 'value': s}
                     for s in df_symbols['Symbol']
                     ],
            value=df_symbols['Symbol'][3],
        )
    ],
        style={'width': '32%', 'display': 'inline-block', 'padding': '5px 3px'}
    ),

    html.Div([
        dcc.Dropdown(
            id='drop-5',
            options=[{'label': s, 'value': s}
                     for s in df_symbols['Symbol']
                     ],
            value=df_symbols['Symbol'][4],
        )
    ],
        style={'width': '32%', 'display': 'inline-block', 'padding': '5px 3px'}
    ),

    html.Div([
        dcc.Dropdown(
            id='drop-6',
            options=[{'label': s, 'value': s}
                     for s in df_symbols['Symbol']
                     ],
            value=df_symbols['Symbol'][5],
        )
    ],
        style={'width': '32%', 'display': 'inline-block', 'padding': '5px 3px'}
    ),

    html.Div([
        dcc.Graph(id='stock-4')
    ], style={'width': '32%', 'display': 'inline-block', }),

    html.Div([
        dcc.Graph(id='stock-5')
    ], style={'width': '32%', 'display': 'inline-block', }),

    html.Div([
        dcc.Graph(id='stock-6')
    ], style={'width': '32%', 'display': 'inline-block', }),
])


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
    df=get_single_stock(symbol, period='1y', datadir='./data/')

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits=[0.95 * df['Low'].min(), 1.05 * df['High'].max()]

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
    df=get_single_stock(symbol, period='1y', datadir='./data/')

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits=[0.95 * df['Low'].min(), 1.05 * df['High'].max()]

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
    df=get_single_stock(symbol, period='1y', datadir='./data/')

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits=[0.95 * df['Low'].min(), 1.05 * df['High'].max()]

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
    df=get_single_stock(symbol, period='1y', datadir='./data/')

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits=[0.95 * df['Low'].min(), 1.05 * df['High'].max()]

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
    df=get_single_stock(symbol, period='1y', datadir='./data/')

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits=[0.95 * df['Low'].min(), 1.05 * df['High'].max()]

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
    df=get_single_stock(symbol, period='1y', datadir='./data/')

    # make plot data
    data=make_plot_data(df, graph_name=graph_name, chart_name=chart_name, days=days_num)
    yaxis_limits=[0.95 * df['Low'].min(), 1.05 * df['High'].max()]

    return make_graph(data, yaxis_limits=yaxis_limits, xaxis_limits=date_range)


# main function
if __name__ == '__main__':
    app.run_server(debug=True)
