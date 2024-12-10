import json
import glob
from collections import Counter, defaultdict
from datetime import datetime

# Load all JSON files
file_paths = glob.glob("*.json")
all_jobs = []
job_occurrences = defaultdict(list)

for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if 'data' in data:
            for job in data['data']:
                all_jobs.append(job)
                job_occurrences[job['job_id']].append(file_path)
        else:
            print(f"Warning: 'data' key not found in {file_path}")

# Identify duplicates based on job_id
job_id_to_title = {job['job_id']: job['job_title'] for job in all_jobs}
job_ids = [job['job_id'] for job in all_jobs]
duplicate_job_ids = [item for item,
                     count in Counter(job_ids).items() if count > 1]

# Function to decode file name to readable date and time


def decode_filename(filename):
    timestamp_str = filename.split('.')[0]
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H-%M-%S-%fZ")
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


# Get duplicate job titles and their occurrences
duplicate_job_titles = {}
for job_id in duplicate_job_ids:
    title = job_id_to_title[job_id]
    occurrences = job_occurrences[job_id]
    duplicate_job_titles[title] = {
        'count': len(occurrences),
        'dates': [decode_filename(occurrence) for occurrence in occurrences]
    }

# General analysis
job_titles = [job['job_title'] for job in all_jobs]
employers = [job['employer_name'] for job in all_jobs]
locations = [job['job_location'] for job in all_jobs]

# Print analysis results
print(f"Total jobs: {len(all_jobs)}")
print(f"Duplicate jobs: {len(duplicate_job_ids)}")
print(f"Unique job titles: {len(set(job_titles))}")
print(f"Unique employers: {len(set(employers))}")
print(f"Unique locations: {len(set(locations))}")

# Print duplicate job titles with occurrences
print("Duplicate job titles and their occurrences:")
for title, info in duplicate_job_titles.items():
    print(f"Title: {title}, Count: {info['count']}, Dates: {info['dates']}")
