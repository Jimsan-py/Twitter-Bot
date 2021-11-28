''' decompose the task into subtasks & assign a function for each subtask
SDLC SW development lifecycle

**************************************************************************************************************************
Functional Requirement 	
- Functional Requirements Form The Behavior Of The Product.
- They Explain “What The System Does.”	
- Helps You Verify The Functionality Of The Software.	
- They Are Captured In Use Cases.	
- Easy To Define.	
- Focus On User Requirement.	


Non-functional Requirements
- Non-functional requirements describe the general software characteristics.
- They explain “How the system works.”
- Helps you verify the performance of the software.
- They are captured as a quality attribute.
- Difficult to define.
- Focus on the user's expectation and experience.

--------------------------------------------------------------------------------------------------------------------------
A. What - Requirement Analysis - Functional Requirements (FRs)

What?: a Twitter Bot that gathers tweets relating to commodities

Big Brain Commodities
In retrospect, it was inevitable."

Prerequisites:
- Acquiring a Twitter Developer Account [DONE]

FR 1. Like a tweet using a random search term from list.
FR 2 Retweet a tweet relating to commodities by select
group of friends in past day
FR 3. Retweet a trending tweet
FR 4. Follow people who are following list of trusted users.
FR 5. Extract commodity prices from CNBC and tweet.
Only do this once every six hours.
FR 4. News generator - specified scraper function to extract news headlines.
Generate hashtags. Use google news
FR 5. Sleep between FR 1 - 5 for 30 mins to an hour

#use random intervals for sleep to make more human like

Non-functional requirements (NFRs) - UI, effectiveness, security
NFR1. Connect To Twitter and get API tokens #

Notes-------------------------------
Use hashtags
extract headlines and use links in tweets
Use emojis
Link to twitter feed using $

--------------------------------------------------------------------------------------------------------------------------
B. How - Design
Classes
BB_Com
BB_comDemo

methods
init()
search_and_like()
retweet_using_search_terms()

Resources
https://www.freecodecamp.org/news/how-to-build-and-deploy-a-multifunctional-twitter-bot-49e941bb3092/
--------------------------------------------------------------------------------------------------------------------------
C. Write the code - Implementation'''
from datetime import date, datetime
from random import choice, randint
from time import sleep
from urllib.request import urlopen

from bs4 import BeautifulSoup
from requests import get, session
import re
from tweepy import API, Cursor, OAuthHandler, TweepError
from selenium import webdriver
from collections import Counter
from string import punctuation
import operator
# import RAKE
from James_twitter_bot_keys_tokens import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()


