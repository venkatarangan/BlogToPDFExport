# pip install requests beautifulsoup4 pandas

import requests
from bs4 import BeautifulSoup
import csv

# URL format to iterate over pages
base_url = "https://www.example.com/blogs/?paged={}"

# Function to fetch and parse a single page
def fetch_page(page_number):
    try:
        url = base_url.format(page_number)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        return None

# Function to extract headings and URLs from a given BeautifulSoup object
def extract_posts(soup):
    if soup is None:
        return []
    articles = soup.find_all('article')
    posts = []
    for article in articles:
        headline = article.find('h1', class_='entry-title')
        if headline and headline.a:
            posts.append((headline.get_text(strip=True), headline.a['href']))
    return posts

# List to store all posts across all pages
all_posts = []

# Iterate over each page
# The number of pages in the blog post listing has to be determined prior to invoking.
# This has to be done manually for now. 

for page_number in range(1, 17):  # 16 pages total in the blog I had so it is 17 here
    soup = fetch_page(page_number)
    posts = extract_posts(soup)
    all_posts.extend(posts)
    print(f"Page {page_number} processed, found {len(posts)} posts.")

# Saving to CSV file
csv_filename = 'example_Blogs_Posts.csv'  # Default folder in Windows
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'URL'])  # Writing header
    writer.writerows(all_posts)

print(f"All posts have been extracted and saved to {csv_filename}.")
