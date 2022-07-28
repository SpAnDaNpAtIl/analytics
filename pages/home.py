import string
import dash
import pandas as pd
from dash import Dash, html, dcc, dash_table, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import config as cfg


dash.register_page(__name__, path='/')


wine_mask = np.array(Image.open("twittertry.png"))
def follower_number_homepage():
    return pd.read_excel('data/TVS.xlsx').iloc[-1]['number_of_followers']

def latest_tweet_homepage():
    df = pd.read_excel('data/TVS.xlsx')
    df = df[df.flag == 'tweets']
    tweetArray = []
    ls = reversed(df['cleaned_translated_tweet'].to_list())
    for i in ls:
        for j in (i.split("'")):
            if ((j != ']') and (j != ',') and (j != '[') and (j != ' ,') and (j != ', ') and j != ' '):
                if (len(tweetArray) < 10):
                    tweetArray.append(j)
    for i in range(len(tweetArray)):
        if (tweetArray[i][0] in string.whitespace):
            tweetArray[i] = tweetArray[i][1:]
        if (tweetArray[i][-1] in string.whitespace):
            tweetArray[i] = tweetArray[i][:-1]
    new_df = pd.DataFrame({
        "Sr No": [i + 1 for i in range(len(tweetArray))],
        "Tweet": tweetArray
    })
    return html.Div([
        dbc.Table.from_dataframe(new_df, striped=True, bordered=True, hover=True)
    ])





