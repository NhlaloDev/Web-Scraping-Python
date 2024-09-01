from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import xml.etree.ElementTree as ET
import time


# Set up the web driver (change the path to where your ChromeDriver is located)
driver_path = 'chromedriver.exe'  # Make sure to have the correct path for your environment
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Open the webpage
url = 'https://www.listcorp.com/jse/sectors/consumer-services'
driver.get(url)

# Wait for the page to load
time.sleep(20)  # Increase if necessary depending on your internet speed

# Initialize a list to store the data
data = []


# Locate the table rows containing the data
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

# Loop through the rows and extract the desired information
for row in rows:
    item = {}
    item['Code'] = row.find_element(By.XPATH, ".//td[1]").text
    item['Company'] = row.find_element(By.XPATH, ".//td[2]").text
    item['Market Cap'] = row.find_element(By.XPATH, ".//td[3]").text
    item['Share Price'] = row.find_element(By.XPATH, ".//td[4]").text
    item['% Change'] = row.find_element(By.XPATH, ".//td[5]").text

    data.append(item)


# Close the web driver
driver.quit()

# Save data to CSV
df = pd.DataFrame(data)
df.to_csv('Consumer_services.csv', index=False)

# Save data to XML
root = ET.Element("Companies")

for item in data:
    company_elem = ET.SubElement(root, "Company")
    
    code_elem = ET.SubElement(company_elem, "Code")
    code_elem.text = item['Code']
    
    name_elem = ET.SubElement(company_elem, "Name")
    name_elem.text = item['Company']
    
    market_cap_elem = ET.SubElement(company_elem, "MarketCap")
    market_cap_elem.text = item['Market Cap']
    
    share_price_elem = ET.SubElement(company_elem, "SharePrice")
    share_price_elem.text = item['Share Price']
    
    change_elem = ET.SubElement(company_elem, "PercentageChange")
    change_elem.text = item['% Change']

tree = ET.ElementTree(root)
tree.write("Consumer_services.xml")

print("Data has been saved to 'Consumer_services.csv' and 'Consumer_services.xml'.")
