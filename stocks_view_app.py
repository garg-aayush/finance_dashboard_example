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

#app = dash.Dash(__name__)

# read all the stocks data in dict of dfs
datadir = './data/'
margin = dict(l=25, r=25, t=30, b=5, pad=5)
transition_duration = 300

# read all symbols
df_symbols = pd.read_csv(datadir + 'symbols_ns.csv')

# make helper functions


def fig_update_layout(fig):
    fig.update_layout(
        margin=dict(l=25, r=25, t=30, b=5, pad=5, height=400))


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


def make_line_graph(df, x="Date", y="Close"):
    fig = px.line(df, x='Date', y='Close')
    fig.update_layout(margin=margin,
                      transition_duration=transition_duration)
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
###################################################
# App layout
###################################################


app.layout = html.Div(className='row', children=[

    html.Div([
        html.H4("Multiple stocks view"),
        dcc.RadioItems(
            id='graph-type',
            options=[{'label': 'Close price', 'value': 'Close'},
                     {'label': 'Single-candlestick', 'value': 'Candlestick'},
                     {'label': 'Both', 'value': 'Both'}
                     ],
            value='Close',
            labelStyle={'display': 'inline-block'}
        )
    ], style={'width': '100%', 'display': 'inline-block'}
    ),

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
            value=df_symbols['Symbol'][0],
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
@app.callback(
    Output('stock-1', 'figure'),
    [Input('drop-1', 'value'),
     Input('graph-type', 'value')]
)
def update_figure(symbol, graph_name):
    df = get_single_stock(symbol, period='1y', datadir='./data/')
    if graph_name == 'Close':
        return make_line_graph(df, x='Date', y='Close')
    elif graph_name == 'Candlestick':
        return make_candlestick(df)
    else:
        fig = make_line_graph(df, x='Date', y='Close') 

# call back, stock-2


@app.callback(
    Output('stock-2', 'figure'),
    [Input('drop-2', 'value'),
     Input('graph-type', 'value')]
)
def update_figure(symbol, graph_name):
    df = get_single_stock(symbol, period='1y', datadir='./data/')
    if graph_name == 'Close':
        return make_line_graph(df, x='Date', y='Close')
    else:
        return make_candlestick(df)

# call back, stock-3


@app.callback(
    Output('stock-3', 'figure'),
    [Input('drop-3', 'value'),
     Input('graph-type', 'value')]
)
def update_figure(symbol, graph_name):
    df = get_single_stock(symbol, period='1y', datadir='./data/')
    if graph_name == 'Close':
        return make_line_graph(df, x='Date', y='Close')
    else:
        return make_candlestick(df)

# call back, stock-4


@app.callback(
    Output('stock-4', 'figure'),
    [Input('drop-4', 'value'),
     Input('graph-type', 'value')]
)
def update_figure(symbol, graph_name):
    df = get_single_stock(symbol, period='1y', datadir='./data/')
    if graph_name == 'Close':
        return make_line_graph(df, x='Date', y='Close')
    else:
        return make_candlestick(df)

# call back, stock-5


@app.callback(
    Output('stock-5', 'figure'),
    [Input('drop-5', 'value'),
    Input('graph-type', 'value')]
)
def update_figure(symbol, graph_name):
    df = get_single_stock(symbol, period='1y', datadir='./data/')
    if graph_name == 'Close':
        return make_line_graph(df, x='Date', y='Close')
    else:
        return make_candlestick(df)

# call back, stock-6


@app.callback(
    Output('stock-6', 'figure'),
    [Input('drop-6', 'value'),
    Input('graph-type', 'value')]
) 
def update_figure(symbol, graph_name):
    df = get_single_stock(symbol, period='1y', datadir='./data/')
    if graph_name == 'Close':
        return make_line_graph(df, x='Date', y='Close')
    else:
        return make_candlestick(df)


# main function
if __name__ == '__main__':
    app.run_server(debug=True)
