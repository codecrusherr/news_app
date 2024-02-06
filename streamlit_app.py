import requests
import streamlit as st
import pandas as pd
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import main_functions
import plotly.express as px

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
