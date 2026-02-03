"""
Selenium Test - OrangeHRM Login Test
Question 2: Login Test with Valid Credentials
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service


class TestQuestion2Login:
    """Test class for OrangeHRM login functionality"""
    
    def setup_method(self, method):
        """Setup method - runs before each test"""
        # Initialize Edge WebDriver (change to Chrome if needed)
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.vars = {}
    
    def teardown_method(self, method):
        """Teardown method - runs after each test"""
        self.driver.quit()
    
    def test_login_valid_credentials(self):
        """
        Test Case: Login with valid credentials
        Steps:
        1. Open OrangeHRM login page
        2. Set window size
        3. Click on username field
        4. TYPE (not typo!) username: Admin
        5. Click on password field
        6. Type password: admin123
        7. Click submit button
        8. Wait for Dashboard element
        9. Assert Dashboard text is displayed
        """
        
        # Step 1: Open the login page
        print("Step 1: Opening OrangeHRM login page...")
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        
        # Step 2: Set window size
        print("Step 2: Setting window size...")
        self.driver.set_window_size(1920, 1080)
        time.sleep(2)  # Wait for page to load
        
        # Step 3 & 4: Click and TYPE username (FIXED: was 'typo', now 'type')
        print("Step 3-4: Entering username...")
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.click()
        username_field.send_keys("Admin")  # This is the TYPE command (not typo!)
        
        # Step 5 & 6: Click and type password
        print("Step 5-6: Entering password...")
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.click()
        password_field.send_keys("admin123")
        
        # Step 7: Click submit button
        print("Step 7: Clicking submit button...")
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        submit_button.click()
        
        # Step 8: Wait for Dashboard element to be present
        print("Step 8: Waiting for Dashboard to load...")
        dashboard_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".oxd-text.oxd-text--h6.oxd-topbar-header-breadcrumb-module")
            )
        )
        
        # Step 9: Assert Dashboard text
        print("Step 9: Verifying Dashboard text...")
        assert dashboard_element.text == "Dashboard", \
            f"Expected 'Dashboard' but got '{dashboard_element.text}'"
        
        print("\n" + "="*50)
        print("✓ LOGIN TEST PASSED! Successfully logged in!")
        print("="*50)
        
        # Wait to see the result
        time.sleep(3)


# Standalone execution function
def run_test():
    """Run the test standalone"""
    test_instance = TestQuestion2Login()
    test_instance.setup_method(None)
    
    try:
        test_instance.test_login_valid_credentials()
        print("\nTest execution completed successfully!")
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        raise
    finally:
        test_instance.teardown_method(None)


if __name__ == "__main__":
    print("="*50)
    print("OrangeHRM Login Test - Valid Credentials")
    print("="*50 + "\n")
    
    run_test()
