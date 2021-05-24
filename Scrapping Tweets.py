# Scraps the most recent 5 tweets tweeted by the user.

import re
import json
import tweepy
consumer_key="Insert_consumer_key_here"
consumer_secret="Insert_consumer_secret"
access_token="Insert_access_token"
access_token_secret="Insert_access_token_secret"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
if (api):
    print("Login Success")
else:
    print("Failed")
 
id_list=[25073877, 939091] #add the id's of twitter pages you want to get here. I used trump's and biden's Twitter handle here.
individual_tweet_list=[]  # the tweets of 1 particular ID or page is stored here and replaced
final_tweet_list=[]
for i in range(len(id_list)):
    new_tweets=[]
    new_tweets = api.user_timeline(id= id_list[i],count=5,tweet_mode='extended') #count tell the number of most recent tweets you want
    for tweet in new_tweets:
        text=str(tweet.full_text)
        text = re.sub(r':', '', text)
        text = re.sub(r'‚Ä¶', '', text)           
        text = re.sub(r'[^\x00-\x7F]+',' ', text)
        print(text) 
        individual_tweet_list.append(text)
    final_tweet_list.append(individual_tweet_list) # This is the final answer. It is a 2D list. First row contains the tweets of first user.  
