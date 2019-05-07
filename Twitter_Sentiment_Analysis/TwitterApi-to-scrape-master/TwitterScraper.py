import sys
import MySQLdb
import re
import time
from unidecode import unidecode
import twitterscraper
from twitterscraper import query_tweets

reload(sys)
sys.setdefaultencoding('utf-8')


def assignBrandTag(search_keyword):

    yoplait = ['generalmills yogurt', 'gogurt', 'trix yogurt', 'trixyogurt', 'yoplait', '#trixyogurt','#gogurt','#yoplait', '@yoplait']

    chobani = ['chobani flip', 'drink chobani', 'chobani kids', 'chobani gives', 'made with chobani', 'chobani cafe', 'chobaniflip',
               'drinkchobani', 'chobanikids', 'chobanigives', 'madewithchobani', 'chobanicafe', 'chobani', '#drinkchobani',
               '#chobanikids', '#chobanigives','#chobanicafe', '#chobaniflip', '#madewithchobani', '#chobani', '@chobanicafe', '@chobani']

    fage = ['fage crossovers', 'fage total', 'fage usa', 'fagecrossovers', 'fagetotal', 'fageusa', '#fagecrossovers',
            '#fagetotal', '#fageusa', '@fageusa']

    dannon = ['oikos', 'activia', 'actimel', 'dannonlight&fit', 'dannonlight', 'danimals', 'danactive', 'danonino', 'yocrunch',
              'dannon', '#dannonlight', '#dannonlight&fit', '#activia', '#oikos', '#danimals', '#danactive', '#danonino',
              '#yocrunch', '#actimel', '#dannon', '@activia', '@oikos', '@yocrunch', '@dannon']

    stonyfield = ['browncowyogurt', 'brown cow yogurt', 'stonyfield', '#browncowyogurt', '#stonyfield', '@browncowyogurt', '@stonyfield']

    noosa = ['noosamates', 'noosayoghurt', 'noosa yoghurt', '#noosamates', '#noosayoghurt', '@noosayoghurt']

    lala = ['be more lala', 'lala challenge', 'lala yogurt smoothies', 'lala yogurt', 'bemorelala', 'lalachallenge', 'lalayogurtsmoothies',
            'lalayogurt', '#bemorelala', '#lalachallenge', '#lalayogurtsmoothies', '#lalayogurt', '@lalayogurt']

    siggis = ['siggi skyr', 'siggi filmjolk', 'siggi tubes', 'siggi dairy', 'siggi yogurt', 'siggisdairy', '#siggisdairy', '@siggisdairy']

    voskos = ['voskos yogurt', 'govoskos', '#govoskos', '@govoskos']

    yami = ['yami yogurt', 'yamiyogurt', '#yamiyogurt', '@yamiyogurt']

    greekgods = ['seriously indulgent yogurt', 'greek gods yogurt', 'greek gods kefir', 'greek gods lebni', 'thegreekgods',
                 '#greekgodskefir', '#thegreekgods', '@thegreekgods']

    maia = ['maia yogurt', 'maiayogurt', '#maiayogurt', '@maiayogurt']

    tillamook = ['tillamook yogurt farmstyle greek', 'tillamook yogurt good creamy', 'tillamookcheese yogurt', 'tillamook yogurt', 'tillamookyogurt', '#tillamookyogurt', '@tillamookcheese yogurt']

    wallaby = ['wallaby organic', 'wallaby yogurt', 'wallaby kefir', 'wallabyyogurt', '#wallabyorganic', '#wallabyyogurt', '@wallabyyogurt']

    smari = ['smari yogurt', 'smari organics', 'smariorganics', '#smariorganics', '@smariorganics']

    liberte = ['liberte organic', 'liberte greek', 'liberte mediterranee', 'liberte yogurt', 'liberteorganic', 'libertegreek',
               'liberteyogurt', 'libertemediterranee', 'liberteusa', '#liberteusa', '@liberteusa']

    annies = ['annies yogurt', 'annies homegrown', 'annieshomegrown', '#annieshomegrown', '@annieshomegrown']

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
    elif search_keyword in tillamook: return 'tillamook'
    elif search_keyword in wallaby: return 'wallaby'
    elif search_keyword in smari: return 'smari'
    elif search_keyword in liberte: return 'liberte'
    elif search_keyword in annies: return 'annies'
    else: return 'Default'


