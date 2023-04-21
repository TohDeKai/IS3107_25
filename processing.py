import string
import json

def tokenize(sentence):
    # split sentence into words and remove punctuation
    words = sentence.translate(str.maketrans('', '', string.punctuation)).split()

    #Returns list of tokenized words
    return words

def remove_stopwords(words):
    # remove stopwords from the list of words
    stop_words = ["didn't", 'off', 'were', 'been', 'isn', 'then', 'which', 'in', 'wouldn', 'below', 'had', 'own', 'couldn', "wouldn't", 'both', 'each', 'an', "should've", 'a', 'himself', "mustn't", 'has', 'and', 'ourselves', 'very', 'have', 'that', 'don', 'themselves', 'on', 'at', 'until', 'its', 'him', 'does', 'for', "haven't", "needn't", 'me', 'myself', 'than', 'after', 'or', 'didn', 'so', 'why', 'when', 'mustn', 'this', "aren't", 'more', "weren't", "hadn't", "hasn't", 'they', 'your', 'do', 'weren', 'we', 'am', 'those', 'once', 'doesn', 'she', 'such', 'his', 'will', 'few', 'hers', 'between', 'ours', 'did', 'other', 'mightn', "won't", 're', 'these', "you're", 'hasn', 'while', 'further', 'being', 'aren', "couldn't", 'too', 'now', 'having', 'against', 'with', "don't", 'wasn', 'be', 'through', 'our', 'doing', 'the', 'same', "it's", 'because', 'under', 'my', "you've", 'is', 'm', 'over', 'if', 't', 'as', 'during', 'it', 'before', 'there', 'their', 'yours', 'but', 'how', 'by', 'what', 'yourself', 'o', "you'll", "she's", "shouldn't", 'are', "doesn't", 'was', 'hadn', 'where', 'i', 'into', "you'd", 'most', 'any', 'needn', 'not', 'who', "isn't", 'y', 'whom', 'again', 'you', 'down', 've', 'to', 'd', 'some', 'them', "that'll", 'ain', 'from', 'haven', 'of', 'herself', 'ma', 's', 'here', 'up', 'should', 'can', 'just', 'shouldn', 'he', 'theirs', 'about', 'her', 'above', 'all', 'nor', 'itself', "mightn't", "wasn't", 'only', 'no', 'll', "shan't", 'shan', 'won', 'yourselves', 'out']
    filtered_words = [word for word in words if word.lower() not in stop_words]

    #return list of filtered words
    return filtered_words

def filter_title(file_path):
    with open(file_path) as f:
        data = json.load(f)

    dict = {}

    for article in data:
        title = article['title']
        print(title)
        title = tokenize(title)
        for i in title:
          if i in dict:
              dict[i] += 1
          else:
              dict[i] = 1

    return dict


        
