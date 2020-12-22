import twitter_credencials
import tweepy
import re
from textblob import TextBlob 

auth=tweepy.OAuthHandler(twitter_credencials.consumer_key,twitter_credencials.consumer_key_secret)
auth.set_access_token(twitter_credencials.access_token,twitter_credencials.access_token_secret)
api=tweepy.API(auth)

#function to check the login status
class check_login:
    def login_status(self):
        try:
            api.verify_credentials()
            print("authetication ok")
        except:
            print("error!!")

#simple class to get username and description of any public account
class spy:
    def __init__(self,username=None):
        self.username=username
    def get_details(self):
        try:
           
            user=api.get_user(self.username)
            print("user details are:")
            print(user.name)
            print(user.description)
            print("success")
        except:
            print("error")

"""
###this update function is not working most probably because i have got the access to read only api from twitter
def update(status):
    try:
            
        api.update_profile(description=status)
        print("success")
    except:
        print("error")
"""
#simple class to get the tweets on interested topics
class get_tweets:
    def recent_tweet(self,topic,language,number):
            for tweet in api.search(q=topic,lang=language,rpp=number):
                print(f"{tweet.user.name}:{tweet.text}")
                print("-"*30)

class sentiment_analysis():
    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_tweet_sentiment(self,tweet):
        analysis=TextBlob(self.clean_tweet(tweet))
        if(analysis.sentiment.polarity>0):
            return 'positive'
        elif(analysis.sentiment.polarity<0):
            return 'negetive'
        else:
            return 'neutral'

    def analysis(self,topic,language,number):
        tweets=[]
        try:
            fetched_tweets=api.search(q=topic,lang=language,rpp=number)
            parsed_tweet={}
            for tweet in fetched_tweets:
                parsed_tweet['text']=tweet.text
                parsed_tweet['sentiment']=self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count>0:
                    if(parsed_tweet not in tweets):
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except:
            print("error")


    
#there you go the main function
if __name__ == "__main__":
    analyzer=sentiment_analysis()
    tweets=[]
    ptweet=[]
    ntweet=[]
    netweet=[]
    tweets=analyzer.analysis("rebulic tv","en",200)
    for tweet in tweets:
        if(tweet['sentiment']=='positive'):
            ptweet.append(tweet)
        elif(tweet['sentiment']=='negetive'):
            ntweet.append(tweet)
        else:
            netweet.append(tweet)
    # print(f"the number of positive tweets are {(len(ptweet)*100)/len(tweets)} ")
    print("positive tweets are")
    for twee in ptweet:
        print(twee['text'])

    print("negetive tweets are")
    for twee in ntweet:
        print(twee['text'])




    