class BB_Com():

    def __init__(self):
        '''Constructor, called when we create an object of the class
        '''
        self.public_tweets = ''
        self.followers_count = 0
        self.tweet_count = 0
        self.results = []
        self.count = 0
        self.term_list = ["Copper market", "tin market", "shipping market",
                          "coal market", "lithium market",
                          "natural gas market", "rare earth metals",
                          "freight market",
                          "metals market", "oil market",
                          "LNG market", "crude oil market",
                          "precious metals markets", "wheat market",
                          "green energy commodities",
                          "batteries electric vehicles",
                          "base metals", "iron ore market"]
        self.retweet_from_selected_user_list = ['dscrybe',
                                                     'onlyanna100',
                                                     'jfarchy',
                                                     'RhiannonHoyle',
                                                     'Edspencive',
                                                     'PeterSainsbury7',
                                                     'FinancialTimes',
                                                     'ArgusMedia',
                                                     'commoditypress',
                                                     'PlattsGas',
                                                     'amran_abocar',
                                                     'USDA',
                                                     'ftenergy',
                                                     'IEA',
                                                     'base_metals',
                                                     'BloombergNEF',
                                                     'BaseMetals',
                                                     'plattsmetals',
                                                     'ClydeCommods',
                                                     'ETCommodities',
                                                     'ReutersCommods',
                                                     'BNCommodities',
                                                     'ftcommodities',
                                                     'plattsshipping',
                                                     'ReutersAg',
                                                     'climatefinance',
                                                     'LloydsList',
                                                     'IHSMarkitMandT']
        self.nrTweets_random_search = 0
        self.nrTweets_following = 0
        self.retweets_count = 0
        self.price_dict = {}
        self.url_prices_cnbc_dict = {
                                     "$WTI Crude":
                                        "https://www.cnbc.com/quotes/@CL.1",
                                     "$Natural Gas":
                                         "https://www.cnbc.com/quotes/@NG.1",
                                     "$Gold":
                                         "https://www.cnbc.com/quotes/@GC.1",
                                     "$Copper":
                                         "https://www.cnbc.com/quotes/@HG.1",
                                     "$Wheat":
                                         "https://www.cnbc.com/quotes/@W.1",
                                     "$Soybeans":
                                         "https://www.cnbc.com/quotes/@S.1",
                                     "$Corn":
                                         "https://www.cnbc.com/quotes/@C.1",
                                     "$Dollar Index Future":
                                         "https://www.cnbc.com/quotes/@DX.1"}
        self.tweet_text = ""
        self.tweet_text_2 = ""
        self.tweet_text_3 = ""
        self.price_tweet_counter = 0
        self.price_tweet_timestamp = ''
        self.text_file = ''
        self.google_commodities_news_links = ["https://news.google.com/rss/search?q=commodities", 
                                              "https://news.google.com/rss/search?q=commodities+news", 
                                              "https://news.google.com/rss/search?q=commodities+markets", 
                                              "https://news.google.com/rss/search?q=commodities+price",
                                              "https://news.google.com/rss/search?q=energy+market",
                                              "https://news.google.com/rss/search?q=metals+market",
                                              "https://news.google.com/rss/search?q=agricultural+commodity+market"]
        self.articles_headlines = ''
        self.link = ''
        self.tweet_article_hashtags = ''
        self.stop_dir = "C:\\Users\\jhamilton2\\Desktop\\Python\\twitter bot\\stop_words.txt"
        self.followers = api.followers_ids("CommoditiesBb")
        self.friends = api.friends_ids("CommoditiesBb")

    def search_and_like(self):
        self.nrTweets_following = 10
        self.nrTweets_random_search = 1

        success_like = False

        for tweet in Cursor(api.search, choice(self.term_list)).items(self.nrTweets_random_search):
            if not success_like:
                try:
                    tweet.favorite()
                    print("Tweet Liked")
                    success_like = True
                    break
                except TweepError as e:
                    print("kek...error")
                    print(e.reason)
                except Exception as general_exception:
                    print("An exception occurred")

    def retweet_from_selected_user_list_method(self):
        
        success_retweet = False

        for tweet in Cursor(api.user_timeline, screen_name=choice(self.retweet_from_selected_user_list)).items():
            if not success_retweet:
                if(datetime.utcnow() - tweet.created_at).days < 1:
                    try:
                        print('\nTweet by :' + tweet.user.screen_name)
                        tweet.retweet()
                        print("retweeted the tweet")
                        success_retweet = True
                        break
                    except TweepError as e:
                        print(e.reason)
                    except Exception as general_exception:
                        print("An exception occurred")

    def prices_scraper_cnbc(self):
        # while True:
        key_list = list(self.url_prices_cnbc_dict.keys())
        print(key_list)
        counter = 0
        self.tweet_text = ""
        d = date.today().weekday()
        if d in range(5):
            for i in self.url_prices_cnbc_dict:
                # if counter < len(key_list):
                    try:
                        result = get(self.url_prices_cnbc_dict[i])
                        c = result.content
                        soup = BeautifulSoup(c, 'html.parser')
                        time_of_information = soup.find("div", {"class": ["QuoteStrip-lastTradeTime"]})
                        current_price = soup.find("span", {"class": ["QuoteStrip-lastPrice"]})
                        current_change_price = soup.find("span", {"class": ["QuoteStrip-changeUp"]})
                        current_change_price_percentage = soup.find("span", {"class": ["QuoteStrip-changeUp"]})
                        price_text = f"{key_list[counter]}: {current_price.get_text()} "
                        current_change_price_text = f"{current_change_price.get_text()} "
                        print(f"{key_list[counter]} change in price : {current_change_price.get_text()} ")
                        if '+' in current_change_price_text:
                            emoji = 'U+2B06 \n'
                        elif '-' in current_change_price_text:
                            emoji = 'U+2B07 \n'
                        combined_prices_and_emojis = price_text + current_change_price_text + emoji
                        self.tweet_text += combined_prices_and_emojis
                        counter += 1
                    except TweepError as e:
                        print(e.reason)
                    except Exception as general_exception:
                        print("An exception occurred")
        cnbc_time = f"USD - Source: CNBC {time_of_information.get_text()}"
        print(cnbc_time)
        self.tweet_text += cnbc_time
        '''
                    https://hackersandslackers.com/scraping-urls-with-beautifulsoup/

                    https://realpython.com/beautiful-soup-web-scraper-python/
                    https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup
                    '''
        counter = 0 
        
    def tweet_prices(self):
        self.text_file = open("C:\\Users\\jhamilton2\\Desktop\\Python\\twitter bot\\time_stamp_tweet.txt", "w")
        if self.tweet_text:
            try:
                tweet_prices_one_tweet = api.update_status(self.tweet_text)
                print("First price tweet")
                self.price_tweet_counter += 1  # work on this
                self.tweet_time_stamp = tweet_prices_one_tweet.created_at
                print(self.tweet_time_stamp)
                with self.text_file as fout:
                    print("opening write_file")
                    fout.write(str(self.tweet_time_stamp)) # str(tweet_prices_one_tweet.created_at())
            except TweepError as e:
                print(e.reason)

    def follow_people(self):
        for i in range(3):
            try:
                random_person_i_follow = choice(self.retweet_from_selected_user_list)
                followers_of_single_person_i_follow_ids = api.followers_ids(random_person_i_follow)
                random_follower_of_someone_i_follow = choice(followers_of_single_person_i_follow_ids)
                user = api.get_user(random_follower_of_someone_i_follow)
                api.create_friendship(random_follower_of_someone_i_follow)
                print(f"From {random_person_i_follow}'s follower list, you followed {user.screen_name}")
            except TweepError as e:
                print(e.reason)
            except Exception as general_exception:
                print("An exception occurred")

    def compare_price_tweet_timestamp_to_present(self):
        try:
            with open("C:\\Users\\jhamilton2\\Desktop\\Python\\twitter bot\\time_stamp_tweet.txt", "r") as file:
                first_line = file.readline()

            timestamp1 = first_line
            timestamp2 = str(datetime.utcnow())

            print(timestamp1)
            print(timestamp2)
            t1 = datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S") #UTC
            t2 = datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S.%f") #UTC
            print(f"{t1} UTC")
            print(f"{t2} UTC")
            difference = t1 - t2
            print(f"difference:{difference}")

            diff_seconds = difference.total_seconds()
            seconds_between_price_tweets = -14400
            print(diff_seconds) 
            if int(diff_seconds) < seconds_between_price_tweets: # 4 hours
                print('True')
                return True
            else:
                print(f'False - {seconds_between_price_tweets/3600} hours have'
                      'not elapsed yet between now and the last price tweet')
                return False
        except Exception as general_exception:
            print("An exception occurred")

    def unfollow_people_who_do_not_follow_back(self):
        print(len(self.friends))
        for f in self.friends:
            if f not in self.followers:
                print(f)
                print("Unfollow {0}".format(api.get_user(f).screen_name))
                api.destroy_friendship(f)
                nsecs=randint(5,25)
                sleep(nsecs)
            else:
                continue

    def tweet_articles(self):
        my_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1"
                      "4_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0"
                      ".3578.98 Safari/537.36", 
        "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"}

        article_list = []
        links = []
        hashtags = []
        try:
            # news_result = get(choice(self.google_commodities_news_links))
            # news_result = get(choice(self.google_commodities_news_links), '''headers=my_headers''')
            news_result = get(choice(self.google_commodities_news_links), headers=my_headers)
            c = news_result.content
            soup = BeautifulSoup(c, 'html.parser')
            tweet_article_header = str(soup.item.title.text)
            Client = urlopen(choice(self.google_commodities_news_links))
            xml_page = Client.read()
            Client.close()

            soup_page=soup(xml_page,"xml")
            news_list=soup.select("item")
            random_news_list = choice(news_list)
            # print(f"news_list{news_list}")
            print(f"random {random_news_list}")
            # Print news title, url and publish date
            # for news in news_list:
            title = random_news_list.find('title').text
            print(f"title: {title}")
            links += [random_news_list.link.next_sibling]
            # print(f"links: {links}")
            # break
            self.link = ", ".join(links)
            print(f"self.link {self.link}")
            html = urlopen(self.link) 
            
            # use selenium here to interface with 
            # web page. Captchas and cookies require interaction. 
            # if javascript is used to dynamically generate content, 
            # then there potentially might be issues
            '''.read()
            soup = BeautifulSoup(html)

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = [line for line in text.splitlines()]
            print(f"lines:{lines}")
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            text_lower = text.lower()
            text_lower_split = text_lower.split()
            alphanumeric_words = [word for word in text_lower_split if word.isalpha()]
            result = ' '.join(alphanumeric_words)
            str_result = result

            print(text_lower.encode('utf-8'))

            rake_object = RAKE.Rake(self.stop_dir)
            print(rake_object)
            keywords = rake_object.run(str_result) 
            print("Keywords:", keywords[0:4])'''

            
            api.update_status(f"{title} \nRead more {str(self.link)} \n {self.link} \n {self.tweet_article_hashtags}")
        except Exception as general_exception:
            print("An exception occurred", general_exception)

        "https://stackoverflow.com/questions/60792898/tag-of-google-news-title-for-beautiful-soup"
    
    def run(self):
        d = date.today().weekday() 

        while True:
            self.tweet_text = ""
            self.tweet_text_2 = ""
            self.tweet_text_3 = ""
            print('Hi and welcome to BB_Com demo')
            self.search_and_like()
            sleep((randint(1, 10)))
            self.retweet_from_selected_user_list_method()
            if d in range(5):
                if self.compare_price_tweet_timestamp_to_present():
                    self.prices_scraper_cnbc()
                    self.tweet_prices()
            else:
                print("it's the weekend")
            self.tweet_articles()
            self.follow_people()
            if len(self.friends) > 100:
                self.unfollow_people_who_do_not_follow_back()
            print("This cycle is ending. Time to sleep")
            sleep((randint(1800, 3600)))

class BB_comDemo(): #put in another file?
    def run_demo(self):
        '''main instance
        '''        
    bb_com = BB_Com()
    bb_com.run()

'''D. Testing'''
