import csv
from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime

pd.set_option('display.max_colwidth', 50)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

jobs = scrape_jobs(
    site_name=["indeed","google","glassdoor"],
    search_term="intern new grad",
    google_search_term="intern jobs Canada since yesterday",
    location="Canada",
    results_wanted=20,
    hours_old=48,
    country_indeed='Canada',

    # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],

    # Potential Enhancements: Explore integrating with talent.com, utilizing proxy servers for scraping, and leveraging the ChatGPT API for data analysis. Investigate scraping government job boards and directly obtaining application URLs.
    # Note: Initial attempts to scrape data from talent.ca were unsuccessful.
    # LinkedIn Scraping: High-quality proxy servers are required for effective LinkedIn scraping, as free options proved unreliable during testing. Further investigation is warranted.
    # AI Model Comparison: Comparing ChatGPT and Perplexity revealed limitations with web search functionality in the API version, restricting access to web-based search results.
    # Government Job Boards: Scraping government job boards requires further research and analysis due to potential complexities in data structure and accessibility.
    # Application URL Extraction: Directly scraping application URLs presents a challenge on job boards requiring user login. Strategies for circumventing this obstacle should be explored.
    # Job Board Selection: Due to challenges in obtaining direct application URLs, the script will initially focus on scraping from
    
)

# Generate a timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"jobs_{timestamp}.csv"

jobs.to_csv(filename, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel