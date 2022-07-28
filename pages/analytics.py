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
import base64

dash.register_page(__name__)
wine_mask = np.array(Image.open("twittertry.png"))

layout = html.Div([
    dbc.Breadcrumb(
    items=[
        {"label": "Main", "href": "/", "external_link": True},
        {"label": "Compare Brands", "active": True},
    ],
    ),
    html.H1('Compare Brands'),
    dbc.Container([
        dbc.Row(
            dbc.Col(html.H4('Select Brands',className="text-dark my-1 fs-2 text-center"),
                    width={"size": 3},), justify='center',
        ),
        dbc.Row(
            dbc.Col(dcc.Dropdown(['Hero', 'Honda'], 'Honda', multi=True, id='compete-brand-dropdown'),
                    width={"size": 3},), justify='center',
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(html.H4('Tweets or Mentions',className="text-dark my-1 fs-2 text-center")
                    ,width={"size": 3},), justify='center',
        ),
        dbc.Row(
            dbc.Col(dcc.Dropdown(['Tweets', 'Mentions'], 'Mentions', multi=False, id='tweets-or-mentions-dropdown'),
                    width={"size": 3}, ), justify='center',
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(html.H4('No. of Days',className="text-dark my-1 fs-2 text-center")
                    ,width={"size": 3},), justify='center',
        ),
        dbc.Row(
            dbc.Col(dcc.Dropdown([i for i in range(2,11)], value=5,id='number-of-days-dropdown'),
                    width={"size": 3}, ), justify='center',
        ),
        html.Br(),]),
    dbc.Container([
        html.H2('Number of Followers', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='followers-area', justify="center"),
        html.Br(),
        html.H2('Tweet Counts', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='line-graph-area', justify="center"),
        html.Br(),
        html.H2('Tweet Sentiments', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='sentiments-area', justify="center"),
        html.Br(),
        html.H2('Wordcloud', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='wordcloud-area', justify="center"),
        html.Br(),
        html.H2('Latest #10 tweets', className="text-dark fw-bolder my-1 fs-2"),
        dbc.Row([], id='tweet-table-area', justify="center"),

    ]),
])














@callback(
    Output('followers-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_followers_count(brand_list, tweets_or_mentions, number_of_days):
    def follower_card(brandName):
        df = pd.read_excel('data/{}.xlsx'.format(brandName))
        return dbc.Card(dbc.CardBody(dbc.Row([
                    dbc.Col([
                        html.Div([html.P(brandName + ' @{}'.format(df.Brand[0]), className='card-title')], className="text-xs font-weight-bold text-primary text-uppercase mb-1"),
                        html.Div([html.P(df['number_of_followers'].tolist()[-1], id='followers_number_homepage')], className="h5 mb-0 font-weight-bold text-gray-800"),
                    ]),
                    dbc.Col([
                        html.Div(html.I(className="bi bi-person-circle"))
                    ], className='col-auto'),
                ], className='no-gutters align-items-center')), className='border-left-primary shadow h-100 py-2')
    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                            follower_card('TVS'),
                            ],
                           id='TVS-column', width="auto", className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    follower_card(brand),
                                    ],
                                   id=brand+'-column', width="auto", className='m-3'))
    return column_list


@callback(
    Output('line-graph-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_line_graph(brand_list, tweets_or_mentions, number_of_days):
    def line_grapher(brandName, tweets_or_mentions, number_of_days):
        df = pd.read_excel('data/{}.xlsx'.format(brandName))
        df = df[(df.flag == tweets_or_mentions.lower())].tail(number_of_days)
        x = df['date'].tolist()
        y = df['tweet_count'].tolist()
        return dcc.Graph(figure=go.Figure(
            data=[go.Scatter(x=x, y=y, mode='lines', marker=dict(color='#0066ff'))],
            layout={'title': tweets_or_mentions + ' Count of ' + brandName,
                    'xaxis': {'title': 'Number of days'},
                    'yaxis': {'title': 'Number of ' + tweets_or_mentions}}
        ))
    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                        line_grapher('TVS', tweets_or_mentions, number_of_days),
                            ],
                           id='TVS-column', width="auto", className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    line_grapher(brand, tweets_or_mentions, number_of_days),
                                    ],
                                   id=brand+'-column', width="auto", className='m-3'))
    return column_list




