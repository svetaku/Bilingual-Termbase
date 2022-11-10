#!/usr/bin/env python
# coding: utf-8

# In[19]:

import pandas as pd
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import WordPunctTokenizer
word_punctuation_tokenizer = nltk.WordPunctTokenizer()
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
nlp.max_length = 2100000
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

def load_separate_corpora_from_csv(path, source_lang, target_lang):
    '''
    This function loads our parallel corpus as .csv, cleans it from duplicate, 
    test, empty and untranslated strings,
    and returns source and target strings as separate lists
    path = path (current path as default)
    source_lang = name of the column with the source language
    target_lang = name of the column with the target language
    '''
    df = pd.read_csv(path, sep=';', low_memory=False)
    df = df[[source_lang, target_lang]]
    df = df.dropna()
    df = df.loc[~(df[source_lang].str.contains("тест") | df[source_lang].str.contains("test"))]
    df = df.drop_duplicates()
    df = df.loc[df[source_lang] != df[target_lang]]
    df = df.loc[df[source_lang].str.strip() != ""]
    source_list = df[source_lang].tolist()
    target_list = df[target_lang].tolist()
    
    return source_list, target_list

class Preprocess(object):
    '''String that needs to be preprocessed'''
    
    
    def __init__(self,text):
        self.text = text
        
    def preprocess_en_text(self, exceptions):
        '''
        This function preprocesses EN corpus by cleaning it from extra symbols, lowercasing it,
        then lemmatizing every word and removing stopwords, returning the corpus as a list of clean sentences.
        Takes a list of exceptions as an argument
        '''
        item = self.text
        item = re.sub(r"\d+%", " ", item)         # percetages
        item = re.sub(r"x\d+", " ", item)         # 'x2' etc.
        item = re.sub(r"\d+", " ", item)          # standalone digits
        item = re.sub(r"\n", " ", item)           # line breaks
        item = re.sub(r"\[.+\]", " ", item)       # [...]
        item = re.sub(r"\\+.+;", " ", item)       # color tags '\...;'
        item = re.sub(r"http.+", " ", item)       # links
        item = re.sub(r"\{.*\}", " ", item)       # {...}
        item = re.sub(r" [xX] ", " ", item)       # ' x ', ' X '
        item = re.sub(r"%[sd]", " ", item)        # tags %d, %s
        item = re.sub(r"<.+>", " ", item)         # <...>
        item = re.sub(r"[\U00010000-\U0010ffff]", " ", item)              # emoji
        item = re.sub(r"[!@#$%\^\&\*()_=+\?\!:;\",\.\\»«—-]", " ", item)  # punctuation
        item = re.sub(r"\s+", " ", item)          # several consecutive whitespaces
        item = item.strip(' ')
        item = item.lower()

        tokens = item.split()
        tokens = [nlp(word)[0].lemma_ if word not in exceptions else word for word in tokens]
        tokens = [word for word in tokens if word not in stopwords.words('english')]
        preprocessed_text = ' '.join(tokens)

        return preprocessed_text

    def preprocess_ru_text(self, russian_stopwords):
        '''
        This function preprocesses RU corpus by cleaning it from extra symbols, lowercasing it,
        then lemmatizing every word and removing stopwords, returning the corpus as a list of clean sentences.
        Takes a list of exceptions as an argument
        '''

        item = self.text
        item = re.sub(r"\d+%", " ", item)
        item = re.sub(r"x\d+", " ", item)
        item = re.sub(r"\d+", " ", item)
        item = re.sub(r"\n", " ", item)
        item = re.sub(r"\[.+\]", " ", item)
        item = re.sub(r"\\.+\\;", " ", item)
        item = re.sub(r"http.+", " ", item)
        item = re.sub(r"\{.*\}", " ", item)
        item = re.sub(r" [xX] ", " ", item)
        item = re.sub(r"%[sd]", " ", item)
        item = re.sub(r"<.+>", " ", item)
        item = re.sub(r"[\U00010000-\U0010ffff]", " ", item)
        item = re.sub(r"[!@#$%\^\&\*()_=+\?\!:;\",\.\\»«—-№]", " ", item)
        item = re.sub(r"\s+", " ", item)
        item = item.strip(' ')
        item = item.lower()

        tokens = item.split()
        tokens = [morph.parse(word)[0].normal_form for word in tokens]
        tokens = [word for word in tokens if word not in russian_stopwords]
        preprocessed_text = ' '.join(tokens)

        return preprocessed_text

    def preprocess_no_lemmatization(self, exceptions):
        '''
        This function preprocesses the corpus by cleaning it from extra symbols, lowercasing it,
        removing stopwords, returning the corpus as a list of clean sentences.
        Takes a list of exceptions as an argument
        '''
        item = self.text
        item = re.sub(r"\d+%", " ", item)         # percetages
        item = re.sub(r"x\d+", " ", item)         # 'x2' etc.
        item = re.sub(r"\d+", " ", item)          # standalone digits
        item = re.sub(r"\n", " ", item)           # line breaks
        item = re.sub(r"\[.+\]", " ", item)       # [...]
        item = re.sub(r"\\+.+;", " ", item)       # color tags '\...;'
        item = re.sub(r"http.+", " ", item)       # links
        item = re.sub(r"\{.*\}", " ", item)       # {...}
        item = re.sub(r" [xX] ", " ", item)       # ' x ', ' X '
        item = re.sub(r"%[sd]", " ", item)        # tags %d, %s
        item = re.sub(r"<.+>", " ", item)         # <...>
        item = re.sub(r"[\U00010000-\U0010ffff]", " ", item)              # emoji
        item = re.sub(r"[!@#$%\^\&\*()_=+\?\!:;\",\.\\»«—-]", " ", item)  # punctuation
        item = re.sub(r"\s+", " ", item)          # several consecutive whitespaces
        item = item.strip(' ')
        item = item.lower()

        tokens = item.split()
        tokens = [word for word in tokens if word not in stopwords.words('english')]
        preprocessed_text = ' '.join(tokens)

        return preprocessed_text

