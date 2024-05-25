# pip install pandas pdfkit
# pip install pytz
# Install wkhtmltopdf from wkhtmltopdf.org a

import pandas as pd
import pdfkit
import requests
import os
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import datetime
import subprocess
import logging

def sanitize_filename(title):
    import string
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    return ''.join(c for c in title if c in valid_chars)

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist, allowed_methods=frozenset(['GET', 'POST']))
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def read_data_from_csv(csv_file):
    try:
        data = pd.read_csv(csv_file)
        logging.info(f"Read {len(data)} entries from {csv_file}")
        return data
    except Exception as e:
        logging.error(f"Failed to read CSV file: {e}")
        return pd.DataFrame()

def fetch_and_parse_html(url):
    session = requests_retry_session()
    try:
        response = session.get(url, timeout=60)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1', class_='entry-title').get_text(strip=True)
        date_string = soup.find('time', class_='entry-date published')['datetime']
        date = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
        return title, date
    except Exception as e:
        logging.error(f"Failed to fetch or parse HTML from {url}: {e}")
        return "Untitled", datetime.datetime.now()

def convert_to_pdf(url, output_directory, default_title):
    title, date = fetch_and_parse_html(url)
    filename = sanitize_filename(title if title != "Untitled" else default_title) + '.pdf'
    output_path = os.path.join(output_directory, filename)
    options = {
        'page-size': 'Letter',
        'minimum-font-size': 12,
        'encoding': "UTF-8",
        'custom-header': [('User-Agent', 'Mozilla/5.0')],
        'no-outline': None
    }
    try:
        logging.info(f"Converting {url} to PDF as {output_path}")
        pdfkit.from_url(url, output_path, options=options)
        check_pdf_content(output_path)
    except Exception as e:
        logging.error(f"Failed to convert {url} to PDF: {e}")
    set_file_creation_date(output_path, date)

def check_pdf_content(filepath):
    if os.path.getsize(filepath) == 0:
        logging.warning(f"Generated PDF is empty: {filepath}")

def set_file_creation_date(filepath, creation_date):
    formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
    command = f'(Get-Item "{filepath}").creationtime=$(Get-Date "{formatted_date}")'
    subprocess.run(['powershell', '-command', command], check=True)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    csv_filename = 'example_blogs_posts.csv'
    output_directory = 'pdf_output'
    data = read_data_from_csv(csv_filename)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for index, row in data.iterrows():
        default_title = f'Untitled_{index}'
        convert_to_pdf(row['URL'], output_directory, row.get('Title', default_title))

if __name__ == "__main__":
    main()
    logging.info("All pages have been processed and saved as PDFs.")
