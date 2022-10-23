import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def aboutPage():
    return (
        html.Div(children=[
            html.H3("Educating investors on evolving market volatility and conditions.", className="card-title", style = {"text-transform": "none"}),
            html.H6("Created by Team Quasar", style = {
                    "margin-top": "1rem"
                }),
            html.Div([
                dcc.Markdown(
                    '''
                    We created **`volatility viewer`** to introduce investors to management considerations in evolving markets. Our goal is empowering individual investors to understand the role market volatility may have on investment risk-profiles.

                    **`The team`:**
                    * Aniket Pant: 3rd year BS MSE @ GT. Passionate about scientific machine learning. 
                    * Ritvik Verma: 2nd year BS CompE @ GT. Passionate about cybersecurity and multimedia creation. 
                    * Ritarka Samanta: 2nd year BS CompE @ GT. Passionate about data analytics and computer architecture.
                    * Smit Shete: 2nd year BS CS @ GT. Passionate about front-end informatics and software accessibility.

                    **`Tech stack:`**
                    * Frontend: Dash + Plotly
                    * Theming: Bootstrap
                    * Data processing: Pandas/Numpy

                    **`Data stack:`**
                    * $SPY, ^VIX: MacroTrends
                    * CPI: BLS
                    * Federal Fund Reserve Rates: FRED

                    Please check out our [GitHub](https://github.com/Ritarka/HackGT9)! 
                    '''
                , style = {
                    "margin-top": "1rem"
                })
            ])
        ], style = {"margin-top": "4rem"}))