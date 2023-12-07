import requests
from bs4 import BeautifulSoup

class GithubScraper:
    def __init__(self):
        self.url = "https://github.com/trending"
        self.soup = None
        self.response = None

    def send_query(self):
        """Send a search query to GitHub trending and store the response."""
        self.response = requests.get(self.url)
        return self.response

    def parse_html(self):
        """Parse the HTML response using BeautifulSoup."""
        soup = BeautifulSoup(self.response.text, 'html.parser')
        self.soup = soup
        return soup

    def extract_topics(self):
        """Extract programming language topics from the parsed HTML."""
        self.parse_html()  # Make sure to call parse_html before extracting topics
        topic_spans = self.soup.find_all('span', {'itemprop': 'programmingLanguage'})
        topics = [topic_span.text.strip() for topic_span in topic_spans]
        return topics


