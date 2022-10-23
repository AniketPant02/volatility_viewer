import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html
import plotly.express as px


from components.content_meta import content_meta_populate

app = dash.Dash(external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
app.title = "Volatility Viewer"
html.Link(href="https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap", rel="stylesheet")

last_back = 0
last_next = 0
last_back_2 = 0
last_next_2 = 0
last_back_3 = 0
last_next_3 = 0

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "absolute",
    "top": 0,
    "left": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#f3f6fa",
    "text-align": "center",
    "font-family": 'open sans,sans-serif',
    "font-size": 11,
    "height": "100%",
    "justify-content": "center"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left" : SIDEBAR_STYLE['width'],
    "margin-right" : "auto",
    "padding": "3rem 2rem",
    "padding-top" : "2rem",
    "text-align": "left",
    "font-family": 'open sans,sans-serif',
    "border" : "none",
    "font-size": 13,
    "position" : "fixed"
}


NAV_LINK_STYLE = {
    "margin": "auto"
}


APP_STYLE = {
    "height": "100%"
}

SIDE_CONTENT_STYLE = {
    "padding-top": "2rem"
}

SIDE_TEXT_STYLE = {
    "font-size": 14,
    "font-family": 'open sans,sans-serif'
}

buttonStyle = {
    "margin-top": "1rem"
}

# src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Georgia_Tech_Yellow_Jackets_logo.svg/2560px-Georgia_Tech_Yellow_Jackets_logo.svg.png",

