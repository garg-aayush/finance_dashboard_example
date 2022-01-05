# App to view particular stock price over the last 1 year

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from utils import read_single_stock, write_csv

app = dash.Dash(__name__)

# read all the stocks data in dict of dfs
datadir = './data/'
symbol = ['ADANIPORTS', 'ALKEM', 'ASHOKA',
        'ASHOKLEY', 'ASIANPAINT', 'BAJFINANCE',
        'BRITANNIA', 'CAMS', 'COALINDIA']

df_dict={}
for s in symbol:
    df_dict[s] = pd.read_csv(datadir + s + '.NS')

# read all symbols
df_symbols = pd.read_csv(datadir + 'symbols_ns.csv')

# make helper functions
def fig_update_layout(fig):
    fig.update_layout(
        margin=dict(l=25, r=25, t=30, b=5)
        )

def make_fig(df_dict, name='', x="Date", y="Close"):
    fig = px.line(df_dict[name], x=x, y=y, title=name)
    return fig


fig1 = make_fig(df_dict, name='ADANIPORTS')
fig2 = make_fig(df_dict, name='ALKEM')
fig3 = make_fig(df_dict, name='ASHOKA')
fig4 = make_fig(df_dict, name='ASHOKLEY')
fig5 = make_fig(df_dict, name='ASIANPAINT')
fig6 = make_fig(df_dict, name='BAJFINANCE')
fig7 = make_fig(df_dict, name='BRITANNIA')
fig8 = make_fig(df_dict, name='CAMS')
fig9 = make_fig(df_dict, name='COALINDIA')

fig_update_layout(fig1)
fig_update_layout(fig2)
fig_update_layout(fig3)
fig_update_layout(fig4)
fig_update_layout(fig5)
fig_update_layout(fig6)
fig_update_layout(fig7)
fig_update_layout(fig8)
fig_update_layout(fig9)

###################################################
# callbacks
###################################################
@app.callback(
    Output('stock-1', 'figure'),
    Input('drop-1', 'value'))

def update_figure(symbol):
    df = read_single_stock(symbol=symbol+'.NS', period='1y')
    write_csv(df, './data/'+symbol+'.NS')
    df = pd.read_csv('./data/'+symbol+'.NS')
    print(df.head())
    fig = px.line(df, x='Date', y='Close', title=symbol)


    # fig.update_layout(
    #     transition_duration=500)
    return fig

###################################################
# App layout
###################################################
app.layout = html.Div(className='row', children=[
    html.H1("Multiple stocks view"),
    html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(
            id='drop-1',
            options=[{'label': s, 'value': s}
                    for s in df_symbols['Symbol']],
            value=df_symbols['Symbol'][0]
        )
    ]),
    html.Div(children=[
        dcc.Graph(id="stock-1", style={'display': 'inline-block', 'width': '60vh', 'height': '40vh'}, figure=fig1),
        dcc.Graph(id="stock-2", style={'display': 'inline-block', 'width': '60vh', 'height': '40vh'}, figure=fig2),
        dcc.Graph(id="stock-3", style={'display': 'inline-block', 'width': '60vh', 'height': '40vh'}, figure=fig3)
    ]),
    html.Div(children=[
        dcc.Graph(id="stock-4", style={'display': 'inline-block', 'width': '60vh', 'height': '40vh'}, figure=fig4),
        dcc.Graph(id="stock-5", style={'display': 'inline-block', 'width': '60vh', 'height': '40vh'}, figure=fig5),
        dcc.Graph(id="stock-6", style={'display': 'inline-block', 'width': '60vh', 'height': '40vh'}, figure=fig6)
    ]),
    html.Div(children=[
        dcc.Graph(id="stock-7", style={'display': 'inline-block', 'width': '60vh', 'height': '40vh'}, figure=fig7),
        dcc.Graph(id="stock-8", style={'display': 'inline-block', 'width': '60vh', 'height': '40vh'}, figure=fig8),
        dcc.Graph(id="stock-9", style={'display': 'inline-block', 'width': '60vh', 'height': '40vh'}, figure=fig9)
    ])
])

# main function
if __name__ == '__main__':
    app.run_server(debug=True)
