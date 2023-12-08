# GitHub Trends Visualization

## Overview

The GitHub Trends Visualization project aims to provide users with a dynamic and informative view of the current trends in programming languages and their associated repositories on GitHub. Leveraging web scraping techniques, the system collects real-time data from GitHub's trending page, offering users an up-to-date perspective on the rapidly evolving landscape of programming languages.

## Team Members

- **Roshan Shrestha (Group Leader) - C0901142**
- **Yubraj Rai - C0899391**
- **Piyumika Samarasuriyage - C0900440**
- **Pauline Angelica Balmores - C0901339**
- **Fuchun Li - C0901297**

## Project Scope

The project encompasses:

- Implementation of web scraping techniques to collect data from GitHub trending.
- Development of a Flask web application for displaying trends and repositories.
- Creation of a visually appealing and responsive UI using HTML, CSS, and other front-end technologies.
- Integration of Matplotlib/Numpy for graphical representation of programming language trends.
- Storing trending GitHub data in a Database.

## Features

1. **Web Scraping with BeautifulSoup:**

   - The project employs the powerful BeautifulSoup library to scrape relevant data from GitHub's trending page, ensuring the extraction of accurate and current information about the trending programming languages and repositories.

2. **Flask Web Application:**

   - A Flask web application is developed to make the trends accessible and user-friendly. Users can interact with the system through an intuitive interface, exploring trends and gaining insights into popular repositories.

3. **Responsive UI with HTML and CSS:**

   - The user interface is designed to be visually appealing and responsive. Using HTML and CSS, the system provides a seamless experience across different devices, allowing users to explore GitHub trends on desktops, tablets, and smartphones.

4. **Matplotlib for Data Visualization:**
   - Matplotlib, a widely used Python library for data visualization, is integrated to represent programming language trends graphically. Users can easily interpret trends through interactive and customizable charts and visualizations.

## Requirements

To run the project successfully, ensure that the following dependencies are installed:

- Python 3.x
- Flask
- Beautiful Soup
- Matplotlib

## Technologies Used

The project primarily utilizes:

- Advanced Python concepts, including object-oriented programming (OOP).
- Python libraries such as Flask, Beautiful Soup, and Matplotlib.
- HTML and CSS for building the user interface.

## Project Milestones

The project is divided into several phases:

1. **Planning and Setup:**
   - Define requirements, set up project structure, and assign roles.
2. **Web Scraping:**
   - Implement scraping, validate, and clean data.
3. **Flask Web Application:**
   - Develop the application, design UI, and integrate with scraped data.
4. **Data Visualization:**
   - Integrate Matplotlib for graphical representation.
5. **Testing and Debugging:**
   - Conduct thorough testing and resolve issues.
6. **Documentation and Finalization:**
   - Document code and functionalities, finalize the project for deployment.

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/github-trends-visualization.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```
   Open your web browser and navigate to http://localhost:5000 to access the GitHub Trends Visualization.

## Contribution Guidelines

- Fork the repository.
- Create a new branch: git checkout -b feature/new-feature.
- Make your changes and commit them: git commit -m 'Add new feature'.
- Push to the branch: git push origin feature/new-feature.
- Submit a pull request.