layout = html.Div(children=[
    html.H1('Twitter Analytics Dashboard for TVS', className='h3 mb-0 text-gray-800'),
    html.Br(),
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card(dbc.CardBody(dbc.Row([
                    dbc.Col([
                        html.Div([html.P("No. of followers")], className="text-xs font-weight-bold text-primary text-uppercase mb-1"),
                        html.Div([html.P(str(follower_number_homepage()))], className="h5 mb-0 font-weight-bold text-gray-800"),
                    ]),
                    dbc.Col([
                        html.Div(html.I(className="bi bi-person-circle"))
                    ], className='col-auto'),
                ], className='no-gutters align-items-center')), className='border-left-primary shadow h-100 py-2')
            ], width=3),


            dbc.Col([
                dbc.Card(dbc.CardBody(dbc.Row([
                    dbc.Col([
                        html.Div([html.P("Following")], className="text-xs font-weight-bold text-primary text-uppercase mb-1"),
                        html.Div([html.P("20", id='following_number_homepage')], className="h5 mb-0 font-weight-bold text-gray-800"),
                    ]),
                    dbc.Col([
                        html.Div(html.I(className="bi bi-person-circle"))
                    ], className='col-auto'),
                ], className='no-gutters align-items-center')), className='border-left-primary shadow h-100 py-2')
            ], width=3),
        ], justify="center"),

        html.Br(),

        dbc.Row
            ([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Tweet Counts", className="text-gray-800"),
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Tweets", id='tweets_dropdown_homepage'),
                                dbc.DropdownMenuItem("Mentions", id='mentions_dropdown_homepage'),
                            ],
                            direction='left',
                            className="no-arrow"
                        )
                    ],
                    className="card-header py-3 d-flex flex-row align-items-center justify-content-between"),

                    dbc.CardBody([
                        html.Div([
                            dbc.Row([dbc.Col('No. of days', className="text-gray-800 fs-5", width=1),
                                dbc.Col(dcc.Dropdown([i for i in range(2, 11)], value=5, id='number-of-days-dropdown-homepage'),
                                        width=3, ),
                            ], justify='start'),

                            dbc.Row([
                                html.Div([dbc.Row([
                                    dbc.Col(follower_number_homepage(), id='line-graph-tvs-homepage', className='chart-container', width='auto')
                                ], justify='center')], ),
                            ])
                        ])
                    ])

                ])
            ], width=8),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Sentiment Analysis", className="text-gray-800"),
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Tweets", id='tweets_dropdown_homepage_sentiments'),
                                dbc.DropdownMenuItem("Mentions", id='mentions_dropdown_homepage_sentiments'),
                            ],
                            direction='left',
                            className="no-arrow"
                        )
                    ],
                    className="card-header py-3 d-flex flex-row align-items-center justify-content-between"),

                    dbc.CardBody([
                        html.Div([
                            dbc.Row([dbc.Col('No. of days', className="text-gray-800 fs-5", width=2),
                                dbc.Col(dcc.Dropdown([i for i in range(2, 11)], value=2, id='number-of-days-dropdown-homepage-sentiments'), width=6),
                            ], justify='start'),

                            dbc.Row([
                                html.Div([dbc.Row([
                                    dbc.Col(id='donut-graph-sentiments-tvs', className='chart-container', width='auto')
                                ], justify='center')], ),
                            ])
                        ])
                    ])
                ])
            ], width=4)


        ]),

        html.Br(),

        dbc.Row([

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Wordcloud", className="text-gray-800"),
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Tweets", id='tweets_dropdown_homepage_wordcloud'),
                                dbc.DropdownMenuItem("Mentions", id='mentions_dropdown_homepage_wordcloud'),
                            ],
                            direction='left',
                            className="no-arrow"
                        )
                    ],
                    className="card-header py-3 d-flex flex-row align-items-center justify-content-between"),

                    dbc.CardBody([
                        html.Div([
                            dbc.Row([dbc.Col('No. of days', className="text-gray-800 fs-5", width=2),
                                dbc.Col(dcc.Dropdown([i for i in range(2, 11)], value=2, id='number-of-days-dropdown-homepage-wordcloud'), width=6),
                            ], justify='start'),

                            dbc.Row([
                                html.Div([dbc.Row([
                                    dbc.Col(id='word-cloud-tvs', className='chart-container', width='auto')
                                ], justify='center')], ),
                            ])
                        ])
                    ])
                ])
            ], width=4),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.H4("Sentiment Analysis(date-wise)", className="text-gray-800"),
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Tweets", id='tweets_dropdown_homepage_sentiments_datewise'),
                                dbc.DropdownMenuItem("Mentions", id='mentions_dropdown_homepage_sentiments_datewise'),
                            ],
                            direction='left',
                            className="no-arrow"
                        )
                    ], className="card-header py-3 d-flex flex-row align-items-center justify-content-between"),

                    dbc.CardBody([
                        html.Div([
                            dbc.Row([dbc.Col('No. of days', className="text-gray-800 fs-5", width=1),
                                dbc.Col(dcc.Dropdown([i for i in range(2, 11)], value=5, id='number-of-days-dropdown-homepage-sentiments-datewise'), width=3),
                            ], justify='start'),

                            dbc.Row([
                                html.Div([dbc.Row([
                                    dbc.Col(id='bar-graph-sentiments-tvs-datewise', className='chart-container', width='auto')
                                ], justify='center')], ),
                            ])
                        ])
                    ])


                ]), width=8)
        ]),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader([
                            html.H4("#10 Latest Tweets", className="text-gray-800"),
                    ], className="card-header py-3 d-flex flex-row align-items-center justify-content-between"),

                        dbc.CardBody([
                            latest_tweet_homepage()
                        ])
                    ])
                )
            ]
        )



    ])

])





@callback(
    Output('line-graph-tvs-homepage', 'children'),
    [
        Input('number-of-days-dropdown-homepage', 'value'),
        Input('tweets_dropdown_homepage', 'n_clicks'),
        Input('mentions_dropdown_homepage', 'n_clicks'),
    ]
)
def line_grapher_home(days, n1clicks, n2clicks):
    ctx = dash.callback_context
    if(ctx.triggered[0]["prop_id"].split(".")[0] == 'tweets_dropdown_homepage' or ctx.triggered[0]["prop_id"].split(".")[0] == 'number-of-days-dropdown-homepage' or ctx.triggered[0]['value']==None):
        df = pd.read_excel('data/TVS.xlsx')
        df = df[(df.flag == 'Tweets'.lower())].tail(days)
        x = df['date'].tolist()
        y = df['tweet_count'].tolist()
        return dcc.Graph(figure=go.Figure(
            data=[go.Scatter(x=x, y=y, mode='lines', marker=dict(color='#0066ff'))],
            layout={'title': 'Tweets Count of TVS',
                    'xaxis': {'title': 'Number of days'},
                    'yaxis': {'title': 'Number of tweets'}}))
    if(ctx.triggered[0]["prop_id"].split(".")[0] == 'mentions_dropdown_homepage'):
        df = pd.read_excel('data/TVS.xlsx')
        df = df[(df.flag == 'Mentions'.lower())].tail(days)
        x = df['date'].tolist()
        y = df['tweet_count'].tolist()
        return dcc.Graph(figure=go.Figure(
            data=[go.Scatter(x=x, y=y, mode='lines', marker=dict(color='#0066ff'))],
            layout={'title': 'Mentions Count of TVS',
                    'xaxis': {'title': 'Number of days'},
                    'yaxis': {'title': 'Number of mentions'}}))




