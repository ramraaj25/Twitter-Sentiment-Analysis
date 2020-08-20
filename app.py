from flask import Flask, render_template, request
from helper import nltk_predict_from_tweet, nltk_predict_from_api, sk_predict_from_tweet, sk_predict_from_api, apology
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nltk', methods=["GET", "POST"])
def nltk():
    if request.method == 'GET':
        return render_template('lib.html', acc=71.5, model='nltk')

    elif request.method == 'POST':
        if request.form.get('from-tweet'):
            tweet = request.form.get('tweet')
            if tweet == '':
                return apology("Must provide a tweet")
            prediction = nltk_predict_from_tweet(tweet)
            return render_template('prediction.html', prediction=prediction, tweet=tweet, model='nltk')
        elif request.form.get('from-twitter'):
            query = request.form.get('query')
            if query == '':
                return apology("Must provide query")

            no_of_tweets = request.form.get('no-of-tweets')
            if not no_of_tweets.isdigit():
                return apology("Must provide valid number of tweets")
            no_of_tweets = int(no_of_tweets)
            prediction = nltk_predict_from_api(query, no_of_tweets)
            return render_template('prediction_api.html', model='nltk', predicted_tweets=prediction)


@app.route('/sk-learn', methods=['GET', 'POST'])
def sk_learn():
    if request.method == 'GET':
        return render_template('lib.html', acc=75.5, model='sk-learn')
    elif request.method == 'POST':
        if request.form.get('from-tweet'):
            tweet = request.form.get('tweet')
            if tweet == '':
                return apology("Must provide a tweet")
            prediction = sk_predict_from_tweet(tweet)
            return render_template('prediction.html', prediction=prediction, tweet=tweet, model='sk')
        elif request.form.get('from-twitter'):
            query = request.form.get('query')
            no_of_tweets = request.form.get('no-of-tweets')
            if query == '':
                return apology("Must provide query")

            no_of_tweets = request.form.get('no-of-tweets')
            if not no_of_tweets.isdigit():
                return apology("Must provide valid number of tweets")
            no_of_tweets = int(no_of_tweets)

            prediction = sk_predict_from_api(query, no_of_tweets)
            return render_template('prediction_api.html', model='sk', predicted_tweets=prediction)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    print(e.name)
    return apology(e.name)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
