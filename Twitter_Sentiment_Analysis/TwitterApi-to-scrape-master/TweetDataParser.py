import sys
import MySQLdb
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8')

stopwordsset = set(stopwords.words("english") + list(string.punctuation) + ["rt", "via", "https", "http"])

con = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="tiger123", db="twitter", use_unicode=True,
                      charset="utf8")
cursor = con.cursor()
brand_tag_list = ['yoplait', 'chobani', 'fage', 'dannon', 'stonyfield', 'noosa', 'voskos', 'lala', 'yami', 'siggis',
                  'greekgods', 'maia', 'wallaby', 'smari', 'liberte', 'annies']

final_df = pd.DataFrame()
for brand in brand_tag_list:
    queryStr = "SELECT * FROM scraped_tweets_table where brand_tag='%s'" % brand
    tweets_df = pd.read_sql(queryStr,con)
    tweet_text = ''

    for row in tweets_df['text']:
        tweet_text = tweet_text + row

    tweet_text = tweet_text.lower().replace('#','').replace('@','')

    tokenized_tweet_text = word_tokenize(tweet_text)
    filtered_words_stop = [str(word) for word in tokenized_tweet_text if word not in stopwordsset]
    filtered_words = [str(word) for word in filtered_words_stop if len(word)>3]
    word_count = Counter(str(word) for word in filtered_words)
    frequent_words = word_count.most_common(30)
    # print "%s : %s" % (brand, frequent_words)
    df = pd.DataFrame({'word_tuple': frequent_words})
    df[['word', 'count']] = df['word_tuple'].apply(pd.Series)
    df['brand'] = brand
    final_df = final_df.append(df,ignore_index=True)

print final_df
final_df = final_df.drop('word_tuple', axis=1)
final_df.to_csv("/home/nithish/Downloads/twitter/word_count.csv", index=False)