@callback(
    Output('donut-graph-sentiments-tvs', 'children'),
    [   Input('number-of-days-dropdown-homepage-sentiments', 'value'),
        Input('tweets_dropdown_homepage_sentiments', 'n_clicks'),
        Input('mentions_dropdown_homepage_sentiments', 'n_clicks'),
    ]
)
def donut_grapher_home(days, n1clicks, n2clicks):
    ctx = dash.callback_context
    labels = ['Positive', 'Negative']
    df = pd.read_excel('data/TVS.xlsx')
    df = df[['POSITIVE', 'NEGATIVE', 'flag']]
    df = pd.concat([df[(df.flag == 'Tweets'.lower())].tail(days), df[(df.flag == 'Mentions'.lower())].tail(days)])
    new_df = df.groupby(['flag']).sum()
    if(ctx.triggered[0]["prop_id"].split(".")[0] == 'tweets_dropdown_homepage_sentiments' or ctx.triggered[0]["prop_id"].split(".")[0] == 'number-of-days-dropdown-homepage-sentiments' or ctx.triggered[0]['value']==None):
        values = [new_df['POSITIVE'][1], new_df['NEGATIVE'][1]]
        return dcc.Graph(figure=go.Figure(
            data=[go.Pie(labels=labels, values=values, hole=0.3)],
            layout={'title': 'Sentiments Analysis for tweets of TVS'}))
    if(ctx.triggered[0]["prop_id"].split(".")[0] == 'mentions_dropdown_homepage_sentiments'):
        values = [new_df['POSITIVE'][0], new_df['NEGATIVE'][0]]
        return dcc.Graph(figure=go.Figure(
            data=[go.Pie(labels=labels, values=values, hole=0.3)],
            layout={'title': 'Sentiments Analysis of mentions for TVS'}))




@callback(
    Output('bar-graph-sentiments-tvs-datewise', 'children'),
    [Input('number-of-days-dropdown-homepage-sentiments-datewise', 'value'),
     Input('tweets_dropdown_homepage_sentiments_datewise', 'n_clicks'),
     Input('mentions_dropdown_homepage_sentiments_datewise', 'n_clicks'),
     ]
)
def bar_grapher_home_for_sentiments(days, n1clicks, n2clicks):
    ctx = dash.callback_context
    df = pd.read_excel('data/TVS.xlsx')
    if (ctx.triggered[0]["prop_id"].split(".")[0] == 'tweets_dropdown_homepage_sentiments_datewise' or ctx.triggered[0]["prop_id"].split(".")[0] == 'number-of-days-dropdown-homepage-sentiments-datewise' or ctx.triggered[0]['value'] == None):
        df = df[(df.flag == 'Tweets'.lower())].tail(days)
        x = df['date'].tolist()
        return dcc.Graph(
            figure=dict(
                data=[dict(x=x,
                           y=df[j],
                           type='bar',
                           name=j) for j in ['POSITIVE', 'NEGATIVE']],
                layout=go.Layout(title='Sentiments count of TVS for Tweets',
                                 barmode='stack',
                                 xaxis={'title': 'No. of days'},
                                 yaxis={'title': 'Count of sentiments'})),
        )

    if (ctx.triggered[0]["prop_id"].split(".")[0] == 'mentions_dropdown_homepage_sentiments_datewise'):
        df = df[(df.flag == 'Mentions'.lower())].tail(days)
        x = df['date'].tolist()
        return dcc.Graph(
            figure=dict(
                data=[dict(x=x,
                           y=df[j],
                           type='bar',
                           name=j) for j in ['POSITIVE', 'NEGATIVE']],
                layout=go.Layout(title='Sentiments count of TVS for Mentions',
                                 barmode='stack',
                                 xaxis={'title': 'No. of days'},
                                 yaxis={'title': 'Count of sentiments'})),
        )


