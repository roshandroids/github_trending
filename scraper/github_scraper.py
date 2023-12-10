import requests
from bs4 import BeautifulSoup

from models.repository_model import RepositoryModel


class GithubScraper:
    def __init__(self):
        self.url = "https://github.com/trending"
        self.soup = None
        self.response = None

    def fetch_data(self, duration=None):
        """Send a search query to GitHub trending and store the response."""
        try:
            if not duration:
                url = self.url
            else:
                if duration.lower() == 'daily':
                    url = f"{self.url}?since=daily"
                elif duration.lower() == 'weekly':
                    url = f"{self.url}?since=weekly"
                elif duration.lower() == 'monthly':
                    url = f"{self.url}?since=monthly"
                else:
                    print(f"Invalid duration: {duration}")
                    return None

            self.response = requests.get(url)
            self.response.raise_for_status()  # Check for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data: {e}")
            return None

        return self.response

    def parse_html(self):
        """Parse the HTML response using BeautifulSoup."""
        if not self.response:
            print("No response to parse. Fetch data first.")
            return None

        soup = BeautifulSoup(self.response.text, 'html.parser')
        self.soup = soup
        return soup

    def extract_repositories(self):
        self.parse_html()
        repo_elements = self.soup.select('article.Box-row')
        repositories = [RepositoryModel.from_html(repo) for repo in repo_elements]
        print(repositories)
        return repositories
