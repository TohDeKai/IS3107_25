import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.util import mark_negation
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import nltk

# Removing non aplhanum characters, stripping whitespace and converting all characters to lowercase
def simple_headline_cleaning(title):
    pattern = "[^0-9a-zA-Z ]"
    alphanum_headline = re.sub(pattern, '', title)
    return alphanum_headline.strip().lower()

# Helper function for tokenization, POS tagging and lemmatization
lemmatizer = WordNetLemmatizer()

def lemmatize(pos_tagging_pair):
  word, tag = pos_tagging_pair
  try:
    return lemmatizer.lemmatize(word, pos=tag[0].lower())
  except KeyError:
    return word

def tokenization_tagging(headline):
  tokenized = word_tokenize(headline)
  pos_tagged = nltk.pos_tag(tokenized)
  lemmatized = [lemmatize(word) for word in pos_tagged]
  return ' '.join(lemmatized)

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    tokens = nltk.word_tokenize(text)
    marked_tokens = mark_negation(tokens)
    scores = sid.polarity_scores(' '.join(marked_tokens))
    if scores['compound'] > 0:
        return("Positive sentiment")
    elif scores['compound'] < 0:
        return("Negative sentiment")
    else:
        return("Neutral sentiment")

# Helper function for stopword removal
def stopwords_removal(headline):
    STOP_WORDS_ENG = stopwords.words('english')
    tokenized = word_tokenize(headline)
    stopwords_removed = [word for word in tokenized if word.lower() not in STOP_WORDS_ENG]
    return ' '.join(stopwords_removed)

# Testing on exported data
import json

def test_with_export(file_path):
    with open(file_path) as f:
        data = json.load(f)

    for article in data:
        title = article['title']
        print(title)
        title = simple_headline_cleaning(title)
        print("tokenization_tagging: " + tokenization_tagging(title))
        print("stopwords_removal: " + stopwords_removal(title))

"""
test_with_export("data_collection/exports/krasia.json")
test_with_export("data_collection/exports/cna.json")
test_with_export("data_collection/exports/today.json")
"""