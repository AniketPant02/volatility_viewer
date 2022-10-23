import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.express as px


TEXT_STYLE = {"padding-top": "1rem", "padding-bottom": "1rem"}

title_texts = {
    0: "Where we stand: 2022",
    1: "Volatility plays a large role in portfolio risk.",
    2: "The bottom line."
}

texts = {
    0: "In 2022, we note an unprecented time in financial markets, with surging volatility and falling equity prices due to economic concerns. With Fed hikes, surging inflation, and pandemic recovery, some believe economic markets may be on the verge of a new era.",
    1: "Empirical analysis of 29 years of financial data demonstrates that market volatility strongly correlates with negative market returns. Periodic negative return increases leverage, making equity valuations increasingly volatile.",
    2: "In the last 20 years, 24/25 worst trading days were within one month of the 25 best trading days (Courtesy: BlackRock Investments, LLC). Keeping a long-term plan benefits investors and mitigates portfolio risk via short term volatility."
}

def page1Ret(fig, slider_idx):
    if (len(fig) == 2):
        return (
            html.Div(children=
            [
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
