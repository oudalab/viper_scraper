import pandas as pd
import numpy as np
import csv
import logging
import nltk
import os
import glob
import argparse
import json
import sys
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from operator import itemgetter

def normalized_relative_term_frequency_generator(data_filtered):
    tokenizer = TweetTokenizer()
    vectorizer = CountVectorizer(tokenizer=tokenizer.tokenize,ngram_range=(1,1))

    # Get count of each term in each document
    count_matrix = vectorizer.fit_transform(data_filtered['text']) #term-document matrix
    feature_names = vectorizer.get_feature_names() # terms, corresponding with columns of t-d matrix

    # Count total words
    total_words = count_matrix.sum()       # np.int64
    # Sum each column (term) to get term counts
    # Note each column corresponds to each term in feature_names
    term_counts = count_matrix.sum(axis=0) # np.matrix shape (1, len(feature_names))

    # Calculate term frequency of each term
    term_frequencies = np.divide(term_counts,total_words)

    # Load baseline frequencies into dictionary for comparison
    baseline_frequencies = {} #name, frequency pairs
    with open('utils/freq_table_72319443_total_words_twitter_corpus.csv','r') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            baseline_frequencies[row[0]] = float(row[2])
    
    # Calculate relative frequencies (tf / tf_baseline)
    relative_frequencies = []
    i = 0
    for tf in np.nditer(term_frequencies):
        if (baseline_frequencies.__contains__(feature_names[i])):
            relative_frequencies.append(tf / baseline_frequencies[feature_names[i]])
        i += 1

    # Get indices which would sort relative frequencies
    indices = np.argsort(relative_frequencies)[::-1]
    
    n = 400 # Number of terms to save

    # Use to grab the top n terms and save to file
    top_features = [feature_names[i] for i in indices[:n]]
    with open('topn.txt', 'w') as f:
        for word in top_features:
            f.write(word + '\n')

# Generate the tracking file with TF-IDF
def tfidf_generator(data_filtered):
    # TODO: Improve generation
        # Right now, just gets top from the inverse document frequency vector
        # Use average TFIDF of terms across documents


    tokenizer = TweetTokenizer()
    # Override the tokenizer of the tfidfvectorizer with one made for tweets
    vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize,ngram_range=(1,3))
    # Get term-document matrix from tweets' text
    tdmat = vectorizer.fit_transform(data_filtered['text'])
    feature_names = vectorizer.get_feature_names()
    weight = vectorizer.idf_
    # Indices which would sort weights
    indices = np.argsort(weight)[::-1]
    n = 400
    # Grab top n features
    top_features = [feature_names[i] for i in indices[:n]]
    with open('topn.txt', 'w') as f:
        for word in top_features:
            f.write(word + '\n')

# TODO: Simple frequency (with stop words) file generation

# Partitioning data and cleaning text before sending to file generation fns
def trending_phrases(csv_filename):
    """
    Get top 400 trending phrases from our data and saves in the topn.txt file
    """
    df = pd.read_csv(csv_filename)

    print(str(len(df.index)) + ' total tweets')

    # Partition data - only want to analyze desirable set
    # m is bools
    m = df['detected_file'].apply(is_above_threshold,args=[csv_filename,.5],)
    
    # Remove URLs (links to images) or else they dominate ranking
    # Remove special chars (less # and @)
    data_filtered = df[m].replace('https?:\/\/.*[\r\n]*|[^0-9a-zA-Z#@]+',' ',regex=True)

    print(str(len(data_filtered.index)) + " contain target")

    normalized_relative_term_frequency_generator(data_filtered)

# Returns true if the object has been detected with some confidence above
# the threshold in the image
def is_above_threshold(detected_filename, csv_filename, threshold):
    file_path = os.path.join(os.path.dirname(csv_filename),detected_filename)
    try:
        with open(file_path,'r') as f:
            detected = json.load(f)
            if len(detected['aeroplane']) is 0:
                return False
            else:
                for c in detected['aeroplane']:
                    if c > threshold:
                        return True
                return False
    except OSError as e:
        print(e)
        return False

# TODO: Actually let choose what we are looking for and confidence threshold
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('csv_file',metavar="CSV File",
                        help="The path to the csv file containing tweets")

    args = parser.parse_args()
    trending_phrases(args.csv_file)