def storeInDB(tweet_id, user, fullname, timestamp, text, search_keyword):
    print "Inside DB function"
    con = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="tiger123", db="twitter", use_unicode=True, charset="utf8")
    cursor = con.cursor()
    print search_keyword
    brand_tag = assignBrandTag(search_keyword)  # .replace('#','').replace('@','')

    scraped_tweets_table = "REPLACE INTO scraped_tweets_table (tweet_id, user, fullname, timestamp, text, search_keyword, brand_tag) " \
                       "VALUES (%s,%s,%s,%s,%s,%s,%s)"

    cursor.execute(scraped_tweets_table, (tweet_id, user, fullname, timestamp, text, search_keyword, brand_tag))

    con.commit()
    print 'DB operations performed'
    con.close()

# search_query_list = ['generalmills yogurt',	'gogurt', 'trix yogurt', 'trixyogurt', 'yoplait', '#trixyogurt', '#gogurt',
#                      '#yoplait', '@yoplait', 'chobani flip', 'drink chobani', 'chobani kids', 'chobani gives',
#                      'made with chobani', 'chobani cafe', 'chobaniflip', 'drinkchobani', 'chobanikids', 'chobanigives',
#                      'madewithchobani', 'chobanicafe', 'chobani', '#drinkchobani', '#chobanikids', '#chobanigives',
#                      '#chobanicafe', '#chobaniflip', '#madewithchobani', '#chobani', '@chobanicafe', '@chobani',
#                      'fage crossovers', 'fage total', 'fage usa', 'fagecrossovers', 'fagetotal', 'fageusa',
#                      '#fagecrossovers', '#fagetotal', '#fageusa', '@fageusa', 'oikos', 'activia', 'actimel',
#                      'dannonlight&fit',	'dannonlight', 'danimals', 'danactive', 'danonino',	'yocrunch',	'dannon',
#                      '#dannonlight', '#dannonlight&fit', '#activia', '#oikos', '#danimals',	'#danactive', '#danonino',
#                      '#yocrunch', '#actimel', '#dannon', '@activia', '@oikos', '@yocrunch',	'@dannon', 'browncowyogurt',
#                      'brown cow yogurt', 'stonyfield', '#browncowyogurt', '#stonyfield', '@browncowyogurt',	'@stonyfield',
#                      'noosamates', 'noosayoghurt', 'noosa yoghurt',	'#noosamates', '#noosayoghurt',	'@noosayoghurt',
#                      'be more lala', 'lala challenge', 'lala yogurt smoothies',	'lala yogurt', 'bemorelala', 'lalachallenge',
#                      'lalayogurtsmoothies',	'lalayogurt', '#bemorelala', '#lalachallenge', '#lalayogurtsmoothies',
#                      '#lalayogurt',	'@lalayogurt', 'siggi skyr', 'siggi filmjolk', 'siggi tubes', 'siggi dairy', 'siggi yogurt',
#                      "siggi's skyr", "siggi's filmjolk", "siggi's tubes", "siggi's dairy", "siggi's yogurt",
#                      'siggisdairy',	'#siggisdairy',	'@siggisdairy',	'voskos yogurt', 'govoskos', '#govoskos', '@govoskos',
#                      'yami yogurt',	'yamiyogurt', '#yamiyogurt', '@yamiyogurt',	'seriously indulgent yogurt', 'greek gods yogurt',
#                      'greek gods kefir', 'greek gods lebni', 'thegreekgods', '#greekgodskefir', '#thegreekgods', '@thegreekgods',
#                      'maia yogurt',	'maiayogurt', '#maiayogurt', '@maiayogurt',	'wallaby organic', 'wallaby yogurt', 'wallaby kefir',
#                      'wallabyyogurt', '#wallabyorganic', '#wallabyyogurt', '@wallabyyogurt', 'smari yogurt', 'smari organics',
#                      'smariorganics', '#smariorganics',	'@smariorganics', 'liberte organic', 'liberte greek', 'liberte mediterranee',
#                      'liberte yogurt', 'liberteorganic', 'libertegreek', 'liberteyogurt', 'libertemediterranee', 'liberteusa',
#                      '#liberteusa',	'@liberteusa', 'annies yogurt',	'annies homegrown',	'annieshomegrown', '#annieshomegrown',
#                      '@annieshomegrown']

