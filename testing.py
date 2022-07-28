import pandas as pd

ddf = pd.read_excel('data/{}.xlsx'.format('TVS'))

k = ddf[(ddf.flag == 'Tweets'.lower())]['date', 'tweet_count'].tolist()[-5:]