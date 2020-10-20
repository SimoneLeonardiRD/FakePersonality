import micro_influencer_utilities as miu
import tweepy
import time
import pandas as pd


pathToTwitterAuthData = "twitterAccess.txt"
pathToDevKeyAndSecret = "consumer_api_keys.txt"
pathToData = "~/Venv/Documents/dataset/CoAID/"
fn = "NewsFakeCOVID-19_tweets.csv"
# fn = ClaimFakeCOVID-19_tweets.csv
fake_news = pd.read_csv(pathToData+fn)
print(fake_news.shape)
ids = fake_news[['tweet_id']]
# ids = ids[:1000]
print(ids)
api = miu.authentication(pathToDevKeyAndSecret, pathToTwitterAuthData)
counter = 0
total_retweeters = []
for tweetid in ids['tweet_id']:
    try:
        # for page in miu.limit_handled(tweepy.Cursor(api.retweeters, tweetid).pages()):
        #    print(page)
        retweeters_100 = api.retweeters(int(tweetid))
        print(retweeters_100)
        if len(retweeters_100) > 0:
            counter = counter + 1
            for user_id in retweeters_100:
                total_retweeters.append(user_id)
    except tweepy.RateLimitError:
        time.sleep(15*60)
    except tweepy.TweepError as e:
        print(e)
print(str(counter))
fout = open("retweeters.txt", "w")
# fout = open("claim_retweeters.txt", "w")
for user in total_retweeters:
    fout.write(str(user)+"\n")
