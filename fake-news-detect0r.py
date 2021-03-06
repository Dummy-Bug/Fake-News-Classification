from copyreg import pickle
import streamlit as st
import pandas as pd
import pickle

import numpy as np
import pandas as pd
import numpy as np
from sklearn import linear_model
import joblib
from bs4 import BeautifulSoup
import time
import re
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler


st.title("  ❌ Fake News Detector ❌  ") # adding the Title

st.text("This Web App detects the Fake News, You just have to enter manually ")
st.text("or paste the News Artcile and this app will predict  if the News is ")
st.text("is Fake or not")

from PIL import Image
image = Image.open(r'C:\Users\LAXIT RANA\Desktop\Git\Case Studies\Fake News Classifier\fake_ai.jfif')

st.image(image, width = 550)


# def load_data(nrows):
  
  # data = pd.read_csv(r'C:\Users\LAXIT RANA\Desktop\Git\Case Studies\Fake News Classifier\preprocessed_News_for_app.csv')
  
  # data.drop_duplicates()
  # data = data.dropna(inplace = False).reset_index()
  
  # data.rename(columns = {'text' : "News Articles"},inplace = True)
  
  # return data['News Articles'][:nrows]

# st.text("Select the Check box if you want to view some sample News Text")
# data = load_data(5)

# if st.checkbox("Show Data"):
  
  # st.subheader("Data samples")
  # st.write(data)


st.subheader("Enter The News Text below")
user_input = st.text_area("",height = 150)

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase
  
stopwords= set(['br', 'the', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",\
            "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', \
            'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their',\
            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', \
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', \
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', \
            'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',\
            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',\
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',\
            'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', \
            's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', \
            've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',\
            "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',\
            "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", \
            'won', "won't", 'wouldn', "wouldn't"])

def clean_text(sentence):
  
    sentence = re.sub(r"http\S+", "", sentence)
    sentence = BeautifulSoup(sentence, 'lxml').get_text()
    sentence = decontracted(sentence)
    sentence = re.sub("\S*\d\S*", "", sentence).strip()
    sentence = re.sub('[^A-Za-z]+', ' ', sentence)
    sentence = ' '.join(e.lower() for e in sentence.split() if e.lower() not in stopwords)
    
    return sentence.strip()
  
###################################################

def predict(user_input):# it will run this function and it will return either prediction
    start = time.time()
    clf = joblib.load(r'C:\Users\LAXIT RANA\Desktop\Git\Case Studies\Fake News Classifier\model.pkl')
    vectorizer = joblib.load(r'C:\Users\LAXIT RANA\Desktop\Git\Case Studies\Fake News Classifier\count_vect.pkl')
    standard_scaler = joblib.load(r'C:\Users\LAXIT RANA\Desktop\Git\Case Studies\Fake News Classifier\standard_scaler.pkl')
    
    news_text   = clean_text(user_input) # cleaning the query point 
    vectorized_news_text   = vectorizer.transform([news_text])
    query_point = standard_scaler.transform(vectorized_news_text)
    
    pred        = clf.predict(query_point)
    
    if pred[0]: # if prediction is True means if News == 1 then it is a Fake News.
        st.markdown("<h1><span style='color:red'>❌ This is a fake news 😡</span></h1>", unsafe_allow_html = True)
    
    else: 
        st.markdown("<h1><span style='color:green'>✅ This is a real news 👍</span></h1>",unsafe_allow_html = True)
    end  = time.time()
    print(end-start)
    
if st.button("Submit"):
  predict(user_input)
  
  
