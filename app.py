import requests
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt

from collections import Counter


def send_query():

    url = "https://github.com/trending"
    response = requests.get(url)
    return response


def parse_html(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def extract_topics(soup):
    topic_spans = soup.find_all('span', {'itemprop': 'programmingLanguage'})

    topics = []
    for topic_span in topic_spans:
        topic = topic_span.text.strip()
        topics.append(topic)

    return topics


def main():
    response = send_query()

    if response.status_code == 200:
        soup = parse_html(response)
        topic_list = extract_topics(soup)

        print(topic_list)

        # Count the occurrences of each programming language
        language_counts = Counter(topic_list)

        # Extract languages and their counts for plotting
        languages = list(language_counts.keys())
        counts = list(language_counts.values())

        # Plotting the bar chart
        plt.bar(languages, counts, color='skyblue')
        plt.xlabel('Programming Languages')
        plt.ylabel('Number of Occurrences')
        plt.title('Programming Language Distribution')
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Show the plot
        plt.show()

    else:
        print(
            f"Failed to retrieve search results. Status code: {response.status_code}")
