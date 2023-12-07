# web/app.py
import sys
import os
from flask import Flask, render_template
import matplotlib
from collections import Counter
from scraper.github_scraper import GithubScraper

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

matplotlib.use('agg')
app = Flask(__name__)


@app.route('/')
def index():
    github_scraper = GithubScraper()
    # Fetch data using the scraper module
    response = github_scraper.send_query()

    if response.status_code == 200:
        # Example usage:
        github_scraper.parse_html()
        topics = github_scraper.extract_topics()

        return render_template('index.html', topics=topics)

    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
