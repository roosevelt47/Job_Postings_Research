import requests
import json
import os

"""
Query Params
query
*
developer jobs in chicago
String
Free-form jobs search query. It is highly recommended to include job title and location as part of the query, see query examples below.

Examples:

web development jobs in chicago
marketing manager in new york via linkedin
page
(optional)
1
Number
Page to return (each page includes up to 10 results).

Default: 1

Allowed values: 1-100

num_pages
(optional)
1
Number
Number of pages to return, starting from page.

Default: 1

Allowed values: 1-20

Note: requests for more than one page and up to 10 pages are charged x2 and requests for more than 10 pages are charged 3x.

country
(optional)
us
String
Country code of the country from which to return job postings. Please note that this parameter must be set in order to get jobs in a specific country, for example, to query for software developer jobs in Berlin, one should add country=de to the request - e.g. query=software+developers+in+berlin&country=de.

Default: us

Allowed values: See https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2

language
(optional)
String
Language code in which to return job postings. Leave empty to use the primary language in the specified country (country parameter).

Note that each country supports certain languages. In case a language not supported by the specified country is used, it is likely that no results will be returned.

Allowed values: See https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes

date_posted
(optional)
Enum
Find jobs posted within the time you specify.

Default: all

Allowed values: all, today, 3days, week, month

# testing criteria
3 days, then current day, then current day.

work_from_home
(optional)
Boolean
Only return work from home / remote jobs.

Default: false

employment_types
(optional)
String
Find jobs of particular employment types, specified as a comma delimited list of the following values: FULLTIME, CONTRACTOR, PARTTIME, INTERN.

job_requirements
(optional)
String
Find jobs with specific requirements, specified as a comma delimited list of the following values: under_3_years_experience, more_than_3_years_experience, no_experience, no_degree.

radius
(optional)
Number
Return jobs within a certain distance from location as specified as part of the query (in km).

exclude_job_publishers
(optional)
String
Exclude jobs published by specific publishers, specified as a comma (,) separated list of publishers to exclude.

Example: BeeBe,Dice

fields
(optional)
String
A comma separated list of job fields to include in the response (field projection). By default all fields are returned.

Example: employer_name,job_publisher,job_title,job_country
"""

url = "https://jsearch.p.rapidapi.com/search"
querystring = {"query": "software intern jobs in canada", "page": "1",
               "num_pages": "1", "country": "ca", "date_posted": "week"}

headers = {
    "x-rapidapi-key": "apikeyhere",
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
response_json = response.json()

# Prettify JSON
pretty_json = json.dumps(response_json, indent=4)

# Print prettified JSON
print(pretty_json)

# Export to JSON file
# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Define the relative path
relative_path = os.path.join(script_dir, 'frontend', 'data.json')

# Export to JSON file
with open(relative_path, 'w') as f:
    f.write(pretty_json)

"""
const request = require('request');

const options = {
  method: 'GET',
  url: 'https://jsearch.p.rapidapi.com/search',
  qs: {
    query: 'software intern jobs in canada',
    page: '1',
    num_pages: '1',
    country: 'ca',
    date_posted: 'week'
  },
  headers: {
    'x-rapidapi-key': '28e0ec2275msh2c235abb3fa00e4p12919cjsn9489555acb73',
    'x-rapidapi-host': 'jsearch.p.rapidapi.com'
  }
};

request(options, function (error, response, body) {
	if (error) throw new Error(error);

	console.log(body);
});
"""
