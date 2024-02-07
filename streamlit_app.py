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


# Load API key
def load_api_key():
    api_data = main_functions.read_from_file("JSON_Files/api_key.json")
    return api_data["my_key"]


app_page = st.sidebar.selectbox("Select an API",
                                ["", "Top Stories", "Most Popular Articles"])


# Function to fetch data from the NYT API
def fetch_nyt_data(section):
    api_key = load_api_key()  # Ensure the API key is loaded right where it's needed
    url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return " ".join(article['title'] + ' ' + article['abstract'] for article in response.json()['results'])
    else:
        st.error("Error fetching data from the NYT API")
        return ""


# Function to generate word cloud
def generate_word_cloud(text_wordcloud, max_words, background_color, colormap):
    user_wordcloud = WordCloud(width=800,
                               height=800,
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
            max_words_wordcloud = st.slider("Max words in WordCloud", 1, 200, 100)
            colormap_wordcloud = st.selectbox("Colormap",
                                              ["prism", "viridis", "plasma", "magma", "cividis", "cool", "spring",
                                               "autumn", "summer", "winter"])
            background_color_wordcloud = st.color_picker("Background Color", "#000000")

        with col2:
            generate_word_cloud(text_for_wordcloud, max_words_wordcloud, background_color_wordcloud, colormap_wordcloud)

        # Frequency Distribution Plot
        st.subheader("II - Frequency Distribution")
        if st.checkbox("Click here to display the frequency distribution plot"):
            if text_for_wordcloud:
                num_words = st.slider("How many words do you want to see in the plot?", 1, 20, 10)

                words = word_tokenize(text_for_wordcloud.lower())

                no_punkt = []
                for w in words:
                    if w.isalpha():
                        no_punkt.append(w)

                # Load list of stopwords
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
    st.subheader("The Most Popular Articles")
    st.subheader("I - Comparing Most Shared, Viewed and Emailed Articles")
    # User inputs for article type and period
    article_type = st.selectbox("Select the type of articles",
                                ["", "emailed", "shared", "viewed"])
    period = st.selectbox("Select the period",
                          ["", "1", "7", "30"])

    # Fetch data from the NYT Most Popular Articles API
    if article_type and period:
        article_api_key = load_api_key()
        api_url = f"https://api.nytimes.com/svc/mostpopular/v2/{article_type}/{period}.json?api-key={article_api_key}"
        response = requests.get(api_url)

        if response.status_code == 200:
            articles_data = response.json()['results']
            text_for_wordcloud = " ".join(
                article['title'] + ' ' + (article.get('abstract', '') or '') for article in articles_data)

            # Configuration and generation of word cloud
            col1, col2 = st.columns(2)
            with col1:
                max_words_wordcloud = st.slider("Max words in WordCloud", 1, 200, 100)
                colormap_wordcloud = st.selectbox("Colormap",
                                                  ["prism", "viridis", "plasma", "magma", "cividis", "cool", "spring",
                                                   "autumn", "summer", "winter"],
                                                  key='mp_colormap')
                background_color_wordcloud = st.color_picker("Background Color", "#000000")

            with col2:
                # Generate and display the word cloud for Most Popular Articles
                generate_word_cloud(text_for_wordcloud, max_words_wordcloud, background_color_wordcloud,
                                    colormap_wordcloud)

            # Frequency Distribution Plot
            st.subheader("II - Frequency Distribution")
            if st.checkbox("Click here to display the frequency distribution plot"):
                if text_for_wordcloud:
                    num_words = st.slider("How many words do you want to see in the plot?", 1, 20, 10)

                    words = word_tokenize(text_for_wordcloud.lower())

                    no_punkt = []
                    for w in words:
                        if w.isalpha():
                            no_punkt.append(w)

                    # Load list of stopwords
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

