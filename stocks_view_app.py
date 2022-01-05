# App to view particular stock price over the last 1 year

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


app = dash.Dash(__name__)

# read all the stocks data in dict of dfs
datadir = './data/'
symbol = ['ADANIPORTS', 'ALKEM', 'ASHOKA',
        'ASHOKLEY', 'ASIANPAINT', 'BAJFINANCE',
        'BRITANNIA', 'CAMS', 'COALINDIA']

df_dict={}
for s in symbol:
    df_dict[s] = pd.read_csv(datadir + s + '.NS')

# make helper functions
def fig_update_layout(fig):
    fig.update_layout(
        margin=dict(l=25, r=25, t=30, b=5)
        )

def make_fig(df_dict, name='', x="Date", y="Close"):
    fig = px.line(df_dict[name], x=x, y=y, title=name)
    return fig


fig1 = make_fig(df_dict, name='ADANIPORTS', title_x=0.5)
fig2 = make_fig(df_dict, name='ALKEM')
fig3 = make_fig(df_dict, name='ASHOKA')
fig4 = make_fig(df_dict, name='ASHOKLEY')
fig5 = make_fig(df_dict, name='ASIANPAINT')
fig6 = make_fig(df_dict, name='BAJFINANCE')
fig7 = make_fig(df_dict, name='BRITANNIA')
fig8 = make_fig(df_dict, name='CAMS')
fig9 = make_fig(df_dict, name='COALINDIA')

# fig1.update_layout(margin=dict(l=25, r=25, t=20, b=20))
# fig2.update_layout(margin=dict(l=25, r=25, t=20, b=20))
# fig3.update_layout(margin=dict(l=25, r=25, t=20, b=20))
# fig4.update_layout(margin=dict(l=25, r=25, t=20, b=20))
# fig5.update_layout(margin=dict(l=25, r=25, t=20, b=20))
# fig6.update_layout(margin=dict(l=25, r=25, t=20, b=20))
# fig7.update_layout(margin=dict(l=25, r=25, t=20, b=20))
# fig8.update_layout(margin=dict(l=25, r=25, t=20, b=20))
# fig9.update_layout(margin=dict(l=25, r=25, t=20, b=20))
fig_update_layout(fig1)
fig_update_layout(fig2)
fig_update_layout(fig3)
fig_update_layout(fig4)
fig_update_layout(fig5)
fig_update_layout(fig6)
fig_update_layout(fig7)
fig_update_layout(fig8)
fig_update_layout(fig9)

app.layout = html.Div(className='row', children=[
    html.H1("Multiple stocks view"),
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
if __name__ == '__main__':
    app.run_server(debug=True)
