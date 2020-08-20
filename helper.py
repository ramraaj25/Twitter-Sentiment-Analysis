
from models.sk_learn_NB.prediction import get_vectorizer, get_sk_model, preprocess
from models.nltk_NB.classify_tweet import classify, extract_words, get_model, get_words
import os
import tweepy
from configurations import consumer_key, consumer_secret, access_token, access_token_secret
from flask import render_template


def extract_tweets(query, no_of_tweets):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweet_list = []
    for tweet in tweepy.Cursor(api.search, q=query, lang='en').items(no_of_tweets):
        tweet_list.append(tweet.text)

    return tweet_list


# For NLTK Classifier


def nltk_predict_from_tweet(tweet):
    tweet_words = extract_words(tweet)
    nltk_model = get_model(os.path.join(
        'models', 'nltk_NB', 'NaiveBayesClassifier.pickle'))
    words = get_words(os.path.join('models', 'nltk_NB', 'words.pickle'))
    result = classify(tweet, words, nltk_model)
    res_dict = {}
    for key in result.samples():
        if key == 'Happy':
            res_dict['Positive'] = f"{result.prob(key) * 100:.2f}%"
        else:
            res_dict['Negative'] = f"{result.prob(key) * 100:.2f}%"
    return res_dict


def nltk_predict_from_api(query, no_of_tweets):
    tweets = extract_tweets(query, no_of_tweets)
    res_dict = {}
    for tweet in tweets:
        tweet_tf = tweet.replace('\n', ' . ')
        res_dict[tweet] = nltk_predict_from_tweet(tweet_tf)

    return res_dict


# For SK-Learn


def sk_predict_from_tweet(tweet):
    model = get_sk_model(os.path.join(
        'models', 'sk_learn_NB', 'mnb_model_large.pickle'))
    cv = get_vectorizer(os.path.join(
        'models', 'sk_learn_NB', 'count_vectorizer.pickle'))
    tweet_tf = preprocess(tweet, cv)
    prediction = model.predict(tweet_tf)
    if prediction[0] == 1:
        return 'Positive'
    else:
        return 'Negative'


def sk_predict_from_api(query, no_of_tweets):
    tweets = extract_tweets(query, no_of_tweets)
    res_dict = {}
    for tweet in tweets:
        tweet_tf = tweet.replace('\n', ' . ')
        res_dict[tweet] = sk_predict_from_tweet(tweet_tf)
    return res_dict


def apology(message):
    return render_template("apology.html", message=message)
