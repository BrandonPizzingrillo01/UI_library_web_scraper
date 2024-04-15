# Data Scraping
import json.decoder  # Allows for seamless customization of JSON encoding, prevents numerous TypeErrors
import requests  # Used to get html elements from webpage
from bs4 import BeautifulSoup  # Turns souped html into readable html for parsing
from urllib.parse import urlparse, urljoin  # Allows for parsing and joining of url elements, utilized in url scraping

# DB Connection
import pyrebase  # Permits interaction between this script and firebase database

# Additional Modules
from datetime import datetime  # Utilized to measure exact length of data scrape, used to log errors in runtime
import time  # Utilized alongside datetime to measure scraper status
import numpy as np  # Primarily used as a conversion module in this script

# NeonDB Config
neondb_url = ''

# NeonDB Authentication
auth_token = ''

# DB Connection
config = {
    "apiKey": "AIzaSyCl6Z31-tlNON8G6aSlrNJkzazUzQA1xqY",
    "authDomain": "researchbookmarktest.firebaseapp.com",
    "databaseURL": "https://researchbookmarktest-default-rtdb.firebaseio.com",
    "projectId": "researchbookmarktest",
    "storageBucket": "researchbookmarktest.appspot.com",
    "messagingSenderId": "739418273205",
    "appId": "1:739418273205:web:4400f9b62476b05595d5fc",
    "measurementId": "G-2WEMT73R2R",
    "db_url": "https://researchbookmarktest-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
db_ref = firebase.database()


def get_html_content(url):
    """
    Collects HTML elements from passed URL.
    :param url: String parameter, Website url to scrape data from.
    :return: HTML content of webpage if connection is successful, or None if connection fails
    """
    # Attempt to connect and get HTML from url
    response = requests.get(url, verify=False)  # Verify = False to avoid certification errors upon accessing url

    # Check if connection is successful
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve content from {url}")
        return None


def find_tables(soup):
    """
    Uses souped HTML to find all instances of tables in the webpage
    :param soup: Souped html to parse for table values
    :return: List of html tables
    """
    tables = soup.find('table')
    return tables


def find_images(soup):
    """
    Uses souped HTML to find all instances of images in the webpage
    :param soup: Souped html to parse for image values
    :return: List of html images
    """
    images = soup.find('img')
    return images


def find_headers(soup):
    """
    Uses souped HTML to find all instances of header elements in the webpage
    :param soup: Souped html to parse for header values
    :return: List of html header
    """
    headers = [header.text for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    return headers


def find_url(soup, url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    urls = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        parsed_url = urlparse(full_url)

        # Check if it's a valid URL and not an anchor or JavaScript link
        if parsed_url.scheme and parsed_url.netloc:
            urls.add(full_url)

    return urls


def remove_duplicates(title):
    try:
        data = db_ref.child(''+title).get().val()
        unique_data = {}

    # Loop through the data and remove duplicates
        try:
            for key, value in data.items():
                if value not in unique_data.values():
                    unique_data[key] = value
                    db_ref.child('' + title).set(unique_data)
                else:
                    db_ref.child('' + title).remove()
                    print("Duplicates removed successfully.")

        # Update the parent node with the unique data
        except AttributeError or TypeError or json.JSONDecodeError or requests.exceptions.HTTPError as e:
            print(f'Exception {e} raised and handled (116). Continuing')
    except json.decoder.JSONDecodeError or TypeError or AttributeError as e:
        print(f'Exception {e} raised and handled (118). Continuing')

# Scrape Filters Function
# Filters: Length, date published, author
# Allow user to select filter possibly?

# Scrape Dates Function
def find_date(soup):
    try:
        # Search for common meta tags where the publication date might be specified
        soup.find('date')

        # Search for specific HTML elements where the publication date might be specified
        # This is a simplified example and may need to be adjusted based on the specific structure of the website
        date_patterns = [
            r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',  # Matches dates in the format DD-MM-YYYY or DD/MM/YYYY
            r'\b(\d{2,4}[-/]\d{1,2}[-/]\d{1,2})\b'  # Matches dates in the format YYYY-MM-DD or YYYY/MM/DD
        ]

        # If no date is found, return None
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Scrape Author Function

# Scrape Length Function

def main():
    """
    Main function to display web scraped data in html browser format
    :return: Web browser with displayed scraped information
    """
    # URL to scrape data from
    try:
        url_list = ['https://www.uxdesigninstitute.com/blog/guide-to-the-ui-design-process/', 'https://www.coursera.org/articles/ui-design', 'https://dribbble.com/resources/ui-design-principles', 'https://www.figma.com/resource-library/ui-design-principles/',  'https://ui.aceternity.com/components/wavy-background', 'https://ui.aceternity.com/', 'https://ui.aceternity.com/components/3d-card-effect', 'https://ui.aceternity.com/components/sparkles', 'https://www.interaction-design.org/literature/topics/ui-design-patterns', 'https://www.interaction-design.org/literature/article/10-great-sites-for-ui-design-patterns']
        high = len(url_list)
        url_num = np.random.randint(0, high)
        url = url_list[url_num]
        print(f'Currently Scraping: {url}')

        # Save scraped data into html_content
        html_content = get_html_content(url)

        if html_content:
            # These will need to go into the for loop
            scraped_list = []
            try:
                soup = BeautifulSoup(html_content, 'html.parser')
                scraped_list = find_url(soup, url)
            except TypeError as e:
                print(f'Exception {e} raised and handled (144). Continuing')

        # The loop will make a new soup object for each scraped link
        # The link will then be scraped and the loop will reset
        # Need to find a way to set a current url variable to scrape/make into soup
            for j in scraped_list:
                url = j
                html_content = get_html_content(url)
                soup = ''
                try:
                    soup = BeautifulSoup(html_content, 'html.parser')
                except TypeError as e:
                    print(f'Exception {e} raised and handled (204). Continuing')
                if soup.title == 'twitter' or soup.title == 'linkedin':
                    continue
                data = {
                    'site_title': str(soup.title()),
                    'images': str(find_images(soup)),
                    'tables': str(find_tables(soup)),
                    'headers': str(find_headers(soup)),
                    'url': str(find_url(soup, url)),
                }
                title_tag = soup.title
                if title_tag:
                    try:
                        # Extract the text of the title tag
                        title = title_tag.string.strip()
                        remove_duplicates(title)
                        db_ref.child('' + title).push(data)
                        print(f'Data from | {title} | successfully inserted into database')
                    except requests.exceptions.HTTPError or TypeError or AttributeError as e:
                        print(f'Exception {e} raised and handled (168). Continuing')
                else:
                    return "Title tag not found"

    except AttributeError or TypeError or json.JSONDecodeError or requests.exceptions.HTTPError as e:
        print(f'Exception {e} raised and handled (173). Continuing. ')

        # DB Insertion
        # Basic Insert
        # db_ref.push(data)

        # Refined Insert
        # db_ref.child('').child('').set(data)
        # db_ref.child('').push(data)
        # Possibly place this into a loop where scraper collects data from multiple sites?

        # Read Data From DB
        # queried_data = db_ref.child('Scraped Data').child('First Scrape').get()
        # print(queried_data.val())

        # Update Data From DB
        # db_ref.child('UI Aceternity').child('First Scrape').update({'site_title': 'UI Aceternity'})

        # Delete Data
        # Delete Single Value
        # db_ref.child('Notion').remove()

        # Delete Entire Node
        # db_ref.child('Scraped Data').remove()


sleep_interval = 5
# Calls main function
if __name__ == "__main__":
    count = 0
    startTime = time.time()
    while True:
        try:
            main()
            time.sleep(sleep_interval)
        except AttributeError or TypeError or json.JSONDecodeError or requests.exceptions.HTTPError as e:
            print(f'Exception {e} raised and handled (209). Continuing. (Critical Error Count: {count}/10)')
            count += 1
            print(f'Reached error {count} at {datetime.now()}')
            time.sleep(2)
            if count == 10:
                endTime = time.time()
                elapsedTime = endTime - startTime
                print('Max errors reached, failsafe activated.')
                db_ref.child('0A - Failsafe Log').push(f'Failsafe reached, scraping terminated at {datetime.now()}. Scraper ran for {elapsedTime}')
                break


# Additional
# Extract tables
# tables = find_tables(soup)
# print(f"Tables: {tables}")

# Extract images
# images = find_images(soup)
# print(f"Images: {images}")

# Extract headers
# headers = find_headers(soup)
# print(f"Headers: {headers}")

# Extract URL
# url_scrape = find_url(soup, url)
# print(f"Url: {url_scrape}")

# html_content = f"IMAGES: {images}"
# html_content += f"TABLES: {tables}"
# html_content += f"HEADERS: {headers}"

# showcase_items(html_content, images, tables, headers)

# url = "https://www.bearcognition.com/"
# url = "https://www.researchbookmark.io/webinar"
# url = 'https://ui.aceternity.com/'
# url = 'https://ui.aceternity.com/components/3d-card-effect'
# url = 'https://ui.aceternity.com/components/sparkles'
# url = 'https://github.com/'
# url = 'https://www.interaction-design.org/literature/topics/ui-design-patterns'
# url = 'https://www.interaction-design.org/literature/article/10-great-sites-for-ui-design-patterns'
