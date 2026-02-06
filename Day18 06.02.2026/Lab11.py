"""
Lab 11: Advanced Selenium - Page Object Model and Page Factory
Goal: Learning how to use page object model and page factory to make test maintenance easy
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# ========== Page Object Model Classes ==========

class OrangeHRMLoginPage:
    """Page Object for OrangeHRM Login Page - Contains locators and methods"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    # Locators (Page Elements)
    username_locator = (By.NAME, "username")
    password_locator = (By.NAME, "password")
    login_button_locator = (By.XPATH, "//button[@type='submit']")
    dashboard_header_locator = (By.XPATH, "//h6[text()='Dashboard']")
    
    # Page Actions/Methods
    def enter_username(self, username):
        """Enter username in the username field"""
        self.wait.until(EC.presence_of_element_located(self.username_locator))
        self.driver.find_element(*self.username_locator).clear()
        self.driver.find_element(*self.username_locator).send_keys(username)
        print(f"✓ Entered username: {username}")
    
    def enter_password(self, password):
        """Enter password in the password field"""
        self.driver.find_element(*self.password_locator).clear()
        self.driver.find_element(*self.password_locator).send_keys(password)
        print(f"✓ Entered password: {'*' * len(password)}")
    
    def click_login_button(self):
        """Click the login button"""
        self.driver.find_element(*self.login_button_locator).click()
        print("✓ Clicked login button")
    
    def verify_login_successful(self):
        """Verify that login was successful by checking for Dashboard header"""
        try:
            self.wait.until(EC.presence_of_element_located(self.dashboard_header_locator))
            print("✓ Login successful - Dashboard is visible")
            return True
        except:
            print("✗ Login failed - Dashboard not found")
            return False
    
    def perform_login(self, username, password):
        """Complete login flow - Enter credentials and click login"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()


class OrangeHRMDashboardPage:
    """Page Object for OrangeHRM Dashboard Page"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    # Locators
    dashboard_header_locator = (By.XPATH, "//h6[text()='Dashboard']")
    user_dropdown_locator = (By.CLASS_NAME, "oxd-userdropdown-tab")
    logout_link_locator = (By.XPATH, "//a[text()='Logout']")
    
    # Page Actions
    def get_dashboard_title(self):
        """Get the dashboard page title"""
        element = self.wait.until(EC.presence_of_element_located(self.dashboard_header_locator))
        return element.text
    
    def click_user_dropdown(self):
        """Click on user dropdown menu"""
        self.wait.until(EC.element_to_be_clickable(self.user_dropdown_locator))
        self.driver.find_element(*self.user_dropdown_locator).click()
        print("✓ Clicked user dropdown")
    
    def click_logout(self):
        """Click logout link"""
        self.wait.until(EC.element_to_be_clickable(self.logout_link_locator))
        self.driver.find_element(*self.logout_link_locator).click()
        print("✓ Clicked logout")
    
    def perform_logout(self):
        """Complete logout flow"""
        self.click_user_dropdown()
        time.sleep(1)  # Small wait for dropdown animation
        self.click_logout()


# ========== Test Case Class ==========

class TestOrangeHRMLogin:
    """Test cases for OrangeHRM Login functionality using Page Object Model"""
    
    def __init__(self):
        self.driver = None
        self.login_page = None
        self.dashboard_page = None
    
    def setup(self):
        """Setup test - Initialize driver and page objects"""
        print("\n" + "="*60)
        print("Setting up test environment...")
        print("="*60)
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        
        # Initialize Page Objects
        self.login_page = OrangeHRMLoginPage(self.driver)
        self.dashboard_page = OrangeHRMDashboardPage(self.driver)
        
        # Navigate to login page
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        print("✓ Navigated to OrangeHRM login page")
        print("✓ Test setup complete\n")
    
    def teardown(self):
        """Teardown test - Close browser"""
        print("\n" + "="*60)
        print("Tearing down test environment...")
        print("="*60)
        time.sleep(2)  # Wait to see results
        if self.driver:
            self.driver.quit()
            print("✓ Browser closed")
        print("✓ Test teardown complete")
        print("="*60 + "\n")
    
    def test_valid_login(self):
        """Test Case 1: Login with valid credentials"""
        print("\n[TEST CASE 1: Valid Login]")
        print("-" * 60)
        
        # Test data
        username = "Admin"
        password = "admin123"
        
        # Perform login
        self.login_page.perform_login(username, password)
        
        # Verify login
        time.sleep(2)  # Wait for page load
        is_logged_in = self.login_page.verify_login_successful()
        
        if is_logged_in:
            dashboard_title = self.dashboard_page.get_dashboard_title()
            print(f"✓ Dashboard title: {dashboard_title}")
            print("✓ TEST PASSED: Valid login successful")
        else:
            print("✗ TEST FAILED: Login was not successful")
        
        print("-" * 60)
        return is_logged_in
    
    def test_valid_login_and_logout(self):
        """Test Case 2: Login with valid credentials and logout"""
        print("\n[TEST CASE 2: Valid Login and Logout]")
        print("-" * 60)
        
        # Test data
        username = "Admin"
        password = "admin123"
        
        # Perform login
        self.login_page.perform_login(username, password)
        
        # Verify login
        time.sleep(2)
        is_logged_in = self.login_page.verify_login_successful()
        
        if is_logged_in:
            print("✓ Login successful")
            
            # Perform logout
            time.sleep(2)
            self.dashboard_page.perform_logout()
            
            # Verify logout (check if we're back at login page)
            time.sleep(2)
            current_url = self.driver.current_url
            if "auth/login" in current_url:
                print("✓ Logout successful - Redirected to login page")
                print("✓ TEST PASSED: Login and logout successful")
                print("-" * 60)
                return True
            else:
                print("✗ Logout failed - Not at login page")
                print("✗ TEST FAILED")
                print("-" * 60)
                return False
        else:
            print("✗ TEST FAILED: Login was not successful")
            print("-" * 60)
            return False


# ========== Main Execution ==========

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LAB 11: ADVANCED SELENIUM - PAGE OBJECT MODEL")
    print("="*60)
    
    # Create test instance
    test = TestOrangeHRMLogin()
    
    try:
        # Run Test Case 1: Valid Login
        test.setup()
        test.test_valid_login()
        test.teardown()
        
        # Run Test Case 2: Valid Login and Logout
        print("\n" + "="*60)
        print("STARTING NEW TEST")
        print("="*60)
        test.setup()
        test.test_valid_login_and_logout()
        test.teardown()
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        if test.driver:
            test.teardown()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)
