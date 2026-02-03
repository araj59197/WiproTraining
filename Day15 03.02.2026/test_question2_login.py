# test_question2_login.py
# Generated from Selenium IDE - Question 2 Login Test
# Date: 03.02.2026

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class TestLoginAutomation:
    """
    Question 2 - Selenium IDE Export
    Test case that:
    1. Opens browser and navigates to login page
    2. Enters username and password
    3. Clicks login button
    4. Validates successful login message
    """
    
    def setup_method(self, method):
        """Setup method to initialize the WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.vars = {}
    
    def teardown_method(self, method):
        """Teardown method to close the browser"""
        time.sleep(2)
        self.driver.quit()
    
    def test_login_valid_credentials(self):
        """Test case: Login with valid credentials"""
        
        # Step 1: Open browser and navigate to login page
        print("Step 1: Opening browser and navigating to login page...")
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.driver.set_window_size(1920, 1080)
        
        # Step 2: Enter username and password
        print("Step 2: Entering username and password...")
        
        # Wait for username field to be clickable
        wait = WebDriverWait(self.driver, 10)
        username_field = wait.until(
            EC.element_to_be_clickable((By.NAME, "username"))
        )
        username_field.click()
        username_field.send_keys("Admin")
        
        # Enter password
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.click()
        password_field.send_keys("admin123")
        
        # Step 3: Click login button
        print("Step 3: Clicking login button...")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Step 4: Validate successful login message
        print("Step 4: Validating successful login...")
        
        # Wait for dashboard to load
        dashboard_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module")
            )
        )
        
        # Verify Dashboard text is present
        assert dashboard_element.text == "Dashboard", f"Expected 'Dashboard' but got '{dashboard_element.text}'"
        print("✓ Login successful! Dashboard page loaded.")
        
        # Additional verification - check URL
        assert "dashboard" in self.driver.current_url.lower(), "Dashboard URL not found"
        print("✓ URL validation successful!")
        
        time.sleep(2)


# For direct execution without pytest
if __name__ == "__main__":
    print("="*60)
    print("Question 2 - Selenium IDE Export to Python WebDriver")
    print("="*60)
    
    test = TestLoginAutomation()
    test.setup_method(None)
    
    try:
        test.test_login_valid_credentials()
        print("\n" + "="*60)
        print("TEST PASSED ✓")
        print("="*60)
    except Exception as e:
        print("\n" + "="*60)
        print(f"TEST FAILED ✗: {str(e)}")
        print("="*60)
    finally:
        test.teardown_method(None)
