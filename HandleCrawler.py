import tweepy
import sys
import MySQLdb
import re
from unidecode import unidecode

reload(sys)
sys.setdefaultencoding('utf-8')

consumer_key = 'XiDleVnNiEk8cLnyCDYAs7kV2'
consumer_secret = 'pYsq6m1CZwQElHEYOpqHFUycNbyrOBHU4vdEwaMuJYmisoL5Oy'
access_token = '2496071610-zNhNmQVfJmvauEsCcB80n4yxpgkTIlgSoVspDoZ'
access_token_secret = 'csB1HnWfCUDdBkNIvz11vQMZi1DtbjKsrHgBoaiQjbaBx'


def tweepyAuthenticate(consumerKey, consumerSecret):
    auth = tweepy.AppAuthHandler(consumerKey, consumerSecret)
    tweetApi = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5, timeout=1000)

    if not tweetApi:
        print "Can't Authenticate using these Keys"
        sys.exit(-1)
    else:
        print "Authenticated"

    return tweetApi


def assignBrandTag(search_keyword):

    yoplait = ['@yoplait']
    chobani = ['@chobanicafe', '@chobani']
    fage = ['@fageusa']
    dannon = ['@activia', '@oikos', '@yocrunch', '@dannon']
    stonyfield = ['@browncowyogurt', '@stonyfield']
    noosa = ['@noosayoghurt']
    lala = ['@lalayogurt']
    siggis = ['@siggisdairy']
    voskos = ['@govoskos']
    yami = ['@yamiyogurt']
    greekgods = ['@thegreekgods']
    maia = ['@maiayogurt']
    wallaby = ['@wallabyyogurt']
    smari = ['@smariorganics']
    liberte = ['@liberteusa']
    annies = ['@annieshomegrown']

    if search_keyword in yoplait: return 'yoplait'
    elif search_keyword in chobani: return 'chobani'
    elif search_keyword in fage: return 'fage'
    elif search_keyword in dannon: return 'dannon'
    elif search_keyword in stonyfield: return 'stonyfield'
    elif search_keyword in noosa: return 'noosa'
    elif search_keyword in lala: return 'lala'
    elif search_keyword in siggis: return 'siggis'
    elif search_keyword in voskos: return 'voskos'
    elif search_keyword in yami: return 'yami'
    elif search_keyword in greekgods: return 'greekgods'
    elif search_keyword in maia: return 'maia'
    elif search_keyword in wallaby: return 'wallaby'
    elif search_keyword in smari: return 'smari'
    elif search_keyword in liberte: return 'liberte'
    elif search_keyword in annies: return 'annies'
    else: return 'Default'


def storeInDB(tweetsData, search_keyword):
    print "Inside DB function"
    con = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="tiger123", db="twitter", use_unicode=True, charset="utf8")
    print search_keyword
    cursor = con.cursor()

    for tweet in tweetsData:
        handle_tweets_table = "REPLACE INTO handle_tweets_table (tweet_id, tweet_reply_status_id, text, retweet_count, " \
                              "favorite_count, favorited, retweeted, tweet_lang, user_id, created_at, search_keyword, brand_tag) " \
                              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        handle_users_table = "REPLACE INTO handle_users_table (user_id, user_name, screen_name, description, favorites_count, " \
                              "followers_count, statuses_count, friends_count, listed_count, location, language, time_zone, created_at, " \
                              "search_keyword, brand_tag) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        brand_tag = assignBrandTag(search_keyword)  # .replace('#','').replace('@','')
        tweet_id = tweet.id
        tweet_reply_status_id = tweet.in_reply_to_status_id
        retweet_count = tweet.retweet_count
        favorite_count = tweet.favorite_count
        favorited = tweet.favorited
        retweeted = tweet.retweeted
        tweet_lang = tweet.lang
        user_id = tweet.user.id
        created_at = tweet.created_at

        if tweet.text:
            text = re.sub('[^A-Za-z0-9]+', ' ', unidecode(tweet.text).replace("'", "").encode('utf-8'))
        else:
            text = tweet.text

        if tweet.user.name:
            user_name = re.sub('[^A-Za-z0-9]+', ' ', unidecode(tweet.user.name).encode('utf-8'))
        else:
            user_name = tweet.user.name

        if tweet.user.screen_name:
            screen_name = re.sub('[^A-Za-z0-9]+', ' ', unidecode(tweet.user.screen_name).encode('utf-8'))
        else:
            screen_name = tweet.user.screen_name

        if tweet.user.description:
            description = re.sub('[^A-Za-z0-9]+', ' ', unidecode(tweet.user.description).replace("'", "").encode('utf-8'))
        else:
            description = tweet.user.description

        if tweet.user.location:
            location = re.sub('[^A-Za-z0-9]+', ' ', unidecode(tweet.user.location).encode('utf-8'))
        else:
            location = tweet.user.location

        favorites_count = tweet.user.favourites_count
        followers_count = tweet.user.followers_count
        statuses_count = tweet.user.statuses_count
        friends_count = tweet.user.friends_count
        listed_count = tweet.user.listed_count
        language = tweet.user.lang
        time_zone = tweet.user.time_zone
        user_created_at = tweet.user.created_at

        cursor.execute(handle_tweets_table, (tweet_id, tweet_reply_status_id, text, retweet_count, favorite_count,
                                             favorited, retweeted, tweet_lang, user_id, created_at, search_keyword, brand_tag))

        cursor.execute(handle_users_table, (user_id, user_name, screen_name, description, favorites_count,
                                            followers_count, statuses_count, friends_count, listed_count, location,
                                            language, time_zone, user_created_at, search_keyword, brand_tag))

    con.commit()
    print 'DB operations performed'
    con.close()


tweet_handles = ['@yoplait', '@chobanicafe', '@chobani', '@fageusa', '@activia', '@oikos', '@yocrunch',	'@dannon',
                 '@browncowyogurt',	'@stonyfield', '@noosayoghurt', '@lalayogurt', '@siggisdairy', '@govoskos',
                 '@yamiyogurt', '@thegreekgods', '@maiayogurt', '@wallabyyogurt', '@smariorganics', '@liberteusa', '@annieshomegrown']


api = tweepyAuthenticate(consumer_key, consumer_secret)

for handle in tweet_handles:
    try:
        tweets_data = api.user_timeline(screen_name=handle, count=200)
        storeInDB(tweets_data, handle)
        alltweets = []
        alltweets.extend(tweets_data)
        oldest = alltweets[-1].id - 1
        print "Oldest : %s" % oldest

        while len(tweets_data) > 0:
            print "Getting tweets before Tweet ID %s for %s" % (oldest, handle)
            tweets_data = api.user_timeline(screen_name=handle, count=200, max_id=oldest)
            storeInDB(tweets_data,handle)
            alltweets.extend(tweets_data)
            oldest = alltweets[-1].id - 1
            print "Tweets downloaded so far for %s : %s" % (handle, len(alltweets))
    except Exception, e:
        print e

print "######## End of Process ########"