sidebar = html.Div(
    [
        html.Div([
            html.Div([html.Img(
                alt="GaTech",
                src="assets/quasar.png",
                height = 64
            )]),
            html.Div([html.Img(
                alt="BlackRock ©",
                src="https://1000logos.net/wp-content/uploads/2021/09/BlackRock-logo.png",
                height = 64
            )])
        ], style = {
            "display": "flex",
            "flex-direction": "row",
            "justify-content": "space-around",
            "margin-top": "1rem",
            "margin-left": "1rem",
            "margin-right": "1rem",
            "margin-bottom": "4rem"
        }),
        html.H1("Volatility Viewer", className="display-8", style = {"text-transform": "lowercase", "font-color": "#2a3f5f"}),
        html.Hr(),
        html.P(
            "A data exploration tool for observing the effects of market volatility.", style=SIDE_TEXT_STYLE
        ),
        # The memory store reverts to the default on every page refresh
        dcc.Store(id='memory'), # this will hold slider info
        dcc.Store(id='memory2'),
        dcc.Store(id='memory3'),
        html.Div([dbc.Nav(
            [
                dbc.NavLink("Market", href="/", active="exact", style=NAV_LINK_STYLE),
                dbc.NavLink("Inflation", href="/page-2", active="exact", style=NAV_LINK_STYLE),
                dbc.NavLink("Rates", href="/page-3", active="exact", style=NAV_LINK_STYLE),
                dbc.NavLink("About", href="/about", active="exact", style=NAV_LINK_STYLE),
            ],
            horizontal=True,
            pills=True
        )], style = {"margin-top": "3rem", "margin-bottom": "3rem"}),
        html.Div(id="what-page-am-i-on"),
        html.Div([
            html.P("Made with love by team Quasar for HackGT9.")
        ], style = {
            "position": "absolute",
            "bottom": "1px"
        })
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div(
    [
        dcc.Location(id="url"), 
        sidebar, 
        content
    ],
    style=APP_STYLE
)

@app.callback(
    Output("what-page-am-i-on", "children"),
    [Input("url", "pathname")],
)
def render_page_location(pathname):
    if pathname == "/":
        return html.Div([
            dcc.Slider(
                min = 0,
                max = 2,
                step = 1,
                id = f"slider-{pathname}",
                value = 0,
                marks={i: ''.format(i + 1) for i in range(3)},
            ),
            html.Div([
                html.Button("Back", id = "back", className='btn btn-outline-primary btn-sm',
                style={
                    "width": "35%",
                    "margin-left": "10%",
                    "margin-right": "2.5em"
                }),
                html.Button("Next", id = "next", className='btn btn-outline-primary btn-sm',
                style={
                    "width": "35%",
                    "margin-right": "10%"
                })
            ], style = buttonStyle)
        ])
    elif pathname == "/page-2":
        return html.Div([
            dcc.Slider(
               min = 0,
                max = 3,
                step = 1,
                id = f"slider-{pathname}",
                value = 0,
                marks={i: ''.format(i + 1) for i in range(4)},
            ),
            html.Div([
                html.Button("Back", id = "back2", className='btn btn-outline-primary btn-sm',
                style={
                    "width": "35%",
                    "margin-left": "10%",
                    "margin-right": "2.5em"
                }),
                html.Button("Next", id = "next2", className='btn btn-outline-primary btn-sm',
                style={
                    "width": "35%",
                    "margin-right": "10%"
                })
            ], style = buttonStyle)
        ])
    elif pathname == "/page-3":
        return html.Div([
            dcc.Slider(
                min = 0,
                max = 1,
                step = 1,
                id = f"slider-{pathname}",
                value = 0,
                marks={i: ''.format(i + 1) for i in range(4)},
            ),
            html.Div([
                html.Button("Back", id = "back3", className='btn btn-outline-primary btn-sm', 
                style={
                    "width": "35%",
                    "margin-left": "10%",
                    "margin-right": "2.5em"
                }),
                html.Button("Next", id = "next3", className='btn btn-outline-primary btn-sm',
                style={
                    "width": "35%",
                    "margin-right": "10%"
                })
            ]
            , style = buttonStyle)
        ])
    else:
        return html.Div([
            ""
        ])

@app.callback(
    Output("memory", "data"),
    [
        Input("slider-/", "value")
    ]
)
def slider1_callback(value):
    return {"slider_1": value}


@app.callback(
    Output("memory2", "data"),
    [
        Input("slider-/page-2", "value")
    ]
)
def slider2_callback(value):
    return {"slider_2": value}

@app.callback(
    Output("memory3", "data"),
    [
        Input("slider-/page-3", "value")
    ]
)
def slider3_callback(value):
    return {"slider_3": value}

@app.callback(
    Output("slider-/", "value"), 
    [Input('back', 'n_clicks'), Input('next', 'n_clicks')],    
    [State("slider-/", "value")]
)
def advance_slider1(back, nxt, slider):    
    
    if back is None:
        back = 0
    if nxt is None:
        nxt = 0
    if slider is None:
        slider = 0

    global last_back
    global last_next
    

    if back > last_back:
        last_back = back
        slider = max(0, slider - 1)
    if nxt > last_next:
        last_next = nxt
        slider = min(2, slider + 1)
    
    return slider

@app.callback(
    Output("slider-/page-2", "value"), 
    [Input('back2', 'n_clicks'), Input('next2', 'n_clicks')],    
    [State("slider-/page-2", "value")]
)
def advance_slider2(back2, nxt2, slider2):    
    
    if back2 is None:
        back2 = 0
    if nxt2 is None:
        nxt2 = 0
    if slider2 is None:
        slider2 = 0
    
    global last_back_2
    global last_next_2

    if back2 > last_back_2:
        last_back_2 = back2
        slider2 = max(0, slider2 - 1)
    if nxt2 > last_next_2:
        last_next_2 = nxt2
        slider2 = min(3, slider2 + 1)
    
    return slider2

@app.callback(
    Output("slider-/page-3", "value"), 
    [Input('back3', 'n_clicks'), Input('next3', 'n_clicks')],    
    [State("slider-/page-3", "value")]
)
def advance_slider3(back3, nxt3, slider3):    
    if back3 is None:
        back3 = 0
    if nxt3 is None:
        nxt3 = 0
    if slider3 is None:
        slider3 = 0
    
    global last_back_3
    global last_next_3

    if back3 > last_back_3:
        last_back_3 = back3
        slider3 = max(0, slider3 - 1)
    if nxt3 > last_next_3:
        last_next_3 = nxt3
        slider3 = min(1, slider3 + 1)
    
    return slider3


@app.callback(
    Output("page-content", "children"), 
    [
        Input("url", "pathname"),
        Input('memory','data'),
        Input('memory2','data'),
        Input('memory3','data'),
    ],
)
def render_page_content(pathname, jsonDict1, jsonDict2, jsonDict3):

    if jsonDict1 is None:
        jsonDict1 = {"slider_1": 0}
    elif jsonDict2 is None:
        jsonDict2 = {"slider_2": 0}
    elif jsonDict3 is None:
        jsonDict3 = {"slider_3": 0}

    if pathname == "/":
        return content_meta_populate(pathname, jsonDict1['slider_1'])
    elif pathname == "/page-2":
        return content_meta_populate(pathname, jsonDict2['slider_2'])
    elif pathname == "/page-3":
        return content_meta_populate(pathname, jsonDict3['slider_3'])
    elif pathname == "/about":
        return content_meta_populate(pathname, 0)

    

if __name__ == '__main__':
    app.run_server(debug=True)
