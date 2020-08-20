import tweepy
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
import pickle
'''
consumer_key = 'oWvdVLmtfJ80H5NWlUdkibjgH'
consumer_secret = '76e2m11yhXSmqvCfFYotXBZishMryxsTgHTYdcMHUHbrUmdABa'

access_token = '3076194458-V1WEq9B6ncg0driSnMF5zvFWIKuVDLLIXMSE556'
access_token_secret = 'PgMGGNubX2MtGnfWEUNxeEBfNc3VoVMAU9hTqbaDgOfaR'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search, q='#BoycottAirAsia', lang='en').items(10):
    print(tweet.text)
'''


def get_vectorizer(filename):
    pickle_cv = open(filename, 'rb')
    cv = pickle.load(pickle_cv)
    pickle_cv.close()
    return cv


def get_sk_model(filename):
    pickle_model = open(filename, 'rb')
    model = pickle.load(pickle_model)
    pickle_model.close()
    return model


def preprocess(tweet, cv):
    tokenizer = RegexpTokenizer(r'[A-Za-z]+')
    tweet_words = tokenizer.tokenize(tweet)
    stemmer = SnowballStemmer('english')
    tweet_words = [stemmer.stem(word) for word in tweet_words]
    tweet_words = ' '.join(tweet_words)
    tweet_words_transformed = cv.transform([tweet_words])
    return tweet_words_transformed
