## Day 20 : Web Scraping/Extraction

🔍 Web Scraping is used to extract relevant data from websites. Also known as screen scraping or web data extraction, web scraping makes it possible to download specific data from web pages based on defined parameters. 
Today I worked with requests and Beautiful soup library to scrap data from https://lnkd.in/gkQ2Xphp

#### Steps involved in scraping data:

**🛠 Install the Requests and Beautiful Soup libraries if not installed:**
 - <p>⭕ pip install requests bs4</p>
\
**📚 Import the libraries:**
 - <p>⭕ import requests</p>
 - <p>⭕  from bs4 import BeautifulSoup</p>
\
**🔗 Send a GET request to the website you want to scrape and Check the response status code:**
 - <p>⭕ url = "https://lnkd.in/gkQ2Xphp"</p>
 - <p>⭕  response = requests.get(url)</p>
\
**✏ Parse the HTML content:**
 - <p>⭕ soup = BeautifulSoup(response.content, "html.parser")</p>
\
**🕵‍♂️ Locate the elements you want to scrape:**
 - <p>⭕  You can use Beautiful Soup methods like find(), find_all(), select(), and select_one() to locate specific elements in the HTML tree.</p>
\
**📝 Extract the data from the elements:**
 - <p>⭕  Once you have located the elements, you can use BeautifulSoup methods like get_text(), get() (for attributes), and attrs (for all attributes) to extract the data you want.</p>
\
**📍 Save the scraped data:**
 - <p>⭕  You can save the scraped data to a file (CSV, JSON, etc.) or store it in a database for further analysis. for more scraping practice check the above site</p>
\
#100DaysOfDataEngineering #DataEngineering #Data
