import tweepy
import config
import pandas as pd

# Function for authentication with Twitter API V2
def authenticate():
    client = tweepy.Client(bearer_token=config.bearer_token)
    return client

# Querying Twitter serach_recent_tweets endpoint
def query_tweeter(query):
    client = authenticate()
    tweets = []
    for response in tweepy.Paginator(client.search_recent_tweets,
                                     query = query,
                                     user_fields = ['username', 'public_metrics', 'description', 'location'],
                                     tweet_fields = ['created_at', 'geo', 'public_metrics', 'text'],
                                     expansions = ['author_id'],
                                     max_results=10):
        tweets.append(response)

    result = []
    user_dict = {}
    # Looping in each response obj
    for response in tweets:
        # Taking all users information of the data we want to keep
        for user in response.includes['users']:
            user_dict[user.id] = {'username': user.username,
                                  'followers': user.public_metrics['followers_count'],
                                  'tweets': user.public_metrics['tweet_count'],
                                  'description': user.description,
                                  'location': user.location
                                  }
        for tweet in response.data:
            user_info = user_dict[tweet.author_id]
            # All the data that is going to be sent to our DB
            result.append({
                           'tweet_id': tweet.id,
                           'text': tweet.text,
                           'created_at': tweet.created_at,
                           'user_id': tweet.author_id,
                           'username': user_info['username'],
                           'user_description': user_info['description'],
                           'user_location': user_info['location'],
                           'user_followers': user_info['followers'],
                           'user_tweets': user_info['tweets'],
                           'retweets': tweet.public_metrics['retweet_count'],
                           'replies': tweet.public_metrics['reply_count'],
                           'quote_count': tweet.public_metrics['quote_count']
                           })
        return result

data = query_tweeter('Cryptofunk0')
dataframe = pd.DataFrame(data)
