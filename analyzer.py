import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

# Buzzwords
buzzwords = ["HTML", "Python", "Java", "Kotlin", "Office", "Excel"]

# Captcha Workaround:
# Replace de.indeed.com -> indeed.com and Koeln -> New York, NY

# Query Terms
title = "Android"
location = "Köln"
pages = 1 # 15 listings per page

# Get necessary parameters for pages
base_url = "https://de.indeed.com"
url = f"{base_url}/jobs?q={title}&l={location}"


def getPageSoup(page_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
        'referer': 'https://www.google.com/'}

    page = requests.get(page_url, headers)
    soup = BeautifulSoup(page.content, "html.parser")

    return soup


job_urls = []

# Iterate through the first 4 pages (15 job listings per page)
for page_index in range(0, pages):
    # Prepare paged url
    starting_index = page_index * 10
    page_url = url + f"&start={starting_index}"

    # Parse Page
    soup = getPageSoup(page_url)

    # Add links to list
    cards = soup.find_all("a", class_="resultWithShelf")
    links = [card["href"] for card in cards]

    # Add all prepared links to list
    for link in links:
        job_urls.append(base_url + link)


if len(job_urls) == 0:
    raise Exception("No Urls found!")

job_descriptions = []

# Iterate through all job listings
for idx, job_url in enumerate(job_urls):
    print(f"{idx + 1} / {len(job_urls)}")

    # Get a single page
    job_soup = getPageSoup(job_url)

    # Find the job description block
    job_description_soup = job_soup.find("div", id="jobDescriptionText")

    # Generate single string
    joined_strings = " ".join(job_description_soup.strings)

    # Add string to list
    job_descriptions.append(joined_strings)


buzzword_counts = {buzzword: 0 for buzzword in buzzwords}

# Check Job Descriptions for Buzzwords
for job_description in job_descriptions:
    for buzzword in buzzwords:
        if buzzword in job_description:
            buzzword_counts[buzzword] += 1


# Plots the results
plt.title("Buzzword Analysis")
plt.xlabel("Buzzword")
plt.ylabel("Occurences")
plt.bar(buzzword_counts.keys(), buzzword_counts.values())
plt.show()
