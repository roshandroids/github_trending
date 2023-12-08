# web/app.py
import base64
import io
import sqlite3
import sys
import os

from flask import Flask, render_template, request, redirect, url_for
import matplotlib
from collections import Counter

from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from scraper.github_scraper import GithubScraper

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
sys.path.append(project_root)

matplotlib.use('agg')
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
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

@app.route('/getSomethingFromDB')
def getSomethingFromDB():
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute("DROP TABLE movie")
    cur.execute("CREATE TABLE movie(title, year, score)")
    cur.execute("""
        INSERT INTO movie VALUES
            ('Monty Python and the Holy Grail', 1975, 8.2),
            ('And Now for Something Completely Different', 1971, 7.5)
    """)
    con.commit()
    cursor = con.execute('''select * from movie where year''')
    movies = []
    for row in cursor:
        movie = {'title': row[0], 'year': row[1], 'score': row[2]}
        movies.append(movie)
    return render_template('get_data.html', movies=movies)


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    duration = request.args.get('duration', '')
    github_scraper = GithubScraper()
    response = github_scraper.fetch_data(duration)

    if response.status_code == 200:
        repositories = github_scraper.extract_repositories()

        language_list = [repo.language for repo in repositories]
        # Create a Matplotlib figure
        fig = plt.figure(figsize=(10, 6))  # Adjust the size as needed

        # Add a subplot to the figure
        axis = fig.add_subplot(1, 1, 1)

        # Count the occurrences of each programming language
        language_counts = Counter(language_list)

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
        error_message = f"Failed to retrieve search results. Status code: {response.status_code}"
        print(error_message)
        return render_template('error.html', message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
