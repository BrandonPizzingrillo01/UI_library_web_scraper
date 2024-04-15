WEB SCRAPER SHOWCASE README

Python file created in PyCharm IDE that implements 5 modules to scrape a url for data, and present the findings in a local browser. 

Modules:
- Requests: Used to get html elements from webpage
- From bs4, BeautifulSoup: Turns souped html into readable html for parsing
- From http, server: Allows for connection to http local server
- Socketserver: Provides framework for creating network servers
- Webbrowser: Allows for IDE to open local web browser to view souped output

All 5 modules are utilized to scrape and display the data. Each module is called within the main() method, some being called within supporting methods called by main().

Methods:
- main(): Main function to display web scraped data in html browser format. 
- get_html_content(url): Collects HTML elements from passed URL. Param: url: String parameter, website url to scrape data from.
- find_tables(soup): Uses souped HTML to find all instances of tables in the webpage
- find_images(soup): Uses souped HTML to find all instances of images in the webpage
- find_headers(soup): Uses souped HTML to find all instances of header elements in the webpage

Extra Additions:
- Added print statements to state error messages along with lines that caused them
- Added extensive error handling to prevent critical errors from stopping the running of the scraper
- Added additional informational print statements to monitor scraper status and data insertions/duplicate removals
- Added method to remove duplicates if data that is being inserted is already present in the database
