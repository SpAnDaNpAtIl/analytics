import pandas as pd
import numpy as np



twitter_auth={'CONSUMER_KEY': 'NZHPBeGdlM5xmmZrobPCs0RBJ',
'CONSUMER_SECRET': '0Q6zTe9aSwktTQHId2tK8Lnx4IIIzrGWOMyMXzWq7D5iJ0NzeM',
'ACCESS_TOKEN': '94728153-SWsjUyzPHKi3MQzvM8IhKwVRFJHeepMVygzF905st',
'ACCESS_TOKEN_SECRET': 'bVg7bhDwqw4vWrR9w7ubO9sPCTKCHieCEr6JCk8eCwErY',
'BEARER_TOKEN':'AAAAAAAAAAAAAAAAAAAAAGDdJwEAAAAAM8DWT3HezUpsFcz8VIxdDHQt0Wc%3DVYP9QLrBOF1EmFzUnSwV6ScwXL0d5fb57DOPl3hIvaOSZDVtDw'}


my_data={'id_3':'tvsmotorcompany'}
# tvsmotorcompany
# honda2wheelerin
# HeroMotoCorp

my_brand={'brand_name':'TVS'}



my_count={'count_my':1500}

my_day_hist={'hist_my':15}


my_stopwords=[
    'hence', 'since', 'she', 'above', 'not', "there's", "won't", "we've","will","tv",
    "hi","tvs","th","hero","honda","t","bike","day","s","days",
    'herself', 'in', 'however', 'k', 'him', 'itself', 'ours', "mustn't", 'of',
    'am', 'both', 'down', 'few', 'on', 'off', 'or', "shan't", 'own', 'cannot',
    'else', 'before', 'a', "who's", 'is', 'do', 'if', 'during', 'into', 'but',
    "he's", "here's", 'any', 'very', 'here', "why's", 'yourself', "weren't",
    'for', 'no', 'what', 'me', 'where', "i've", "it's", "they've", 'until',
    'have', 'has', "they're", "wouldn't", "we'll", 'through', "i'd", "she's",
    'other', 'again', 'than', "we'd", 'because', "they'd", 'which', 'while',
    "you're", 'all', 'also', 'and', "i'm", 'ought', 'were', "what's", 'most',
    'out', 'we', 'their', 'between', 'are', "you'd", 'com', 'http', 'he',
    'they', 'why', "how's", 'to', 'that', 'with', 'our', 'should', "can't",
    'does', "hasn't", "didn't", "when's", 'these', 'after', 'i', 'just',
    'myself', "hadn't", 'more', 'how', "that's", 'otherwise', 'about', 'by',
    'when', 'further', 'therefore', 'who', "couldn't", 'against', 'been',
    'doing', 'it', "she'll", 'theirs', 'themselves', "haven't", 'himself',
    "i'll", 'then', 'ourselves', "she'd", 'some', 'my', 'too', 'each', 'being',
    "aren't", 'having', "don't", "he'll", "they'll", "you've", 'below', 'its',
    "you'll", "isn't", 'you', 'her', 'ever', "wasn't", 'your', 'be', "let's",
    'those', 'under', "he'd", 'yourselves', 'them', 'there', 'yours',
    "doesn't", 'was', 'over', "shouldn't", 'had', 'r', 'same', 'once', 'only',
    'can', 'nor', 'as', 'at', 'the', 'www', 'did', 'his', 'so', 'like',
    'could', 'such', 'up', 'shall', 'whom', 'hers', "we're", 'this', "where's",
    'from', 'get', 'an', 'would']


# 'id_1' : 'elonmusk','id_2' : 'Pankaj_Udaipur','id_4':'honda2wheelerin','id_5':'HeroMotoCorp'