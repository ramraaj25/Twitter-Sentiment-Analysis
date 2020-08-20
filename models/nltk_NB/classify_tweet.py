
import pickle
import nltk
import string


def classify(tweet, words, classifier):

    for word in tweet:
        features = {
            w: (w in tweet) for w in words
        }
        return classifier.prob_classify(features)


def extract_words(tweet):
    tweet_words = nltk.tokenize.word_tokenize(tweet)
    tweet_words = [word.lower() for word in tweet_words if word.isalpha()
                   and word != 'http' and word not in nltk.corpus.stopwords.words('english')]

    return tweet_words


# importing our model
def get_model(filename):
    pickle_in = open(filename, 'rb')
    classifier = pickle.load(pickle_in)
    pickle_in.close()
    return classifier

# importing words


def get_words(filename):
    pickle_i = open(filename, 'rb')
    words = pickle.load(pickle_i)
    pickle_i.close()
    return words


if __name__ == "__main__":

    classifier = get_model()
    words = get_words()

    # input tweet
    tweet = input("Enter text: ")
    tweet = extract_words(tweet)
    result = classify(tweet, words, classifier)

    # print result
    for key in result.samples():
        print(f"{key}: {result.prob(key):.4f}")
