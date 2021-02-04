import twitter_utilities as tu
import pandas as pd
import nlp_utilities as nu

# ----- Twitter Authenitcation ----- #
pathToTwitterAuthData = "twitterAccess.txt"
pathToDevKeyAndSecret = "consumer_api_keys.txt"
api = tu.authentication(pathToDevKeyAndSecret, pathToTwitterAuthData)

# ----- Users Retrieval from Tweets in CoAID dataset ----- #
real = True
pathToCoAID = "dataset/CoAID/"
pathToUser = "generated_data/user/"

if real is True:
    output_user_file = "users_real_news.txt"
    news_file = "NewsRealCOVID-19_tweets.csv"
    pathToTimelines = "generated_data/tweet_real/"
else:
    output_user_file = "users_fake_news.txt"
    news_file = "NewsFakeCOVID-19_tweets.csv"
    pathToTimelines = "generated_data/tweet/"

news_df = pd.read_csv(pathToCoAID+news_file)
print("news df shape", news_df.shape)
ids = news_df[['tweet_id']]
# ids = ids[5000:10000]
tu.store_users(api, ids, pathToUser+output_user_file)

# ----- Timelines Retrieval ----- #
users_id = []
fin = open(pathToUser+output_user_file, "r")
for line in fin.readlines():
    users_id.append(line.rstrip("\n"))
since_id = news_df["tweet_id"].min()  # time span matching CoAid
users_id = users_id[:200]
df_range = "_0_200"
tu.store_timelines_as_df(api, users_id, pathToTimelines, since_id)  # , max_id)

# ----- News Sharing URL Detection and Collection ----- #
pathToNewsMatched = "generated_data/news_matched/"
fake_checked = "NewsFakeCOVID-19.csv"
df = pd.read_csv(pathToCoAID+"05-01-2020/"+fake_checked)
df2 = pd.read_csv(pathToCoAID+"07-01-2020/"+fake_checked)
df3 = pd.read_csv(pathToCoAID+"09-01-2020/"+fake_checked)
df4 = pd.read_csv(pathToCoAID+"11-01-2020/"+fake_checked)
frames = [df, df2, df3, df4]
df_fake_news = pd.concat(frames, ignore_index=True)
real_checked = "NewsRealCOVID-19.csv"
dfr = pd.read_csv(pathToCoAID+"05-01-2020/"+real_checked)
dfr2 = pd.read_csv(pathToCoAID+"07-01-2020/"+real_checked)
dfr3 = pd.read_csv(pathToCoAID+"09-01-2020/"+real_checked)
dfr4 = pd.read_csv(pathToCoAID+"11-01-2020/"+real_checked)
framesr = [dfr, dfr2, dfr3, dfr4]
df_real_news = pd.concat(framesr, ignore_index=True)
df_fake_news = df_fake_news.fillna('0').astype('object')
df_real_news = df_real_news.fillna('0').astype('object')
nu.parse_match_count(df_fake_news, df_real_news, users_id,
                     pathToTimelines, pathToNewsMatched,
                     df_range)


'''
df_detected = pd.read_csv("data/df/fake_uit_0.csv")
nu.stance_detection_create_file(
    df_fake_news.fillna('0'), df_detected, fake=True)

'''