import MySQLdb
import time
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
import gensim
from gensim import corpora

con = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="tiger123", db="twitter", use_unicode=True, charset="utf8")
cursor = con.cursor()

# brand_tag_list = ['yoplait', 'chobani', 'fage', 'dannon', 'stonyfield', 'noosa', 'voskos', 'lala', 'yami', 'siggis',
#                   'greekgods', 'maia', 'wallaby', 'smari', 'liberte', 'annies']

brand_tag_list = ['dannon']

lemma = WordNetLemmatizer()
Lda = gensim.models.ldamodel.LdaModel
stopwordsset = set(stopwords.words("english") + list(string.punctuation) + ["rt", "via", "https", "http", "twitter"])


def getBrandTweets(brand):
    # query = "select text from scraped_tweets_tbl where brand_tag='"+brand+"' "
    query = "select text from scraped_tweets_tbl where brand_tag='"+brand+"'and date_format(scraped_tweets_tbl.timestamp,'%Y-%m') in ('2016-12','2017-01','2017-02') "
    cursor.execute(query)
    tweets = cursor.fetchall()
    return tweets


def clean(doc):
    tokenized_tweet_text = word_tokenize(doc)
    filtered_words_stop = [str(word) for word in tokenized_tweet_text if word not in stopwordsset]
    filtered_words_num = [str(word) for word in filtered_words_stop if not word.isdigit()]
    filtered_words_alpha = [str(word) for word in filtered_words_num if word.isalpha()]
    filtered_words = [str(word).lower() for word in filtered_words_alpha if len(word) > 3]
    normalized = " ".join(lemma.lemmatize(word) for word in filtered_words)
    return normalized

# final_df = pd.DataFrame()

for brand in brand_tag_list:
    start_time = time.time()
    print "Start Time : %s" % (time.asctime(time.gmtime(start_time)))
    print "Processing Brand : %s" % brand
    doc_clean = [clean(doc[0]).split() for doc in getBrandTweets(brand)]

    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

    ldamodel = Lda(doc_term_matrix, num_topics=5, id2word = dictionary, passes=200)
    lda_list = ldamodel.print_topics(num_topics=5, num_words=10)
    # print lda_list
    lda_df = pd.DataFrame(lda_list, columns=['topicNo', 'topicWords'])
    lda_df['brand'] = brand
    # print lda_df
    end_time = time.time()
    print "End Time : %s" % (time.asctime(time.gmtime(end_time)))
    time_difference = end_time - start_time
    hours = time_difference // 3600
    time_difference = time_difference - 3600 * hours
    minutes = time_difference // 60
    seconds = time_difference - 60 * minutes
    print "Time Taken for Brand  %s =  %s Hours %s Minutes %s seconds" % (brand, hours, minutes, seconds)

    lda_df.to_csv("/home/nithish/Downloads/twitter/topicmodellingresultsdannonpeakAug28_" + brand + ".csv", index=False)

    # final_df = final_df.append(lda_df, ignore_index=True)

# print final_df
# final_df.to_csv("/home/nithish/Downloads/twitter/topicmodellingresults.csv", index=False)
