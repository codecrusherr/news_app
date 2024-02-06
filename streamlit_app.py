import nltk
import requests
import streamlit as st
import pandas as pd
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import main_functions
import plotly.express as px
from wordcloud import WordCloud

# Set up your Streamlit page
st.set_page_config(
    page_title="Project 1",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/library/api-reference',
        'Report a bug': "https://docs.streamlit.io/library/api-reference",
        'About': "# This is Project 1 for COP 4813 - Prof. Gregory Reis"
    }
)

stop_words = set(stopwords.words("english"))
st.title("Project 1 - News App")


# Load API key
def load_api_key():
    with open("JSON_Files/api_key.json") as file:
        return json.load(file)["my_key"]


api_key = load_api_key()

app_page = st.sidebar.selectbox("Select an API",
                                ["Top Stories", "Most Popular Articles"])


# Function to fetch data from the NYT API
def fetch_nyt_data(topic):
    url = f"https://api.nytimes.com/svc/topstories/v2/{topic}.json?api-key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles_data = response.json()['results']
        text_data = " ".join([article['title'] + ' ' + article['abstract'] for article in articles_data])
        return text_data
    else:
        st.error("Error fetching data from the NYT API")
        return ""


# Function to generate word cloud
def generate_word_cloud(text_wordcloud, max_words, background_color, colormap):
    user_wordcloud = WordCloud(width=800,
                               height=400,
                               stopwords=stop_words,
                               max_words=max_words,
                               background_color=background_color,
                               colormap=colormap).generate(text_wordcloud)
    fig, ax = plt.subplots()
    plt.imshow(user_wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)


# Part A: Top Stories API
if app_page == "Top Stories":
    st.subheader("The Stories API")
    st.subheader("I - WordCloud")

    topic_wordcloud = st.selectbox("Select Topic",
                                   ["", "arts", "automobiles", "books", "business", "fashion", "food", "health",
                                    "home",
                                    "insider",
                                    "magazine",
                                    "movies", "nyregion", "opinion", "politics", "realestate", "science", "sports",
                                    "sundayreview", "technology", "theater", "t-magazine", "travel", "upshot", "us",
                                    "world"])

    if topic_wordcloud:
        text_for_wordcloud = fetch_nyt_data(topic_wordcloud)

        col1, col2 = st.columns(2)

        with col1:
            max_words_wordcloud = st.slider("Max words in WordCloud", 1, 200, 50)
            colormap_wordcloud = st.selectbox("Colormap",
                                              ["prism", "viridis", "plasma", "magma", "cividis", "cool", "spring", ])
            background_color_wordcloud = st.color_picker("Background Color", "#FFFFFF")

        with col2:
            generate_word_cloud(text_for_wordcloud, max_words_wordcloud, background_color_wordcloud, colormap_wordcloud)

st.subheader("II - Frequency Distribution")
frequency_plot = st.checkbox("Click here to display the frequency distribution plot")
