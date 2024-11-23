# A/B Testing for Gamers

## Project Overview

This project analyzes and visualizes user data and purchase activity for a gaming platform, leveraging tools like Streamlit, Plotly, and SQLite to provide insights. The main goal is to offer a dashboard for decision-makers to monitor and understand user engagement, revenue patterns, and other key metrics related to the game's charm events.

### Key Components:
1. **Data Analysis (analysis.ipynb)**: 
   - A Jupyter Notebook where the main data analysis is performed. This includes exploratory data analysis (EDA), feature engineering, and statistical summaries. It provides an understanding of the user behavior and the impact of events.
   
2. **SQL Operations (sql.ipynb)**:
   - A Jupyter Notebook for SQL-related tasks. This file includes SQL queries used to extract, transform, and load (ETL) data from the database for analysis and further processing.
   
3. **Interactive Dashboard (app.py)**:
   - A Streamlit application that presents the data insights visually, allowing users to interact with the data in a more intuitive way. It is the main interface for presenting the results of the analysis.


## Project Structure

The project contains the following directories and files:

- **01_data/**  # Raw data files (CSV)
  - `charms.csv`  # User charms data
  - `iaps.csv`  # In-app purchases data
  - `data.csv`  # Additional raw data (if applicable)

- **02_db/**  # SQLite database
  - `my_database.db`  # Database for storing processed data

- **03_notebooks/**  # Jupyter notebooks for analysis and SQL queries
  - `analysis.ipynb`  # Data analysis notebook
  
- **04_dashboard/**  # Streamlit application
  - `app.py`  # Main Streamlit app for data visualization

- **05_sql/**  # SQL scripts for data extraction and transformation
  - `sql.ipynb`  # SQL queries notebook


## Requirements

Before running the app, you will need to install the necessary Python packages. The requirements are listed below:

1. **Python 3.x**: Ensure you have Python installed. It is recommended to use a virtual environment.

2. **Required Libraries**: You can install the necessary Python libraries by running the following commands:

    ```bash
    pip install streamlit
    pip install plotly
    pip install pandas
    pip install sqlite3  # If not already installed
    ```

3. **Running the Application**: After installing the necessary libraries, you can run the Streamlit app by executing the following command in your terminal:

    ```bash
    streamlit run 04_dashboard/app.py
    ```

    This will start a local development server, and you can view the dashboard by opening `http://localhost:8501` in your browser.

## Workflow and Data Analysis

### 1. **Data Analysis (analysis.ipynb)**:
   - The analysis notebook focuses on understanding the datasets, finding correlations, and deriving insights about the users' behavior. Key steps in the notebook include:
     - Data cleaning and preprocessing.
     - Exploratory data analysis (EDA) including plotting and statistical analysis.
     - Feature extraction and interpretation.
   
   Example insights from the analysis might include user spending patterns, correlation between in-app purchases and charm events, etc.

### 2. **SQL Operations (sql.ipynb)**:
   - The SQL notebook includes important SQL queries used for querying the database. For instance:
     - Extracting relevant data for analysis.
     - Performing aggregations, joins, and transformations.
     - Updating or inserting new data into the SQLite database.

   Example SQL queries used in the project:
   ```sql
   SELECT COUNT(DISTINCT SERVER_ID) AS users_finished_event
   FROM charms
   WHERE SETS_COMPLETED_LIFETIME = 18
   AND DATE BETWEEN '2019-12-05' AND '2020-01-02';