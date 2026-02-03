"""
Question 1 – Selenium WebDriver Basics

Write a Selenium WebDriver script that:
1. Opens a Chrome or Firefox browser
2. Navigates to https://example.com
3. Prints the page title and URL
4. Closes the browser
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def test_selenium_basics():
    # Configure Chrome options (optional)
    chrome_options = Options()
    # Uncomment the line below to run in headless mode
    # chrome_options.add_argument('--headless')
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Alternative: Use Firefox instead
    # driver = webdriver.Firefox()
    
    try:
        # Navigate to the website
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        
        # Print the page title
        print(f"Page Title: {driver.title}")
        
        # Print the current URL
        print(f"Current URL: {driver.current_url}")
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    test_selenium_basics()
