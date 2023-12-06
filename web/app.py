# web/app.py
from flask import Flask, render_template
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
from collections import Counter
from scraper import github_scraper  # Import the scraper module

matplotlib.use('agg')
app = Flask(__name__)


@app.route('/')
def index():
    # Fetch data using the scraper module
    response = github_scraper.send_query()

    if response.status_code == 200:
        soup = github_scraper.parse_html(response)
        topic_list = github_scraper.extract_topics(soup)

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

        # Save the plot to a BytesIO object
        img_bytes = BytesIO()
        plt.savefig(img_bytes)
        img_bytes.seek(0)
        data = img_bytes.read()
        print(data)

        # Pass the BytesIO object to the template
        return render_template('index.html', img_data=data)

    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
