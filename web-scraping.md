from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Initialize WebDriver
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Path to ChromeDriver

# Open the Neo4j Browser
driver.get("http://localhost:7474")  # Adjust URL if Neo4j is hosted elsewhere

# Give it time to load
time.sleep(5)

# Find the Cypher input area (this might change depending on the Neo4j version)
cypher_input = driver.find_element("xpath", '//textarea[contains(@class, "cypher-input")]')

# Type your Cypher query
cypher_input.send_keys("MATCH (n) RETURN n LIMIT 10")

# Execute the query by sending the Enter key
cypher_input.send_keys(Keys.RETURN)

# Wait for the query to execute and results to appear
time.sleep(5)

# Optionally, you can scrape the result if needed
results = driver.find_elements("xpath", "//div[contains(@class, 'result-cell')]")
for result in results:
    print(result.text)

# Close the browser
driver.quit()
