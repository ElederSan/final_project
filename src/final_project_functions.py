# importing libraries

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import regex as re
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('tagsets')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from sklearn.naive_bayes import CategoricalNB
from sklearn.model_selection import train_test_split
import random


porter = PorterStemmer()
snowball = SnowballStemmer(language='english')
lemmatizer = WordNetLemmatizer()



from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
import nltk
nltk.download('words')
from nltk.corpus import stopwords
from stop_words import get_stop_words
from bs4 import BeautifulSoup

def clean_up(s):
    """
    Cleans up numbers, URLs, and special characters from a string.

    Args:
        s: The string to be cleaned up.

    Returns:
        A string that has been cleaned up.
    """
    import regex as re
    s = s.lower()
    s = re.sub(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', ' ', s)
    s= re.sub(r'\d+',' ',s) # Replace one or more digits by  ' '
    s = re.sub(r'\W+',' ',s) # Replace everything non-alpahnumeric by ' '
    s = BeautifulSoup(s, 'lxml').get_text().strip()

    return s


def tokenize(s):
    """
    Tokenize a string.

    Args:
        s: String to be tokenized.

    Returns:
        A list of words as the result of tokenization.
    """
    s = word_tokenize(s)

    return s

def stem_and_lemmatize(l):
    """
    Perform stemming and lemmatization on a list of words.

    Args:
        l: A list of strings.

    Returns:
        A list of strings after being stemmed and lemmatized.
    """
    snow_stemmer = SnowballStemmer(language='english')

    stemmed_list = [snow_stemmer.stem(word) if snow_stemmer.stem(word) in words.words() else word for word in l]

    lem = WordNetLemmatizer()

    stem_lemm_list=[lem.lemmatize(word) for word in stemmed_list]

    return stem_lemm_list

def remove_stopwords(l):
    """
    Remove English stopwords from a list of strings.

    Args:
        l: A list of strings.

    Returns:
        A list of strings after stop words are removed.
    """
    stop_words = set(stopwords.words("english"))
    list_wo_stop = [word for word in l if word.lower() not in stop_words]
    return list_wo_stop

    #stop_words = get_stop_words('en')

    # Clean stop words
    #stop_words_clean = [re.sub(r"\s*'\s*\w*", "", word) for word in stop_words]

    #list_wo_stop = [word for word in l if word not in stop_words_clean]

    #return list_wo_stop