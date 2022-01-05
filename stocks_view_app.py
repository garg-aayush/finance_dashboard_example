# App to view particular stock price over the last 1 year

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


app = dash.Dash(__name__)

df = pd.read_csv('./data/sample_stock.csv')

fig = px.line(df, x="Date", y="Close")

app.layout = html.Div([
    dcc.Graph(
        id='sample_stock',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
