# Import necessary libraries and modules
import base64
import io
import os
import sqlite3
import sys
import seaborn as sns
import matplotlib
from flask import Flask, render_template, request
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
from models.repository_model import RepositoryModel
from scraper.github_scraper import GithubScraper

# Add the project root to the system path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
sys.path.append(project_root)

# Set up Flask application
app = Flask(__name__)

# Configure Matplotlib for Agg backend
matplotlib.use('agg')
app = Flask(__name__)


def perform_web_scraping_and_insert(duration, exist):
    """
    Perform web scraping using GithubScraper and insert data into the database.
    """
    github_scraper = GithubScraper()
    response = github_scraper.fetch_data(duration)

    if response.status_code == 200:
        repositories = github_scraper.extract_repositories()

        # Connect to the database
        con = sqlite3.connect("github_trending.db")
        cur = con.cursor()

        if exist:
          # Drop the table if it exists (for demonstration purposes)
          cur.execute("DROP TABLE IF EXISTS repositories")

          # Create the 'repositories' table
          cur.execute("""
            CREATE TABLE IF NOT EXISTS repositories (
                name TEXT,
                owner TEXT,
                description TEXT,
                language TEXT,
                stars_total TEXT,
                stars_today TEXT,
                duration TEXT,
                repository_url TEXT
             )
            """)

        # Insert data into the 'repositories' table
        cur.executemany("""
            INSERT INTO repositories VALUES (?, ?, ?, ?, ?, ?,?,?)
        """, [
            (repo.name, repo.owner, repo.description,
             repo.language, repo.stars_total, repo.stars_today, duration,repo.repository_url)
            for repo in repositories
        ])

        # Commit the changes to the database
        con.commit()

        # Close the database connection
        con.close()
    return repositories


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


@app.route('/', methods=['GET', 'POST'])
def index():
    duration = request.args.get('duration',"daily")
    # Check if the database file exists
    db_file = "github_trending.db"
    if not os.path.exists(db_file):
        # If the database file doesn't exist, create it and perform web scraping
        perform_web_scraping_and_insert(duration, True)

    # Connect to the database
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # Check if the 'repositories' table exists and has data
    cur.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='repositories'")
    table_exists = cur.fetchone()[0] > 0

    if not table_exists:
        # If the 'repositories' table doesn't exist or has no data, perform web scraping
        perform_web_scraping_and_insert(duration, True)

    # Fetch data from the database
    cur.execute(f"SELECT * FROM repositories WHERE duration = ?", (duration,))
    repositories_data = cur.fetchall()

    # Close the database connection
    con.close()
    # Check if repositories_data is empty
    if not repositories_data:
        print("No data found in the 'repositories' table for the specified duration.")
        repositories = perform_web_scraping_and_insert(duration, False)
        print(f'Data from local\n{repositories_data}')
    else:
        print(f'Data from local\n{repositories_data}')
        # Convert data to RepositoryModel instances
        repositories = [RepositoryModel(*repo_data) for repo_data in repositories_data]

    return render_template('index.html', selected_option=duration, repoList=repositories)


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    # Fetch data from the database
    con = sqlite3.connect("github_trending.db")
    cur = con.cursor()
    cur.execute("SELECT language, COUNT(*) FROM repositories GROUP BY language")
    data = cur.fetchall()
    con.close()

    # Create a Matplotlib figure
    fig = plt.figure(figsize=(10, 6))

    # Add a subplot to the figure
    axis = fig.add_subplot(1, 1, 1)

    # Extract languages and their counts for plotting
    languages, counts = zip(*data)

    # Plotting the bar chart
    axis.bar(languages, counts, color='red')
    axis.set_xlabel('Programming Languages')
    axis.set_ylabel('Number of Repositories')
    axis.set_title('Programming Language Distribution')

    # Rotate x-axis labels for better readability
    axis.set_xticks(languages)
    axis.set_xticklabels(languages, rotation='vertical')

    # Save the plot to a BytesIO object
    png_image = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(png_image)

    # Encode PNG image to base64 string
    png_image_64 = "data:image/png;base64,"
    png_image_64 += base64.b64encode(png_image.getvalue()).decode('utf8')

    # Pass the BytesIO object to the template
    return render_template('graph.html', image=png_image_64)


@app.route('/pieChart', methods=['GET', 'POST'])
def pieChart():
    # Fetch data from the database
    con = sqlite3.connect("github_trending.db")
    cur = con.cursor()
    cur.execute("SELECT language, COUNT(*) FROM repositories GROUP BY language")
    data = cur.fetchall()
    con.close()

    # Create a Matplotlib figure
    fig = plt.figure(figsize=(14, 12))  # Adjust the size as needed

    # Extract languages and their counts for plotting
    languages, counts = zip(*data)
    # Adjust the explode tuple as needed
    explode = (1, 0, 0, ...)
    # autopct: the percent
    plt.pie(counts, labels=languages, autopct='%1.1f%%', startangle=60, textprops={'fontsize': 6})

    plt.title('Language Share')
    # Place the legend outside the pie chart to avoid overlapping with the chart itself
    plt.legend(labels=languages, loc="center left", bbox_to_anchor=(1, 0.5))

    plt.show()

    # Save the plot to a BytesIO object
    png_image = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(png_image)

    # Encode PNG image to base64 string
    png_image_64 = "data:image/png;base64,"
    png_image_64 += base64.b64encode(png_image.getvalue()).decode('utf8')

    # Pass the BytesIO object to the template
    return render_template('graph.html', image=png_image_64)


@app.route('/boxPlot', methods=['GET', 'POST'])
def boxPlot():
    # Fetch data from the database
    con = sqlite3.connect("github_trending.db")
    cur = con.cursor()
    cur.execute("SELECT language, COUNT(*) FROM repositories GROUP BY language")
    data = cur.fetchall()
    con.close()

    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=['language', 'count'])

    # Create a Matplotlib figure
    fig = plt.figure(figsize=(10, 6))

    # Use the DataFrame for plotting
    sns.boxplot(x='language', y='count', data=df)
    plt.xlabel('Programming Language')
    plt.ylabel('Stars')
    plt.title('Stars Distribution by Language')
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    # Save the plot to a BytesIO object
    png_image = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(png_image)

    # Encode PNG image to base64 string
    png_image_64 = "data:image/png;base64,"
    png_image_64 += base64.b64encode(png_image.getvalue()).decode('utf8')

    # Pass the BytesIO object to the template
    return render_template('graph.html', image=png_image_64)


if __name__ == '__main__':
    app.run(debug=True)
