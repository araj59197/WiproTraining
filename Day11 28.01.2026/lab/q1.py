"""
Selenium Test - Google Search
Lab Exercise: Enter text on web page and submit with assertions
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time

def test_google_search():
    """
    Test case to perform a Google search and verify results
    """
    # Initialize Edge WebDriver
    driver = webdriver.Edge()
    
    try:
        # Step 1: Navigate to Google
        print("Step 1: Opening Google...")
        driver.get("https://www.google.com")
        driver.maximize_window()
        time.sleep(2)
        
        # Step 2: Find the search box by ID and enter text
        print("Step 2: Locating search box...")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        # Step 3: Enter search text
        search_text = "Selenium WebDriver"
        print(f"Step 3: Entering text: '{search_text}'")
        search_box.clear()
        search_box.send_keys(search_text)
        time.sleep(1)
        
        # Step 4: Submit the search
        print("Step 4: Submitting search...")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # Step 5: Add assertions to verify search results
        print("Step 5: Verifying search results...")
        
        # Assertion 1: Verify page title contains search text (or verify URL)
        # Note: Sometimes Google uses URL instead of title
        page_title = driver.title
        current_url = driver.current_url
        
        title_check = search_text.lower().replace(" ", "") in page_title.lower().replace(" ", "")
        url_check = "selenium" in current_url.lower()
        
        assert title_check or url_check, \
            f"Expected '{search_text}' in title or URL. Title: {page_title}, URL: {current_url}"
        print(f"✓ Assertion 1 PASSED: Search term found in page (Title: {page_title[:50]}...)")
        
        # Assertion 2: Verify search results are displayed
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        assert results is not None, "Search results not found"
        print("✓ Assertion 2 PASSED: Search results are displayed")
        
        # Assertion 3: Verify URL contains search query
        assert "search?q=" in driver.current_url, \
            f"Expected 'search?q=' in URL, but got: {driver.current_url}"
        print("✓ Assertion 3 PASSED: URL contains search query")
        
        # Assertion 4: Verify at least one result is present
        result_divs = driver.find_elements(By.CSS_SELECTOR, "div.g")
        assert len(result_divs) > 0, "No search results found on the page"
        print(f"✓ Assertion 4 PASSED: Found {len(result_divs)} search results")
        
        print("\n" + "="*50)
        print("ALL TESTS PASSED SUCCESSFULLY! ✓")
        print("="*50)
        
        # Wait to see the results
        time.sleep(3)
        
    except AssertionError as e:
        print(f"\n✗ ASSERTION FAILED: {e}")
        raise
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise
        
    finally:
        # Step 6: Close the browser
        print("\nClosing browser...")
        driver.quit()
        print("Browser closed successfully!")

if __name__ == "__main__":
    print("="*50)
    print("Google Search Test with Assertions")
    print("="*50 + "\n")
    
    test_google_search()