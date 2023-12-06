import requests
from bs4 import BeautifulSoup


def send_query():
    """Send a search query to GitHub trending and return the response."""
    url = "https://github.com/trending"
    response = requests.get(url)
    return response


def parse_html(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def extract_topics(soup):
    topic_spans = soup.find_all('span', {'itemprop': 'programmingLanguage'})
    topics = [topic_span.text.strip() for topic_span in topic_spans]
    return topics