# tweet_handles = ['@yoplait', '@chobanicafe', '@chobani', '@fageusa', '@activia', '@oikos', '@yocrunch',	'@dannon',
#                  '@browncowyogurt',	'@stonyfield', '@noosayoghurt', '@lalayogurt', '@siggisdairy', '@govoskos',
#                  '@yamiyogurt', '@thegreekgods', '@maiayogurt', '@wallabyyogurt', '@smariorganics', '@liberteusa', '@annieshomegrown']

search_query_list = ['generalmills yogurt',	'gogurt', 'trix yogurt', 'trixyogurt', 'yoplait', '#trixyogurt', '#gogurt',
                     '#yoplait', '@yoplait', 'chobani flip', 'drink chobani', 'chobani kids', 'chobani gives',
                     'made with chobani', 'chobani cafe', 'chobaniflip', 'drinkchobani', 'chobanikids', 'chobanigives',
                     'madewithchobani', 'chobanicafe', 'chobani', '#drinkchobani', '#chobanikids', '#chobanigives',
                     '#chobanicafe', '#chobaniflip', '#madewithchobani', '#chobani', '@chobanicafe', '@chobani',
                     'oikos', 'activia', 'actimel', 'dannonlight&fit',	'dannonlight', 'danimals', 'danactive',
                     'danonino', 'yocrunch', 'dannon', '#dannonlight', '#dannonlight&fit', '#activia', '#oikos',
                     '#danimals', '#danactive', '#danonino', '#yocrunch', '#actimel', '#dannon', '@activia',
                     '@oikos', '@yocrunch',	'@dannon']

flag_list = []
for searchQuery in search_query_list:
    try:
        if searchQuery not in flag_list:
            start_time = time.time()
            print "Start Time : %s" % (time.asctime(time.gmtime(start_time)))
            for tweet in query_tweets(searchQuery, limit=20000):
                tweet_id = tweet.id.encode('utf-8')
                user = re.sub('[^A-Za-z0-9]+', ' ', unidecode(tweet.user).encode('utf-8'))
                fullname = re.sub('[^A-Za-z0-9]+', ' ', unidecode(tweet.fullname).encode('utf-8'))
                timestamp = tweet.timestamp
                text = re.sub('[^A-Za-z0-9]+', ' ', unidecode(tweet.text).encode('utf-8'))
                print tweet_id, user, fullname, timestamp, text, searchQuery
                storeInDB(tweet_id, user, fullname, timestamp, text, searchQuery)

            end_time = time.time()
            print "End Time : %s" % (time.asctime(time.gmtime(end_time)))
            time_difference = end_time - start_time
            hours = time_difference // 3600
            time_difference = time_difference - 3600 * hours
            minutes = time_difference // 60
            seconds = time_difference - 60 * minutes
            flag_list.extend(searchQuery)
            print "Time Taken for Keyword %s =  %s Hours %s Minutes %s seconds" % (searchQuery, hours, minutes,seconds)
    except Exception, e:
        print e

print "######## End of Process ########"