@callback(
    Output('sentiments-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_sentiments(brand_list, tweets_or_mentions, number_of_days):
    def sentiments(brandName):
        df = pd.read_excel('data/{}.xlsx'.format(brandName))
        df = df[(df.flag == tweets_or_mentions.lower())].tail(number_of_days)
        x = df['date'].tolist()
        return dcc.Graph(figure=dict(
            data=[dict(x=x,
                       y=df[j],
                       type='bar',
                       name=j) for j in ['POSITIVE', 'NEGATIVE']],
            layout=go.Layout(title='Sentiments count of '+brandName+' for '+tweets_or_mentions,
                             barmode='stack',
                             xaxis={'title': 'No. of days'},
                             yaxis={'title': 'Count of sentiments'})),
        )


    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                            sentiments('TVS'),
                            ],
                           id='TVS-column', width="auto", className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    sentiments(brand),
                                    ],
                                   id=brand+'-column', width="auto", className='m-3'))
    return column_list



@callback(
    Output('wordcloud-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_sentiments(brand_list, tweets_or_mentions, number_of_days):
    def wordclouder(brandName):
        df = pd.read_excel('data/{}.xlsx'.format(brandName))
        df = df[(df.flag == tweets_or_mentions.lower())].tail(number_of_days)
        rows =['Cleaned_translated_tweet', 'Hashtags']
        content_arr=[]
        for row in rows:
            ls = df[row.lower()].to_list()
            listToStr = ' '.join([str(elem) for elem in ls])
            listToStr = listToStr.translate({ord('['): None, ord(']'): None})
            if(row=='Hashtags'):
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

        return html.Div([html.H3(brandName),
            dbc.Tabs(
            [
                dbc.Tab(dbc.Card(
                    dbc.CardImg(src=content_arr[0], top=True), style={"width": "100%"}
                ), label='Cleaned_translated_tweet', style={"width": "75%"}),
                dbc.Tab(dbc.Card(
                    dbc.CardImg(src=content_arr[1], top=True), style={"width": "100%"}
                ), label='Hashtags', style={"width": "75%"}),
            ], style={"width": "75%"})], style={"width": "100%", "display": "inline-block"})


    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                            wordclouder('TVS'),
                            ],
                           id='TVS-column', width="auto", className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    wordclouder(brand),
                                    ],
                                   id=brand+'-column', width="auto", className='m-3'))
    return column_list


@callback(
    Output('tweet-table-area', 'children'),
    [Input('compete-brand-dropdown', 'value'),
     Input('tweets-or-mentions-dropdown', 'value'),
     Input('number-of-days-dropdown', 'value')])
def column_maker_sentiments(brand_list, tweets_or_mentions, number_of_days):
    def latesttweet(brandName):
        df = pd.read_excel('data/{}.xlsx'.format(brandName))
        df = df[(df.flag == tweets_or_mentions.lower())].tail(number_of_days)
        tweetArray =[]
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
            "Sr No":[i+1 for i in range(len(tweetArray))],
            "Tweet":tweetArray
        })
        return  html.Div([
            html.H3(brandName),
            dbc.Table.from_dataframe(new_df, striped=True, bordered=True, hover=True)
        ])


    if type(brand_list) == str:
        brand_list = [brand_list]
    column_list = [dbc.Col([
                            latesttweet('TVS'),
                            ],
                           id='TVS-column', width="auto", className='m-3')]
    for brand in brand_list:
        column_list.append(dbc.Col([
                                    latesttweet(brand),
                                    ],
                                   id=brand+'-column', width="auto", className='m-3'))
    return column_list