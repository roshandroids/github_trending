# web/app.py
import base64
import io
import sys
import os
from io import BytesIO

from flask import Flask, render_template, request
import matplotlib
from collections import Counter

from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from scraper.github_scraper import GithubScraper

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
sys.path.append(project_root)

matplotlib.use('agg')
app = Flask(__name__)


@app.route('/')
def index():
    duration = request.args.get('duration', '')
    github_scraper = GithubScraper()
    response = github_scraper.fetch_data(duration)

    if response.status_code == 200:
        repositories = github_scraper.extract_repositories()
        return render_template('index.html', repoList=repositories)
    else:
        error_message = f"Failed to retrieve search results. Status code: {response.status_code}"
        print(error_message)
        return render_template('error.html', message=error_message)


@app.route('/graph')
def graph():
    github_scraper = GithubScraper()
    # Fetch data using the scraper module
    response = github_scraper.fetch_data()

    if response.status_code == 200:
        topic_list = github_scraper.extract_topics()

        print(topic_list)
        # Create a Matplotlib figure
        fig = plt.figure(figsize=(10, 6))  # Adjust the size as needed

        # Add a subplot to the figure
        axis = fig.add_subplot(1, 1, 1)

        # Count the occurrences of each programming language
        language_counts = Counter(topic_list)

        # Extract languages and their counts for plotting
        languages = list(language_counts.keys())
        counts = list(language_counts.values())

        # Plotting the bar chart
        axis.bar(languages, counts, color='skyblue')
        axis.set_xlabel('Programming Languages')
        axis.set_ylabel('Number of Occurrences')
        axis.set_title('Programming Language Distribution')
        # Rotate x-axis labels for better readability
        axis.set_xticks(languages)
        axis.set_xticklabels(languages, rotation='vertical')
        # Show the plot
        plt.show()
        # Convert plot to PNG image
        pngImage = io.BytesIO()
        canvas = FigureCanvas(fig)
        canvas.print_png(pngImage)

        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(
            pngImage.getvalue()).decode('utf8')

        # Pass the BytesIO object to the template
        return render_template('graph.html', image=pngImageB64String)

    else:
        print(
            f"Failed to retrieve search results. Status code: {response.status_code}")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
