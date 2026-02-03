"""
Lab 4 - TutorialsNinja E-Commerce Test Suite
URL: https://tutorialsninja.com/demo/

Test Steps:
1. Open the URL on Firefox
2. Verify title of the page
3. Go to 'Desktops' tab
4. Click on 'Mac'
5. Verify the 'Mac' heading
6. Select 'Name(A-Z)' from the 'Sort By' dropdown
7. Click on 'Add to Cart' button
8. Enter 'Monitors' in 'Search' text box and click on 'Search' button
9. Wait for page to load
10. Clear the text from 'Search Criteria' text box
11. Click on 'Search in product descriptions' check box and click on 'Search' button
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys


class TestTc004():
    """Test Case 004 - TutorialsNinja Product Search and Cart"""
    
    def setup_method(self, method):
        """Setup - Initialize Firefox browser"""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.vars = {}
    
    def teardown_method(self, method):
        """Teardown - Close the browser"""
        self.driver.quit()
    
    def test_tc004_product_search_and_cart(self):
        """
        Test Case: Product navigation, add to cart, and search functionality
        """
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        
        # Step 1: Open the URL
        print("Step 1: Opening TutorialsNinja demo site...")
        driver.get("https://tutorialsninja.com/demo/")
        
        # Step 2: Verify title of the page
        print("Step 2: Verifying page title...")
        assert "Your Store" in driver.title, f"Expected 'Your Store' in title, got: {driver.title}"
        print(f"Page Title: {driver.title}")
        
        # Step 3: Go to 'Desktops' tab
        print("Step 3: Clicking on Desktops tab...")
        driver.find_element(By.LINK_TEXT, "Desktops").click()
        time.sleep(1)
        
        # Step 4: Click on 'Mac'
        print("Step 4: Clicking on Mac category...")
        driver.find_element(By.LINK_TEXT, "Mac (1)").click()
        wait.until(EC.presence_of_element_located((By.ID, "content")))
        
        # Step 5: Verify the 'Mac' heading
        print("Step 5: Verifying 'Mac' heading...")
        heading = driver.find_element(By.TAG_NAME, "h2")
        assert "Mac" in heading.text, f"Expected 'Mac' in heading, got: {heading.text}"
        print(f"Heading verified: {heading.text}")
        
        # Step 6: Select 'Name(A-Z)' from the 'Sort By' dropdown
        print("Step 6: Selecting 'Name (A-Z)' from Sort By dropdown...")
        sort_dropdown = driver.find_element(By.ID, "input-sort")
        sort_dropdown.click()
        sort_dropdown.find_element(By.XPATH, "//option[. = 'Name (A - Z)']").click()
        time.sleep(2)
        
        # Step 7: Click on product and Add to Cart
        print("Step 7: Clicking on product and Add to Cart...")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".image .img-responsive")))
        driver.find_element(By.CSS_SELECTOR, ".image .img-responsive").click()
        time.sleep(2)
        
        wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
        driver.find_element(By.ID, "button-cart").click()
        time.sleep(2)
        
        # Step 8: Enter 'Monitors' in 'Search' text box and click on 'Search' button
        print("Step 8: Searching for 'Monitors'...")
        search_box = driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys("Monitors")
        driver.find_element(By.CSS_SELECTOR, ".fa-search").click()
        
        # Step 9: Wait for page to load
        print("Step 9: Waiting for search results page...")
        wait.until(EC.presence_of_element_located((By.ID, "content")))
        time.sleep(2)
        
        # Step 10: Clear the text from 'Search Criteria' text box
        print("Step 10: Clearing search criteria text box...")
        search_criteria = wait.until(EC.presence_of_element_located((By.ID, "input-search")))
        search_criteria.clear()
        
        # Step 11: Click on 'Search in product descriptions' check box and click on 'Search' button
        print("Step 11: Clicking 'Search in product descriptions' checkbox and Search button...")
        description_checkbox = driver.find_element(By.ID, "description")
        if not description_checkbox.is_selected():
            description_checkbox.click()
        
        # Enter search term and click search
        search_criteria.send_keys("Monitors")
        driver.find_element(By.ID, "button-search").click()
        
        # Wait for results
        wait.until(EC.presence_of_element_located((By.ID, "content")))
        time.sleep(2)
        
        print("Test completed successfully!")


class TestTc004Duplicate():
    """Test Case 004 Duplicate - Same flow for test suite"""
    
    def setup_method(self, method):
        """Setup - Initialize Firefox browser"""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.vars = {}
    
    def teardown_method(self, method):
        """Teardown - Close the browser"""
        self.driver.quit()
    
    def test_tc004_duplicate_flow(self):
        """
        Test Case: Duplicate test with same flow for suite
        """
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        
        # Step 1: Open the URL
        driver.get("https://tutorialsninja.com/demo/")
        
        # Step 2: Verify title
        assert "Your Store" in driver.title
        
        # Step 3: Go to 'Desktops' tab
        driver.find_element(By.LINK_TEXT, "Desktops").click()
        time.sleep(1)
        
        # Step 4: Click on 'Mac'
        driver.find_element(By.LINK_TEXT, "Mac (1)").click()
        wait.until(EC.presence_of_element_located((By.ID, "content")))
        
        # Step 5: Verify the 'Mac' heading
        heading = driver.find_element(By.TAG_NAME, "h2")
        assert "Mac" in heading.text
        
        # Step 6: Select 'Name(A-Z)' from dropdown
        sort_dropdown = driver.find_element(By.ID, "input-sort")
        sort_dropdown.click()
        sort_dropdown.find_element(By.XPATH, "//option[. = 'Name (A - Z)']").click()
        time.sleep(2)
        
        # Step 7: Add to Cart
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".image .img-responsive")))
        driver.find_element(By.CSS_SELECTOR, ".image .img-responsive").click()
        time.sleep(2)
        
        wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
        driver.find_element(By.ID, "button-cart").click()
        time.sleep(2)
        
        # Step 8: Search for 'Monitors'
        search_box = driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys("Monitors")
        driver.find_element(By.CSS_SELECTOR, ".fa-search").click()
        
        # Step 9: Wait for page
        wait.until(EC.presence_of_element_located((By.ID, "content")))
        time.sleep(2)
        
        # Step 10: Clear search criteria
        search_criteria = wait.until(EC.presence_of_element_located((By.ID, "input-search")))
        search_criteria.clear()
        
        # Step 11: Search with description checkbox
        description_checkbox = driver.find_element(By.ID, "description")
        if not description_checkbox.is_selected():
            description_checkbox.click()
        
        search_criteria.send_keys("Monitors")
        driver.find_element(By.ID, "button-search").click()
        
        wait.until(EC.presence_of_element_located((By.ID, "content")))
        
        print("Duplicate test completed successfully!")


# Test Suite - Run with: pytest test_tc004.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

