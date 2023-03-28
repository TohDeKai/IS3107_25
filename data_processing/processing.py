import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
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

# Helper function for stopword removal
def stopwords_removal(headline):
    STOP_WORDS_ENG = stopwords.words('english')
    tokenized = word_tokenize(headline)
    stopwords_removed = [word for word in tokenized if word.lower() not in STOP_WORDS_ENG]
    return ' '.join(stopwords_removed)

# Testing on exported data