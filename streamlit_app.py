import requests
import nltk
import streamlit as st
import pandas as pd
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import main_functions
import plotly.express as px
from wordcloud import WordCloud

nltk.download('punkt')

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

# Load API key directly at the beginning
api_key = main_functions.read_from_file("JSON_Files/api_key.json")["my_key"]

app_page = st.sidebar.selectbox("Select an API", ["", "Top Stories", "Most Popular Articles"])

# Part A: Top Stories API - Fetching and Processing Directly
if app_page == "Top Stories":
    st.header("The Stories API")
    st.subheader("I - WordCloud")

    topic_wordcloud = st.selectbox("Select a topic of your interest", ["", "arts", "automobiles", "books", "business",
                                                                       "fashion", "food", "health", "home", "insider",
                                                                       "magazine", "movies", "nyregion", "opinion",
                                                                       "politics", "realestate", "science", "sports",
                                                                       "sundayreview", "technology", "theater",
                                                                       "t-magazine", "travel",
                                                                       "upshot", "us", "world"])

    if topic_wordcloud:
        url = f"https://api.nytimes.com/svc/topstories/v2/{topic_wordcloud}.json?api-key={api_key}"
        response = requests.get(url)

        text_for_wordcloud = ""
        if response.status_code == 200:
            articles_data = response.json()['results']
            # This will process each article's title and abstract
            for article in articles_data:
                title = article['title']
                abstract = article.get('abstract', '')
                # Concatenate title and abstract with a space for separation
                text_for_wordcloud += title + ' ' + abstract + " "
        else:
            st.error("Failed to fetch data from the NYT API.")

        # Check if text_for_wordcloud is not empty
        if text_for_wordcloud:
            col1, col2 = st.columns(2)

            with col1:
                max_words_wordcloud = st.slider("Choose a maximum number of words to be displayed", 1, 200, 100)
                colormap_wordcloud = st.selectbox("Choose a colormap",
                                                  ["prism", "viridis", "plasma", "magma", "cividis",
                                                   "cool", "spring", "autumn", "summer", "winter"])
                background_color_wordcloud = st.color_picker("Choose a background color", "#000000")

            with col2:
                # Generate word cloud directly here
                user_wordcloud = WordCloud(width=800, height=800, stopwords=stop_words, max_words=max_words_wordcloud,
                                           background_color=background_color_wordcloud,
                                           colormap=colormap_wordcloud).generate(text_for_wordcloud)
                fig, ax = plt.subplots()
                plt.imshow(user_wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(fig)

        # Frequency Distribution Plot
        st.subheader("II - Frequency Distribution")
        if st.checkbox("Click here to display the frequency distribution plot"):
            if text_for_wordcloud:
                num_words = st.slider("Choose the number of words", 1, 20, 10)

                words = word_tokenize(text_for_wordcloud.lower())

                no_punkt = []
                for w in words:
                    if w.isalpha():
                        no_punkt.append(w)

                stopwordsEnglish = stopwords.words("english")

                filtered_list = []
                for w in no_punkt:
                    if w not in stopwordsEnglish:
                        filtered_list.append(w)

                freq_dist = FreqDist(filtered_list)
                # Fetch the most common words up to the number specified by the user
                most_common_words = freq_dist.most_common(num_words)

                df_freq_dist = pd.DataFrame(most_common_words, columns=['words', 'count'])
                freq_fig = px.bar(df_freq_dist, x='words', y='count', color="count")
                freq_fig.update_layout(yaxis_title="sum of count")
                st.plotly_chart(freq_fig)

# Part B: Most Popular Articles API
if app_page == "Most Popular Articles":
    st.header("The Most Popular Articles")
    st.subheader("I - Comparing Most Shared, Viewed and Emailed Articles")

    article_type = st.selectbox("Select your preferred set of articles",
                                ["", "emailed", "shared", "viewed"])
    period = st.selectbox("Select the age of your articles in days",
                          ["", "1", "7", "30"])

    # Fetch data from the NYT Most Popular Articles API
    if article_type and period:
        api_url = f"https://api.nytimes.com/svc/mostpopular/v2/{article_type}/{period}.json?api-key={api_key}"
        response = requests.get(api_url)

        if response.status_code == 200:
            articles_data = response.json()['results']
            text_for_wordcloud = ""

            for article in articles_data:
                title = article['title']
                abstract = article.get('abstract', '')
                text_for_wordcloud += title + ' ' + abstract + " "

            # Configuration and generation of word cloud
            col1, col2 = st.columns(2)
            with col1:
                max_words_wordcloud = st.slider("Choose a maximum number of words to be displayed", 1, 200, 100)
                colormap_wordcloud = st.selectbox("Choose a colormap",
                                                  ["prism", "viridis", "plasma", "magma", "cividis", "cool", "spring",
                                                   "autumn", "summer", "winter"],
                                                  key='mp_colormap')
                background_color_wordcloud = st.color_picker("Choose a background color", "#000000")

            with col2:
                user_wordcloud = WordCloud(width=800, height=800, stopwords=stop_words, max_words=max_words_wordcloud,
                                           background_color=background_color_wordcloud,
                                           colormap=colormap_wordcloud).generate(text_for_wordcloud)
                fig, ax = plt.subplots()
                plt.imshow(user_wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(fig)

            # Frequency Distribution Plot
            st.subheader("II - Frequency Distribution")
            if st.checkbox("Click here to display the frequency distribution plot"):
                if text_for_wordcloud:
                    num_words = st.slider("Choose the number of words", 1, 20, 10)

                    words = word_tokenize(text_for_wordcloud.lower())

                    no_punkt = []
                    for w in words:
                        if w.isalpha():
                            no_punkt.append(w)

                    stopwordsEnglish = stopwords.words("english")

                    filtered_list = []
                    for w in no_punkt:
                        if w not in stopwordsEnglish:
                            filtered_list.append(w)

                    freq_dist = FreqDist(filtered_list)
                    # Fetch the most common words up to the number specified by the user
                    most_common_words = freq_dist.most_common(num_words)

                    df_freq_dist = pd.DataFrame(most_common_words, columns=['words', 'count'])
                    freq_fig = px.bar(df_freq_dist, x='words', y='count', color="count")
                    freq_fig.update_layout(yaxis_title="sum of count")
                    st.plotly_chart(freq_fig)

        else:
            st.error("Error fetching data from the NYT Most Popular Articles API")
