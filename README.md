# News App Project

## Overview

This project is a web application designed to fetch and display news stories from the New York Times API, leveraging the power of Python and the Streamlit framework. It offers a dynamic interface for users to interact with, including selecting news categories, customizing word clouds, and viewing the frequency distribution of common words within articles. It's an ideal showcase of integrating APIs, processing JSON data, and visualizing information in a user-friendly web app.

## Features

- **Dynamic News Selection**: Users can choose from a variety of news categories such as arts, business, science, technology, and more.
- **Customizable Word Clouds**: The application generates word clouds based on the top stories of the selected category, with options to customize the maximum number of words, color schemes, and background colors.
- **Frequency Distribution Plot**: A plot displaying the frequency distribution of the most common words in the selected news stories, excluding stopwords and punctuation.
- **Interactive UI**: Built with Streamlit, the app provides an intuitive sidebar for user inputs and a clean layout for displaying results.

## Technologies Used

- **Python 3.9+**: The core programming language.
- **Streamlit**: For creating the web application interface.
- **New York Times API**: To fetch real-time news stories.
- **NLTK**: For natural language processing tasks.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For interactive plots.
- **WordCloud & Matplotlib**: For generating and displaying word clouds.

## Getting Started

### Prerequisites

Ensure you have Python 3.9 or newer installed on your system. You do not need Anaconda for managing packages in this project.

### Installation

1. **Set Up Your Project**: Start by creating a new project in PyCharm and setting up a virtual environment.
2. **Install Dependencies**: Open your terminal and install the required packages using pip:
3. **API Key Configuration**: Obtain an API key from the New York Times website and store it in a `api_key.json` file within the `JSON_Files` directory.

### Running the Application

1. Navigate to your project directory in the terminal.
2. Run the Streamlit application using:
3. The application should now be running on your local server. Follow the URL displayed in your terminal to view it in your browser.

## Project Structure

- `streamlit_app.py`: The main Python script that runs the web application.
- `JSON_Files/api_key.json`: Contains your New York Times API key.
- `main_functions.py`: Helper functions for the application.
- `venv/`: Virtual environment folder (do not modify).

## Contributing

Interested in contributing? We welcome contributions of all forms including new features, bug fixes, and documentation improvements. Please submit a pull request or open an issue to discuss your ideas.

## License

This project is open source and available under the [MIT License](LICENSE).
