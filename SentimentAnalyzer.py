from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import MySQLdb
import pandas as pd
import nltk
from pylab import *
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf-8')

analyser = SentimentIntensityAnalyzer()


def assignSentiment(x, pos_cutoff, neg_cutoff):
    sentiment = 2
    if x > pos_cutoff:
        sentiment = 1
        return sentiment
    elif x < neg_cutoff:
        sentiment = -1
        return sentiment
    elif (x >= neg_cutoff) and (x <= pos_cutoff):
        sentiment = 0
        return sentiment
    else:
        return sentiment


def sentimentCounter(df, val):
    x = df
    count = 0
    for value in x:
        if value == val:
            count += 1

    return count


con = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="tiger123", db="twitter", use_unicode=True, charset="utf8")
cursor = con.cursor()

words = set(nltk.corpus.words.words())

brand_tag_list = ('yoplait', 'chobani', 'fage', 'dannon', 'stonyfield', 'noosa', 'voskos', 'lala', 'yami', 'siggis',
                  'greekgods', 'maia', 'wallaby', 'smari', 'liberte', 'annies')
# brand_tag_list = ('yami','maia', 'wallaby')
stats_df = pd.DataFrame()

queryStr = "SELECT tweet_id, brand_tag, text FROM scraped_tweets_tbl where brand_tag in %s" % str(brand_tag_list)
print queryStr
tweets_df = pd.read_sql(queryStr, con)
# to remove spanish text and then compute scores - not working properly
# tweets_df['text'] = tweets_df['text'].apply(lambda x: " ".join(w for w in nltk.wordpunct_tokenize(x) if w.lower() in words or not w.isalpha()) )
tweets_df['vaderScore'] = tweets_df['text'].apply(lambda x: analyser.polarity_scores(x)['compound'])

# tweets_df.boxplot(column='vaderScore').plot()
# plt.show()
# quantiles = tweets_df['vaderScore'].quantile([0.01, 0.25, 0.5, 0.7,0.71,0.72,0.73,0.74, 0.75, 0.99])
# print quantiles

pos_cutoff_list = list(tweets_df['vaderScore'].quantile([0.75]))
neg_cutoff_list = list(tweets_df['vaderScore'].quantile([0.25]))
pos_cutoff = pos_cutoff_list[0]
neg_cutoff = neg_cutoff_list[0]

tweets_df['vaderSentiment'] = tweets_df['vaderScore'].apply(lambda x: assignSentiment(x, pos_cutoff, neg_cutoff))
# print tweets_df
tweets_df.to_csv("/home/nithish/Downloads/twitter/allvaderscoresAug25.csv", index=False)

# stats_df = final_df.groupby(['brand_tag'], as_index=False).agg({'vaderScore': ['mean', 'std']})
stats_df['vaderMean'] = tweets_df.groupby(['brand_tag'])['vaderScore'].apply(lambda x: x.mean())
stats_df = stats_df.sort_values('vaderMean', ascending=False)
# stats_df['vaderSD'] = tweets_df.groupby(['brand_tag'])['vaderScore'].apply(lambda x: x.std())
# stats_df['brandScore'] = stats_df['vaderMean'] - stats_df['vaderSD']
stats_df['brandSentiment'] = stats_df['vaderMean'].apply(lambda x: assignSentiment(x, pos_cutoff, neg_cutoff))
stats_df['posCount'] = tweets_df.groupby(['brand_tag'])['vaderSentiment'].apply(lambda x: sentimentCounter(x, 1))
stats_df['neuCount'] = tweets_df.groupby(['brand_tag'])['vaderSentiment'].apply(lambda x: sentimentCounter(x, 0))
stats_df['negCount'] = tweets_df.groupby(['brand_tag'])['vaderSentiment'].apply(lambda x: sentimentCounter(x, -1))
stats_df['pcPosWithinBrand'] = 100 * (stats_df['posCount'] / (stats_df['posCount'] + stats_df['neuCount'] + stats_df['negCount']))
stats_df['pcNegWithinBrand'] = 100 * (stats_df['negCount'] / (stats_df['posCount'] + stats_df['neuCount'] + stats_df['negCount']))
stats_df['pcNeuWithinBrand'] = 100 * (stats_df['neuCount'] / (stats_df['posCount'] + stats_df['neuCount'] + stats_df['negCount']))
stats_df['pcPosAcrossBrands'] = 100 * (stats_df['posCount'] / (stats_df['posCount'].sum()))
stats_df['pcNegAcrossBrands'] = 100 * (stats_df['negCount'] / (stats_df['negCount'].sum()))
stats_df['pcNeuAcrossBrands'] = 100 * (stats_df['neuCount'] / (stats_df['neuCount'].sum()))
# stats_df['OverallSentiment'] = stats_df[['posCount', 'neuCount', 'negCount']].idxmax(axis=1)
stats_df = stats_df.reset_index()
print stats_df
stats_df.to_csv("/home/nithish/Downloads/twitter/groupedstatsvaderAug25.csv", index=False)
