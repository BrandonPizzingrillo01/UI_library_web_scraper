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
- 