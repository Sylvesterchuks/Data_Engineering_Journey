## Day 18: Types of Data and Data Sources Part 1

The previous task focused on working with different files saved on our local system. Today we learnt about different categories of data:

**Here we will categorize:**
<p>
💡 Data based on formats
</p>
<p>💡 Data based on structure</p>
<p></p>💡 Data based on sources</p>

<hr>
**Data based on formats includes:**
<div>
✒ CSV (Comma-Separated Values) - CSV files store tabular data in plain text format. Each row represents a record, and each column represents a field.

✒ XML (Extensible Markup Language) - XML files store structured data in a hierarchical format using tags.

✒ JSON (JavaScript Object Notation) - JSON files store structured data in a text format using key-value pairs.

✒ Spreadsheet- Spreadsheet files store tabular data in a tabular format. Although data in spreadsheets are in plain text, the files can be stored in custom formats and include additional information such as formatting, formulas, etc. The most common spreadsheet includes Excel, Google sheets.

✒ Database-specific files - Some databases, such as MySQL and Oracle, have their own file types for exporting and importing data.

✒ Text files - Text files are simple files that store data as plain text. They can be used to store unstructured data or semi-structured data in a human-readable format e.g., TXT (Plain Text).

✒ Binary files - Binary files are files that store data in binary format. They are used for storing complex data structures or binary data such as images, audio, and video.

✒ PDF (Portable Document Format) - PDF files are used for storing and sharing documents in a fixed layout format. They can be used for ETL processes where data is extracted from PDF files.
</div>
<hr>

**Data based on their structure:**

📝 Structured data is data that has a rigid structure and can be organized neatly into rows and columns. This is the data that you see typically in spreadsheets and databases, for example.

📝 Semi-structured data is a mix of data that has consistent characteristics but doesn’t conform to a rigid structure. For example, emails. An email has a mix of structured data, such as the name of the sender and recipient, but also has the contents of the email, which is unstructured data, other examples include XML and JSON.

📝 Unstructured data is mostly qualitative information that is impossible to reduce to rows and columns. For example, photos, videos, text files, PDFs, and social media content.

<hr>

**Data based on sources:**

🛢 Relational databases, organizations use relational databases such as SQL Server, PostgreSQL, MySQL, and IBM DB2, to store data in a structured way, helping them in managing their day-to-day business activities, customer transactions, human resource activities, and their workflows.

🗃 Financial data or Weather data are made available as Flat files, Spread sheets, XML etc. Flat files store data in plain text format, with one record or row per line, and each value separated by delimiters such as commas, semi-colons, or tabs.

🔐 Many data providers and websites provide APIs, or Application Program Interfaces, and Web Services, which multiple users or applications can interact with and obtain data for processing or analysis. Some popular examples of APIs being used as a data source for data analytics: Twitter and Facebook APIs, Stock Market APIs.

🔍 Web Scraping is used to extract relevant data from websites. Also known as screen scraping or web data extraction, web scraping makes it possible to download specific data from web pages based on defined parameters. Some of the popular web scraping tools include BeautifulSoup, Scrapy, Pandas, and Selenium.

⛓ Data streams are another widely used source for aggregating constant streams of data flowing from sources such as instruments, IoT devices, and applications, GPS data from cars, computer programs, websites, and social media posts. This data is generally timestamped and also geo-tagged for geographical identification. Some of the data streams and ways in which they can be leveraged include: stock and market tickers for financial trading; retail transaction streams for predicting demand and supply chain management; surveillance and video feeds for threat detection; social media feeds for sentiment analysis; sensor data feeds for monitoring industrial or farming machinery; web click feeds for monitoring web performance and improving design; and real-time flight events for rebooking and rescheduling.

#100DaysOfDataEngineering #DataEngineering #Data
