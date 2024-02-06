import requests # Used to get html elements from webpage
from bs4 import BeautifulSoup # Turns souped html into readable html for parsing
import http.server # Allows for connection to http local server
import socketserver # Provides framework for creating network servers
import webbrowser # Allows for IDE to open local web browser to view souped output

def get_html_content(url):
    """
    Collects HTML elements from passed URL.
    :param url: String parameter, Website url to scrape data from.
    :return: HTML content of webpage if connection is successful, or None if connection fails
    """
    # Attempt to connect and get HTML from url
    response = requests.get(url, verify = False) # Verify = False to avoid certification errors upon accessing url

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
    tables = soup.find_all('table')
    return tables

def find_images(soup):
    """
    Uses souped HTML to find all instances of images in the webpage
    :param soup: Souped html to parse for image values
    :return: List of html images
    """
    images = soup.find_all('img')
    return images

def find_headers(soup):
    """
    Uses souped HTML to find all instances of header elements in the webpage
    :param soup: Souped html to parse for header values
    :return: List of html header
    """
    headers = [header.text for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    return headers

def main():
    """
    Main function to display web scraped data in html browser format
    :return: Web browser with displayed scraped information
    """
    # URL to scrape data from
    url = "https://www.uxpin.com/studio/blog/design-systems-vs-pattern-libraries-vs-style-guides-whats-difference/#:~:text=Pattern%20library%20%28Molecules%20%26%20Organisms%29%3A%20A%20pattern%20is,collection%20of%20UI%20patterns%20within%20a%20design%20system."
    # Save scaped data into html_content
    html_content = get_html_content(url)

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract tables
        tables = find_tables(soup)
        print(f"Tables: {tables}")

        # Extract images
        images = find_images(soup)
        print(f"Images: {images}")

        # Extract headers
        headers = find_headers(soup)
        print(f"Headers: {headers}")

        html_content = f"IMAGES: {images}"
        html_content += f"TABLES: {tables}"
        html_content += f"HEADERS: {headers}"

        with open("index.html", "w") as file:
            file.write(html_content)

        handler = http.server.SimpleHTTPRequestHandler

        port = 8092

        with socketserver.TCPServer(("", port), handler) as httpd:
            try:
                # Print a message indicating that the server has started
                print(f"Server started at http://localhost:{port}")

                # Open a new browser tab to access the server
                webbrowser.open_new_tab(f"http://localhost:{port}")

                # Start serving requests indefinitely
                httpd.serve_forever()

            except OSError:
                # Handle keyboard interrupt (e.g., Ctrl + C)
                print("\nServer shutting down...")
                httpd.shutdown()
                print("Server stopped.")

# Calls main function
if __name__ == "__main__":
    main()
