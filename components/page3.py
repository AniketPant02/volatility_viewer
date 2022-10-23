import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.express as px
import pandas as pd

TEXT_STYLE = {
    "padding-top" : "1rem",
    "padding-bottom": "1rem"
}

title_texts = {
    0: "Monetary policy influences volatility.",
    1: "A history of substantial hikes.",
}


texts = {
    0: "The federal fund rate signals the interest rate that banks charge for currency exhange. The federal fund rate influences how expensive borrowing money is. We find that federal fund rate increases tend to lead to elevated market volatility for short periods. However, we suggest the market overprices volatility around federal rate releases.",
    1: "We note that months with substantials changes in the federal fund rate experience elevated volatility. We recommend short-term volatility hedges during times of high federal rate hikes.",
}

def page3Ret(fig, slider_idx):
    if (len(fig) == 2):
        return (
            html.Div(children=[
                        html.H2(
                            f"{title_texts[slider_idx]}",
                            className="card-title",
                            style={"text-transform": "none"},
                            ),
                        dcc.Markdown(
                            f"{texts[slider_idx]}",
                            className="card-text",
                            style=TEXT_STYLE,
                        ),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Div(children=[
                                            dcc.Graph(
                                                id='example-graph1a',
                                                figure=fig[0]
                                            )
                                        ])),
                                        dbc.Col(html.Div(children=[
                                            dcc.Graph(
                                                id='example-graph1b',
                                                figure=fig[1]
                                            )
                                        ])),
                                    ]
                                ),
                            ]
                        )
            ], style={"margin-top": "4rem", "margin-left": "3rem", "margin-right": "3rem"})
        )
    else:
        return (
            html.Div(children=[
                html.H2(
                    f"{title_texts[slider_idx]}",
                    className="card-title",
                    style={"text-transform": "none"},
                    ),
                dcc.Markdown(
                    f"{texts[slider_idx]}",
                    className="card-text",
                    style=TEXT_STYLE,
                ),
                html.Div(
                    [
                        dcc.Graph(
                        id='example-graph3',
                        figure=fig[0]
                    )],
                    style={
                        "align-items": "center"
                    }
                )
            ], style={"margin-top": "4rem", "margin-left": "3rem", "margin-right": "3rem"})
        )
