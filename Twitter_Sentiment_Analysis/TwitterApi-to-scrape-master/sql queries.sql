use twitter;

select count(*) from handle_tweets_table;
select count(*) from handle_users_table;
select * from handle_users_table;
--  where screen_name in ('Yoplait', 'Chobani', 'FAGEUSA', 'Dannon', 'Stonyfield', 'browncowyogurt', 'noosayoghurt', 'GoVoskos', 'LalaYogurt', 'YamiYogurt', 'siggisdairy', 'YoCrunch', 'TheGreekGods', 'MaiaYogurt');
select * from handle_tweets_table where brand_tag='smari';
select search_keyword, count(*) from handle_tweets_table group by search_keyword;
select brand_tag, count(*) from handle_tweets_table group by brand_tag;
select brand_tag, max(date(created_at)) from handle_tweets_table group by brand_tag;
select search_keyword, max(date(created_at)) from handle_tweets_table group by search_keyword;


select count(*) from scraped_tweets_table;
select * from scraped_tweets_table limit 50;
select * from scraped_users_table;
select search_keyword, count(*) from scraped_tweets_table group by search_keyword;
select brand_tag, count(*) from scraped_tweets_table group by brand_tag;
