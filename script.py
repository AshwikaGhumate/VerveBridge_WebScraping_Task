import time
import pandas as pd
import logging
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configuring logging
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuring Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

# Path to the chromedriver
service = Service('C:\\Users\\Ramesh\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')  
driver = webdriver.Chrome(service=service, options=chrome_options)

MAX_RETRIES = 3  # Set a maximum number of retries

def scrape_all_products(category_name, category_url):
    all_products = []  # Initializing an empty list to store all product details
    page_number = 1  # Start from the first page
    retries = 0  # Initializing retry counter
    
    while True:  # Loop through pages until there are no more products
        url = f"{category_url}&page={page_number}"  # Constructing URL for each page of the category
        try:
            start_time = time.time()  # Recording the start time for the current page load
            driver.get(url)  # Loading the category page using Selenium
            
            # Wait until products are loaded
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'tUxRFH'))  # Wait until product elements are present
            )
        except TimeoutException:
            logging.error(f"Timeout while trying to retrieve page {page_number}. Retrying...")
            retries += 1  # Incrementing the retry counter
            if retries > MAX_RETRIES:  # If the max number of retries is reached
                logging.error(f"Max retries reached for {url}. Skipping this page.")
                break  # Exit the loop for this category
            time.sleep(2 ** retries)  # Exponential backoff delay before retrying
            continue  # Retry the current page
        
        time.sleep(random.uniform(3, 7))  # Random wait to mimic human behavior

        # Using BeautifulSoup to parse the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parse the page source with BeautifulSoup
        products = soup.find_all('div', class_='tUxRFH')  # Find all product elements
        
        if not products:  # If no products are found, exit the loop
            logging.info(f"No more products found on page {page_number}.")
            break
        
        for product in products:
            try:
                # Using try-except for each field in case of structure changes
                name = product.find('div', class_='KzDlHZ').text if product.find('div', class_='KzDlHZ') else 'N/A'
                price = product.find('div', class_='Nx9bqj _4b5DiR').text if product.find('div', class_='Nx9bqj _4b5DiR') else 'N/A'
                rating = product.find('div', class_='XQDdHH').text if product.find('div', class_='XQDdHH') else 'N/A'
                num_reviews = product.find('span', class_='Wphh3N').text if product.find('span', class_='Wphh3N') else 'N/A'
                product_link = "https://www.flipkart.com" + product.find('a', class_='CGtC98')['href'] if product.find('a', class_='CGtC98') else 'N/A'

                all_products.append({
                    'Category': category_name,
                    'Name': name,
                    'Price': price,
                    'Rating': rating,
                    'Number of Reviews': num_reviews,
                    'Product Link': product_link,
                    'Category URL': category_url
                })
            except AttributeError as e:
                logging.warning(f"Error extracting product data: {e}")
                continue  # Skip products with missing elements
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Scraped page {page_number} of {category_name} in {elapsed_time:.2f} seconds.")
        
        page_number += 1  # Move to the next page
        time.sleep(random.uniform(10, 20))  # Additional pause to avoid overwhelming the server
    
    return all_products  # Return the list of all products for this category

def main():
    """
    Main function to scrape all product categories and save the results to a CSV file.
    """
    categories = [
        ("Laptop", "https://www.flipkart.com/6bo/b5g/~cs-rmq98biaq5/pr?sid=6bo%2Cb5g&collection-tab-name=Core+i5&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIkNvcmUgaTUgTGFwdG9wcyJdLCJ2YWx1ZVR5cGUiOiJNVUxUSV9WQUxVRUQifX19fX0%3D&wid=2.productCard.PMU_V2_2"),
        ("Gaming-Laptop", "https://www.flipkart.com/gaming/gaming-laptops/pr?sid=4rr,tz1&otracker=categorytree"),
        ("Mobiles", "https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DMOTOROLA&param=19873&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIk1vdG9yb2xhIHNtYXJ0cGhvbmVzIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fX19fQ%3D%3D&wid=58.productCard.PMU_V2_21"),
    ]

    all_product_data = []  # Initializing an empty list to store data from all categories

    for category_name, category_url in categories:
        logging.info(f"Starting to scrape category: {category_name}")
        try:
            category_products = scrape_all_products(category_name, category_url)  # Scrape the category
            all_product_data.extend(category_products)  # Append the category's products to the master list
            logging.info(f"Completed scraping category: {category_name}")
        except Exception as e:
            logging.error(f"Error scraping category {category_name}: {e}")  # Logging any errors encountered during scraping

    # Converting the list of products to a DataFrame and save as CSV and JSON
    df = pd.DataFrame(all_product_data)
    df.to_csv('flipkart_all_products.csv', index=False)
    df.to_json('flipkart_product_details.json', orient='records')
    logging.info(f"Scraping complete. Total products scraped: {len(all_product_data)}")

    # Clean up
    driver.quit()  # Quit the browser after scraping is done

if __name__ == "__main__":
    main()  # Run the main function when the script is executed








