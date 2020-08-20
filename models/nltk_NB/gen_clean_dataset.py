import pandas as pd
import nltk
import pickle
import string

# Reading data
data = pd.read_csv('dataset.csv')
data = data[["mood", "tweet"]]

# Random shuffling of the data
data = data.sample(frac=1).reset_index(drop=True)

# Selecting only the first 50,000 records out of 1.6m
data = data[:50000]


for i in range(len(data['tweet'])):
    # extracting words from the tweets
    tweet_words = nltk.tokenize.word_tokenize(data['tweet'][i])

    # converting every word to lowercase and removing stopwords
    tweet_words = [word.lower() for word in tweet_words if word.isalpha()
                   and word != 'http' and word not in nltk.corpus.stopwords.words('english')]
    data['tweet'][i] = tweet_words
    print(f"Cleaning data...{i + 1}/50000")

# Saving the cleaned dataset
pickle_out_file = open('cleaned_dataset.pickle', 'wb')
pickle.dump(data, pickle_out_file)
pickle_out_file.close()
