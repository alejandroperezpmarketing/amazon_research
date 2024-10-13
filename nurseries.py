from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from selenium.common.exceptions import NoSuchElementException
import json
from srapping.test import csv_file

# Set up Chrome options to avoid closing the browser unexpectedly
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

# Navigate to Google
driver.get('https://www.google.com')

# List to store all extracted links

# List to store all extracted links
all_links = {'SERP': [],
             'URLs': [],
             'URL_cleaned': []}


# Accept the cookie consent banner (if present)
try:
    aceptar_baner = driver.find_element(By.ID, 'L2AGLb')
    aceptar_baner.click()
except NoSuchElementException:
    print("No cookie consent banner found, continuing...")

# Perform a Google search
search_query = "venta de plantas viveros en la Comunidad Valenciana"
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)


def extract_urls():
    # Function to extract links from the current search result page

    search_results = driver.find_elements(By.CSS_SELECTOR, "a")
    for i, result in enumerate(search_results):
        href = result.get_attribute('href')
        if href:
            if '/url?q=' in href:
                cleaned_href = href.split('&')[0].replace('/url?q=', '')
                print(f'saving clead url n{i}...: {cleaned_href}')
                all_links['URL_cleaned'].append(cleaned_href)
                time.sleep(3)

            elif 'google.com' in href or 'googleadservices.com' in href:
                google_clead_href = href
                print(f'saving SERP result n{i}... : {google_clead_href}')
                all_links['SERP'].append(google_clead_href)
                time.sleep(3)

            else:
                print(f'saving general url n{i} ...: {href}')
                # print(href)
                all_links['URLs'].append(href)
                time.sleep(3)

            # google_href_results = href.split('/')[2]
            # print(google_href_results)


def go_to_the_next_page():

    # Try to find the 'Next' button and click it
    try:
        next_button = driver.find_element(By.ID, 'pnnext')
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
        return True
    except NoSuchElementException:
        print("No more pages found, exiting...")
        return False


csv_file = 'nurseries_urls'
page_num = 1
while True:
    print(f"Extracting links from page {page_num}...")
    extract_urls()
    go_to_the_next_page()

    if not go_to_the_next_page():
        with open(csv_file, 'w', encoding='UTF-8', newline=''):
            headers = ['SERP', 'URLs', 'URLs_cleaned']
            writer = csv.DictWriter(all_links, fieldnames=headers)
            writer.writeheader()

            n = 1
            for url in all_links['SERP']:
                writer.writerow({
                    'id': n,
                    'SERP': url,
                    'URLs': 'None',
                    'URLs_cleaned': 'None'})
                n += 1
            for url in all_links['URLs']:
                writer.writerow({
                    'id': n,
                    'SERP': 'None',
                    'URLs': url,
                    'URLs_cleaned': 'None'})
                n += 1

            for url in all_links['URL_cleaned']:
                writer.writerow({
                    'id': n,
                    'SERP': 'None',
                    'URLs': 'None',
                    'URLs_cleaned': url})
                n += 1

        break
""" 
with open(csv_file, mode='w', encoding='UTF-8', newline=''):
    headers = ['SERP', 'URLs', 'URLs_cleaned']
    writer = csv.DictWriter(all_links, fieldnames=headers)
    writer.writeheader()

    n = 1
    for url in all_links['SERP']:
            writer.writerow({
                'id': n,
                'SERP': url,
                'URLs': 'None',
                'URLs_cleaned': 'None'})
            n += 1
    for url in all_links['URLs']:
            writer.writerow({
                'id': n,
                'SERP': 'None',
                'URLs': url,
                'URLs_cleaned': 'None'})
            n += 1

    for url in all_links['URL_cleaned']:
            writer.writerow({
                'id': n,
                'SERP': 'None',
                'URLs': 'None',
                'URLs_cleaned': url})
            n += 1
    page_num += 1
    time.sleep(3)
 """
 
 
 

csv_file = 'output.csv'

with open(csv_file, mode='w', encoding='UTF-8', newline='') as file:
    # Adding 'id' to the headers list
    headers = ['id', 'SERP', 'URLs', 'URLs_cleaned']
    writer = csv.DictWriter(file, fieldnames=headers)

    # Write the header
    writer.writeheader()

    n = 1
    # Writing rows for SERP URLs
    for url in all_links['SERP']:
        writer.writerow({
            'id': n,
            'SERP': url,
            'URLs': 'None',
            'URLs_cleaned': 'None'
        })
        n += 1

    # Writing rows for general URLs
    for url in all_links['URLs']:
        writer.writerow({
            'id': n,
            'SERP': 'None',
            'URLs': url,
            'URLs_cleaned': 'None'
        })
        n += 1

    # Writing rows for cleaned URLs
    for url in all_links['URL_cleaned']:
        writer.writerow({
            'id': n,
            'SERP': 'None',
            'URLs': 'None',
            'URLs_cleaned': url
        })
        n += 1

    # Pause for demonstration purposes (you can remove this if not needed)
    time.sleep(3)

print(f"Data has been saved to {csv_file}")
print(json.dumps(all_links, indent=4))
driver.quit()
