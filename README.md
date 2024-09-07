# VerveBridge_WebScraping_Task

Research Report for Web Scraping Project

Project Overview
The goal of this project was to build a web scraper to extract product details from Flipkart, a leading e-commerce platform. Using Selenium and BeautifulSoup, we navigated multiple product categories (e.g., Laptops, Gaming Laptops, Mobiles), extracted relevant data, and stored the information in structured formats like CSV and JSON. The extracted data includes product name, price, rating, number of reviews, and product links.

Summary of Web Scraping Techniques:

Selenium:
Web Navigation: Selenium was used to dynamically interact with the website, navigate between pages, and handle JavaScript-rendered content. Flipkart’s pages often load content dynamically via AJAX, which requires rendering the full page before extracting data.
Handling Timeouts: To deal with potential loading issues, the scraper included a retry mechanism for pages that did not load within a specified time, with an exponential backoff strategy to handle server delays.
Headless Browser: The Chrome browser was run in headless mode to increase efficiency by avoiding the overhead of graphical interface rendering.

BeautifulSoup:
HTML Parsing: After Selenium fetched the page content, BeautifulSoup was used for parsing the static HTML. It allowed efficient extraction of product data using CSS class selectors and structured HTML tags.
Error Handling: The scraper employed error handling techniques to ensure that even if some elements were missing (e.g., ratings or reviews), the extraction would continue for the remaining elements.

Randomized Delays:
To avoid detection and to mimic human browsing behavior, random delays between requests were implemented using Python’s random.uniform() function. This helps in bypassing potential anti-bot measures that may block scraping attempts due to unusual request patterns.

Data Storage:
CSV and JSON formats were used to store the extracted product data. This provided flexibility for further analysis, as these formats are widely used for data exchange and visualization.
Pandas: Used for managing and exporting the extracted data into structured CSV and JSON formats, ensuring consistent data storage.

Flipkart’s Website Structure

Flipkart’s product pages follow a fairly consistent layout, which made the scraping process straightforward once the appropriate CSS selectors were identified. However, there were challenges due to AJAX-based loading, and dynamic page content generation.


Dynamic Content: Product data such as pricing, reviews, and ratings are dynamically loaded as users scroll through the page, requiring Selenium to wait until all elements are fully loaded before parsing.
Classes and Attributes: The product listings on Flipkart use unique class attributes for essential elements:
Product Name: KzDlHZ
Price: Nx9bqj _4b5DiR
Rating: XQDdHH
Number of Reviews: Wphh3N
Product Link: CGtC98
Pagination: Product categories are divided into multiple pages, with URLs containing a page number parameter. The scraper was designed to iterate through these pages until no more products were found.
Challenges
AJAX Requests: The scraper had to wait for elements to load due to the heavy use of JavaScript and AJAX on the site.
Anti-Scraping Measures: Randomized delays and retries were employed to avoid being blocked by anti-bot systems.
Content Structure Changes: Flipkart occasionally updates its website structure, which may cause scraping scripts to break. Error handling was implemented to mitigate such issues.


Design Documents
Flowchart
Below is the high-level flowchart for the web scraping process:
           +----------------------+
           | Start Scraping Process|
           +----------------------+
                     |
                     v
          +-------------------------+
          | Fetch Category Page URL  |
          +-------------------------+
                     |
                     v
        +------------------------------+
        | Load Page Using Selenium      |
        +------------------------------+
                     |
                     v
         +----------------------------------+
         | Parse Product Data using BeautifulSoup|
         +----------------------------------+
                     |
                     v
        +---------------------------------------+
        | Store Data (Name, Price, Rating, Reviews) |
        +---------------------------------------+
                     |
                     v
        +------------------------------+
        | Go to Next Page (if exists)   |
        +------------------------------+
                     |
                     v
        +------------------------+
        | End of Category?        |
        +------------------------+
                     |           |
                 Yes |           | No
                     v           v
        +------------------+  +------------------+
        | End Process       |  | Next Category    |
        +------------------+  +------------------+

Data Points Extracted
The following are the key data points extracted from each product:

Category: The category from which the product was scraped (e.g., Laptop, Gaming Laptop, Mobiles).
Product Name: The name of the product as displayed on Flipkart.
Price: The price of the product.
Rating: The average rating given by customers (if available).
Number of Reviews: The number of customer reviews.
Product Link: The direct URL to the product’s page.
Category URL: The URL of the category page the product belongs to (for traceability).
Design Decisions
Choice of Libraries:

Selenium was chosen because of its ability to handle dynamic content and JavaScript, which was essential for navigating Flipkart’s pages.
BeautifulSoup was used for its simplicity and efficiency in parsing static HTML after Selenium had rendered the dynamic content.
Exponential Backoff for Retries:

To handle timeouts or temporary failures when loading pages, an exponential backoff strategy was employed. This reduces the load on the server and increases the chance of successful retries.

Random Delays:
Implementing randomized delays between page requests helped avoid detection and minimized the risk of getting blocked by Flipkart’s anti-scraping mechanisms.

Headless Browsing:
The use of a headless browser (Chrome in headless mode) reduced the system’s resource consumption, allowing for faster scraping without the need to render the browser’s GUI.

Conclusion
This web scraping project efficiently extracted product data from Flipkart using a combination of Selenium for dynamic page interaction and BeautifulSoup for HTML parsing. The project overcame several challenges, such as handling AJAX-based dynamic content, implementing retries for timeouts, and using random delays to avoid detection. The extracted data can now be used for further analysis, research, or integration into other applications.
