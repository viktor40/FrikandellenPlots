# -*- coding: utf-8 -*-
"""
    ****************
    dash_app.py
    ****************
    
    Created at 16/09/21        
"""
__author__ = 'Jonas Van Der Donckt'

import traceback

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from PIL import Image
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

# -------  globals
global_df = None
global_fig = None
app = dash.Dash()


# ---------------- helper methods ----------------
def read_parse_csv():
    global global_df
    try:
        df = pd.read_csv('data.csv', sep=',', low_memory=False).set_index(
            'Groep').astype(
            np.uint8)

        # set the index type to category so that the
        df.index = df.index.astype('str')
        # bereken het totaal # frikandellen en sorteer zodat de groep met de meeste frikandellen links weergegeven wordt
        df['totaal_frikandellen'] = df.sum(axis=1)
        df = df.sort_values(by='totaal_frikandellen', ascending=False)
        global_df = df
    except:
        traceback.print_exc()


# construct the app layout
def serve_layout():
    return html.Div([
        dcc.Graph(id='figure', config={
            'displayModeBar': False
        }),
        dcc.Interval(id='interval-component',
                     interval=1 * 1000,
                     n_intervals=0
                     ),
    ])


app.layout = serve_layout()


# ---------- define callbacks
@app.callback(
    Output('figure', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    read_parse_csv()
    global global_df

    fig = make_subplots(
        rows=2,
        cols=2,
        specs=[[{"type": "pie"}, {}], [{"colspan": 2}, None]],
        subplot_titles=(
            f"Totaal: {global_df['totaal_frikandellen'].sum()}", "", "Ranking"),
        vertical_spacing=0.1
    )

    colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c"]

    fig.add_trace(
        go.Pie(
            labels=global_df.index.values.tolist(),
            values=global_df['totaal_frikandellen'].values.tolist(),
            # textinfo='label+value',
            showlegend=False
        ),
        row=1,
        col=1,
    )

    for i, c in enumerate(
            ["min 0-6", "min 6-12", "min 12-18", "min 18-24", "min 24-30"]):
        fig.add_trace(
            go.Bar(
                x=global_df.index.values.tolist(),
                y=global_df[c].values.tolist(),
                marker_color=colors[i],
                name=c,
            ),
            row=2,
            col=1,
        )
    fig.add_layout_image(
        row=1,
        col=2,
        source=Image.open('de_wilg.jpg'),
        xref="x domain",
        yref="y domain",
        x=0.6,
        y=1.05,
        xanchor="left",
        yanchor="top",
        sizex=1,
        sizey=0.5,
    )

    # fig.update_layout(legend_traceorder="reversed")
    fig.update_layout(
        height=500,
        title=f'<b>{global_df.index[0]}</b> leiden met <b>{global_df["totaal_frikandellen"][0]}</b> frikandellen',
        title_x=0.5,
        barmode="stack",
        legend=dict(
            traceorder="normal",
            orientation="h",
            yanchor="bottom",
            xanchor="left",
            y=-.25,
            x=0,
        ),
    )
    fig.update_yaxes(title="# frikandellen", row=2)
    return fig


if __name__ == '__main__':
    app.run_server()
