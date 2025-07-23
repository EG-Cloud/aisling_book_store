# AISLING Bookstore Data Pipeline

## About the Project

AISLING is a fictional bookstore used as a case study for building a complete data pipeline—from data collection to automated loading into a PostgreSQL database. This project served as my first end-to-end data journey, helping me explore and learn several key components of data engineering and analysis.

## Project Workflow

### 1. Learning Web Scraping
I started by following a short course on Udemy to understand the fundamentals of web scraping using Python libraries such as `requests` and `BeautifulSoup`.

### 2. Exploring Website Structure
I analyzed the structure of the Books to Scrape website to identify how to extract relevant product information like book title, price, category, description, and rating.

### 3. Final Web Scraping Script
After testing and refining my code, I built a reliable script to extract structured book data and export it to a clean CSV file.

### 4. Synthetic Data Generation
Using ChatGPT, I created five realistic CSV datasets that simulate a working e-commerce bookstore environment:

- buyers.csv
- products.csv
- reviews.csv
- sellers.csv
- transactions.csv

### 5. Data Wrangling with Python
I cleaned and transformed the datasets using Python and Pandas:
- Parsing dates
- Handling missing and duplicate values
- Standardizing string formatting
- Filling missing price values based on discount logic
- Detecting outliers and fixing inconsistent types

### 6. Data Wrangling with PostgreSQL
I rewrote the same cleaning rules using SQL, ensuring I could achieve similar or better data quality directly in PostgreSQL. This helped reinforce my understanding of SQL-based data wrangling.

### 7. Exploratory Data Analysis (EDA)
I performed:
- Univariate and bivariate analysis
- Customer segmentation by age, gender, and country
- Revenue trends over time
- Most profitable categories and top-rated books
- Answered key business questions from a stakeholder perspective

### 8. Automation
I developed a complete Python automation script that:
- Cleans each dataset
- Logs every deletion and anomaly
- Loads data into PostgreSQL using efficient COPY operations
- Archives all processed files with timestamps

## What I Learned

- Web scraping with BeautifulSoup and requests
- Data cleaning techniques in both Python and SQL
- Building and structuring an automated data pipeline
- Managing referential integrity and foreign key consistency
- Logging and documenting data transformations
- Preparing data for future visualization tools like Power BI

## Conclusion

This project gave me hands-on experience in the complete data lifecycle, from scraping to storing and preparing data for business analysis. I now feel confident building repeatable pipelines and structuring clean, analyzable datasets. The next step will be to connect these tables to Power BI and build interactive dashboards.
