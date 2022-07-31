import string
import pandas as pd
from dash import Dash, html, dcc, dash_table
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import config as cfg

external_scripts = ["https://platform.twitter.com/widgets.js"]
com_logo = "https://www.freepnglogos.com/uploads/tvs-logo-png/tvs-motors-logo-png-0.png"

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], external_scripts=external_scripts, use_pages=True)
server = app.server




app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
             [html.A(
                dbc.Row([
                    dbc.Col(html.Img(src=com_logo, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Twitter Analytics Dashboard for TVS", className="ms-2"),),
                    dbc.Col(
                        html.A(href='https://twitter.com/tvsmotorcompany?ref_src=twsrc%5Etfw',
                            className='twitter-follow-button',
                            target='_blank',
                               ),
                        )
                    ],
                    align="center",
                    className="g-0",
                    ),
                href="https://www.tvsmotor.com/",
                style={"textDecoration": "none"},
                ),
                 dbc.DropdownMenu(
                     children=[
                         dbc.DropdownMenuItem("Home", className="ms-2", href="/"),
                         dbc.DropdownMenuItem("Compare Brands", className="ms-2", href="/analytics"),
                     ],
                     nav=True,
                     in_navbar=True,
                     label="More",
                 ),
             ]
            ),
        color="dark",
        dark=True,
        className='ms-3 me-3'
        ),

    dbc.Container([
        dash.page_container,
    ],
    className="container rounded",
    style={"backgroundColor": "#F5F5F5"}
    )


])