@callback(
    Output('word-cloud-tvs', 'children'),
    [Input('number-of-days-dropdown-homepage-wordcloud', 'value'),
     Input('tweets_dropdown_homepage_wordcloud', 'n_clicks'),
     Input('mentions_dropdown_homepage_wordcloud', 'n_clicks'),]
)
def word_cloud_for_TVS(days, n1clicks, n2clicks):
    ctx = dash.callback_context
    df = pd.read_excel('data/TVS.xlsx')
    if (ctx.triggered[0]["prop_id"].split(".")[0] == 'tweets_dropdown_homepage_wordcloud' or ctx.triggered[0]["prop_id"].split(".")[0] == 'number-of-days-dropdown-homepage-wordcloud' or ctx.triggered[0]['value'] == None):
        df = df[(df.flag == 'tweets')].tail(days)
        rows = ['Cleaned_translated_tweet', 'Hashtags']
        content_arr = []
        for row in rows:
            ls = df[row.lower()].to_list()
            listToStr = ' '.join([str(elem) for elem in ls])
            listToStr = listToStr.translate({ord('['): None, ord(']'): None})
            if (row == 'Hashtags'):
                lst0 = [i[2:-2] for i in listToStr.split()]  # removes hashtags and inverted commas
                lst = []
                for i in lst0:
                    if '#' in i:
                        k = i.split('#')  # if multiple hashtags in one tweet/mention then splits them
                        for j in k:
                            if (j.isalpha()):
                                lst.append(
                                    j)  # only considers words, if after split accounts are tagged then neglects them
                    else:
                        lst.append(i)
            else:
                lst = [i for i in listToStr.split() if i.isalpha()]
            lst = [word for word in lst if word not in cfg.my_stopwords]
            comment_words = ''
            # stopwords = set(cfg.my_stopwords)
            comment_words += " ".join(lst) + " "

            wordcloud = WordCloud(width=1600, height=800,
                                  background_color='white',
                                  # stopwords=stopwords,
                                  min_font_size=5, mask=wine_mask).generate(comment_words)
            img = wordcloud.to_image()
            content_arr.append(img)

        return html.Div([
            dbc.Tabs(
                [
                    dbc.Tab(dbc.Card(
                        dbc.CardImg(src=content_arr[0], top=True)
                    ), label='Content of Tweets'),
                    dbc.Tab(dbc.Card(
                        dbc.CardImg(src=content_arr[1], top=True)
                    ), label='Hashtags of Tweets'),
                ])], className='d-inline-block')

    if (ctx.triggered[0]["prop_id"].split(".")[0] == 'mentions_dropdown_homepage_wordcloud'):
        df = df[(df.flag == 'mentions')].tail(days)
        rows = ['Cleaned_translated_tweet', 'Hashtags']
        content_arr = []
        for row in rows:
            ls = df[row.lower()].to_list()
            listToStr = ' '.join([str(elem) for elem in ls])
            listToStr = listToStr.translate({ord('['): None, ord(']'): None})
            if (row == 'Hashtags'):
                lst0 = [i[2:-2] for i in listToStr.split()]  # removes hashtags and inverted commas
                lst = []
                for i in lst0:
                    if '#' in i:
                        k = i.split('#')  # if multiple hashtags in one tweet/mention then splits them
                        for j in k:
                            if (j.isalpha()):
                                lst.append(
                                    j)  # only considers words, if after split accounts are tagged then neglects them
                    else:
                        lst.append(i)
            else:
                lst = [i for i in listToStr.split() if i.isalpha()]
            lst = [word for word in lst if word not in cfg.my_stopwords]
            comment_words = ''
            # stopwords = set(cfg.my_stopwords)
            comment_words += " ".join(lst) + " "

            wordcloud = WordCloud(width=1600, height=800,
                                  background_color='white',
                                  # stopwords=stopwords,
                                  min_font_size=5, mask=wine_mask).generate(comment_words)
            img = wordcloud.to_image()
            content_arr.append(img)

        return html.Div([
            dbc.Tabs(
                [
                    dbc.Tab(dbc.Card(
                        dbc.CardImg(src=content_arr[0], top=True)
                    ), label='Content of Mentions',),
                    dbc.Tab(dbc.Card(
                        dbc.CardImg(src=content_arr[1], top=True)
                    ), label='Hashtags of Mentions'),
                ])], className='d-inline-block')







