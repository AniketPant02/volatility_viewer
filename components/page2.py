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
    0: "The last century: revisted.",
    1: "CPI-induced volatility is short lived.",
    2: "CPI releases are a weak predictor of volatility.",
    3: "CPI and volatility fall out of long-term correlation in recessionary periods."
}


texts = {
    0: "The Consumer Price Index (CPI) measures average prices paid by consumers for representative goods and services. In 2022, inflation proves rampant: the overall CPI has rapidly climbed and affected market conditions, with overall prices increasing across a variety of sectors.",
    1: "Weeks of CPI releases often involve periods of elevated volatility. However, we note these changes are short lived and see no need for short-term portfolio risk mitigation.",
    2: "We empirically note that correlation between reported monthly CPI increases (BLS) and monthly changes in market volatility are nonexistent. Although the trend is downwards sloping, the correlation is weak, suggesting that CPI releases do not require month-long hedges against volatility.",
    3: "12-month rolling correlations between monthly changes in market volatility and monthly changes in CPI show strong negative signals in times of economic pessimism. We suggest CPI and market volatility fall out of correlation well into recessionary periods."
}

def page2Ret(fig, slider_idx):
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
                    html.Div(children=[
                        dcc.Graph(
                            id='example-graph2',
                            figure=fig
                        )
                    ], style={
                        "align-items": "center"
                    })
                    
        ], style={"margin-top": "4rem", "margin-left": "3rem", "margin-right": "3rem"})
    )