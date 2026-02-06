"""
=============================================================================
DAY 18 - SELENIUM AUTOMATION WITH PAGE OBJECT MODEL (POM)
Tech Academy Submission - Complete Implementation
=============================================================================

This file contains:
1. Question 7 - Complete POM Framework (merged into single file)
2. Lab 11 - Page Object Model Implementation
3. All reusable methods (click, input, select, wait, etc.)
4. Multiple test cases using pytest

Author: Wipro Pre-Skilling Training
Date: 06-02-2026
=============================================================================
"""

# ========== IMPORTS ==========
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pytest


# =============================================================================
# SECTION 1: CONFIGURATION
# =============================================================================

class Config:
    """Configuration class for test framework"""
    
    # Browser Settings
    BROWSER = "firefox"  # Options: chrome, firefox, edge
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 10
    
    # Application URLs
    BASE_URL = "https://opensource-demo.orangehrmlive.com"
    LOGIN_URL = f"{BASE_URL}/web/index.php/auth/login"
    DASHBOARD_URL = f"{BASE_URL}/web/index.php/dashboard/index"
    
    # Test Credentials
    VALID_USERNAME = "Admin"
    VALID_PASSWORD = "admin123"
    INVALID_USERNAME = "InvalidUser"
    INVALID_PASSWORD = "InvalidPass"
    
    # Browser Options
    HEADLESS_MODE = False
    MAXIMIZE_WINDOW = True
    
    # Timeout Settings
    PAGE_LOAD_TIMEOUT = 30
    SCRIPT_TIMEOUT = 30


# =============================================================================
# SECTION 2: BASE PAGE WITH REUSABLE METHODS
# =============================================================================

class BasePage:
    """
    Base class for all page objects with reusable methods
    Contains common actions: click, input, select, wait, etc.
    """
    
    def __init__(self, driver):
        """Initialize BasePage with WebDriver instance"""
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    # ========== Navigation Methods ==========
    
    def open_url(self, url):
        """Navigate to a specific URL"""
        self.driver.get(url)
        print(f"Navigated to: {url}")
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get current page title"""
        return self.driver.title
    
    # ========== Wait Methods (REUSABLE) ==========
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present in DOM"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            print(f"Timeout: Element {locator} not found")
            return None
    
    def wait_for_element_clickable(self, locator, timeout=10):
        """Wait for element to be clickable"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            print(f"Timeout: Element not clickable")
            return None
    
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for element to be visible"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            print(f"Timeout: Element not visible")
            return None
    
    # ========== Click Method (REUSABLE) ==========
    
    def click(self, locator, element_name="element"):
        """
        REUSABLE CLICK METHOD
        Click on an element with error handling
        """
        try:
            element = self.wait_for_element_clickable(locator)
            if element:
                element.click()
                print(f"Clicked on {element_name}")
                return True
            return False
        except Exception as e:
            print(f"Failed to click on {element_name}: {str(e)}")
            return False
    
    # ========== Input Method (REUSABLE) ==========
    
    def input_text(self, locator, text, element_name="field"):
        """
        REUSABLE INPUT METHOD
        Enter text in an input field with clear and error handling
        """
        try:
            element = self.wait_for_element(locator)
            if element:
                element.clear()
                element.send_keys(text)
                print(f"Entered text in {element_name}: {text}")
                return True
            return False
        except Exception as e:
            print(f"Failed to enter text in {element_name}: {str(e)}")
            return False
    
    # ========== Select Methods (REUSABLE) ==========
    
    def select_by_visible_text(self, locator, text, element_name="dropdown"):
        """
        REUSABLE SELECT METHOD
        Select dropdown option by visible text
        """
        try:
            element = self.wait_for_element(locator)
            if element:
                select = Select(element)
                select.select_by_visible_text(text)
                print(f"Selected '{text}' from {element_name}")
                return True
            return False
        except Exception as e:
            print(f"Failed to select from {element_name}: {str(e)}")
            return False
    
    def select_by_value(self, locator, value, element_name="dropdown"):
        """Select dropdown option by value"""
        try:
            element = self.wait_for_element(locator)
            if element:
                select = Select(element)
                select.select_by_value(value)
                print(f"Selected value '{value}' from {element_name}")
                return True
            return False
        except Exception as e:
            print(f"Failed to select from {element_name}: {str(e)}")
            return False
    
    def select_by_index(self, locator, index, element_name="dropdown"):
        """Select dropdown option by index"""
        try:
            element = self.wait_for_element(locator)
            if element:
                select = Select(element)
                select.select_by_index(index)
                print(f"Selected index {index} from {element_name}")
                return True
            return False
        except Exception as e:
            print(f"✗ Failed to select from {element_name}: {str(e)}")
            return False
    
    # ========== Verification Methods ==========
    
    def is_element_present(self, locator):
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def is_element_enabled(self, locator):
        """Check if element is enabled"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_enabled()
        except NoSuchElementException:
            return False
    
    def get_text(self, locator, element_name="element"):
        """Get text from an element"""
        try:
            element = self.wait_for_element(locator)
            if element:
                text = element.text
                print(f"Retrieved text from {element_name}: {text}")
                return text
            return None
        except Exception as e:
            print(f"Failed to get text from {element_name}: {str(e)}")
            return None
    
    def get_attribute(self, locator, attribute_name, element_name="element"):
        """Get attribute value from an element"""
        try:
            element = self.wait_for_element(locator)
            if element:
                value = element.get_attribute(attribute_name)
                return value
            return None
        except Exception as e:
            print(f"Failed to get attribute: {str(e)}")
            return None
    
    # ========== Utility Methods ==========
    
    def scroll_to_element(self, locator):
        """Scroll to a specific element"""
        try:
            element = self.wait_for_element(locator)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                print(f"Scrolled to element")
                return True
            return False
        except Exception as e:
            print(f"Failed to scroll: {str(e)}")
            return False
    
    def take_screenshot(self, filename):
        """Take a screenshot"""
        try:
            self.driver.save_screenshot(filename)
            print(f"Screenshot saved: {filename}")
            return True
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
            return False
    
    def refresh_page(self):
        """Refresh the current page"""
        self.driver.refresh()
        print("Page refreshed")
    
    def sleep(self, seconds):
        """Wait for specified seconds"""
        time.sleep(seconds)


# =============================================================================
# SECTION 3: PAGE OBJECT CLASSES
# =============================================================================

class LoginPage(BasePage):
    """
    Page Object for OrangeHRM Login Page
    Demonstrates separation of locators and methods
    """
    
    # ========== Locators ==========
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.XPATH, "//p[@class='oxd-text oxd-text--p oxd-alert-content-text']")
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    
    # ========== Page Actions ==========
    
    def enter_username(self, username):
        """Enter username using reusable input_text method"""
        return self.input_text(self.USERNAME_FIELD, username, "username field")
    
    def enter_password(self, password):
        """Enter password using reusable input_text method"""
        return self.input_text(self.PASSWORD_FIELD, password, "password field")
    
    def click_login(self):
        """Click login button using reusable click method"""
        return self.click(self.LOGIN_BUTTON, "login button")
    
    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE, "error message")
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def verify_login_page_loaded(self):
        """Verify login page is loaded"""
        return self.is_element_visible(self.LOGIN_BUTTON)
    
    def verify_login_successful(self):
        """Verify login was successful by checking dashboard"""
        try:
            self.wait_for_element(self.DASHBOARD_HEADER)
            print("Login successful - Dashboard is visible")
            return True
        except:
            print("Login failed - Dashboard not found")
            return False
    
    # ========== Business Logic ==========
    
    def login(self, username, password):
        """Complete login workflow"""
        print(f"\n--- Performing Login ---")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        print(f"--- Login Attempted ---\n")
        return True


class DashboardPage(BasePage):
    """
    Page Object for OrangeHRM Dashboard Page
    """
    
    # ========== Locators ==========
    DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    USER_DROPDOWN = (By.CLASS_NAME, "oxd-userdropdown-tab")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Logout']")
    WELCOME_MESSAGE = (By.CLASS_NAME, "oxd-userdropdown-name")
    
    # ========== Page Actions ==========
    
    def get_dashboard_title(self):
        """Get dashboard header text"""
        return self.get_text(self.DASHBOARD_HEADER, "dashboard header")
    
    def is_dashboard_displayed(self):
        """Check if dashboard is displayed"""
        return self.is_element_visible(self.DASHBOARD_HEADER)
    
    def click_user_dropdown(self):
        """Click user dropdown using reusable click method"""
        return self.click(self.USER_DROPDOWN, "user dropdown")
    
    def click_logout(self):
        """Click logout using reusable click method"""
        return self.click(self.LOGOUT_LINK, "logout link")
    
    # ========== Business Logic ==========
    
    def logout(self):
        """Complete logout workflow"""
        print(f"\n--- Performing Logout ---")
        self.click_user_dropdown()
        self.sleep(1)
        self.click_logout()
        print(f"--- Logout Completed ---\n")
        return True
    
    def verify_successful_login(self):
        """Verify user successfully logged in"""
        return self.is_dashboard_displayed()


# =============================================================================
# SECTION 4: TEST CASES (For demonstration)
# =============================================================================

class TestOrangeHRMLogin:
    """
    Test class demonstrating POM usage
    Can be run with pytest or standalone
    """
    
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
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
        self.driver.maximize_window()
        
        # Initialize Page Objects
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        
        # Navigate to login page
        self.driver.get(Config.LOGIN_URL)
        print("Navigated to OrangeHRM login page")
        print("Test setup complete\n")
    
    def teardown(self):
        """Teardown test - Close browser"""
        print("\n" + "="*60)
        print("Tearing down test environment...")
        print("="*60)
        time.sleep(2)
        if self.driver:
            self.driver.quit()
            print("Browser closed")
        print("Test teardown complete")
        print("="*60 + "\n")
    
    def test_valid_login(self):
        """Test Case 1: Login with valid credentials"""
        print("\n[TEST CASE 1: Valid Login]")
        print("-" * 60)
        
        # Perform login
        self.login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        time.sleep(2)
        
        # Verify login
        is_logged_in = self.login_page.verify_login_successful()
        
        if is_logged_in:
            dashboard_title = self.dashboard_page.get_dashboard_title()
            print(f"Dashboard title: {dashboard_title}")
            print("TEST PASSED: Valid login successful")
        else:
            print("TEST FAILED: Login was not successful")
        
        print("-" * 60)
        return is_logged_in
    
    def test_login_and_logout(self):
        """Test Case 2: Login and logout"""
        print("\n[TEST CASE 2: Login and Logout]")
        print("-" * 60)
        
        # Login
        self.login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
        time.sleep(2)
        
        # Verify login
        is_logged_in = self.login_page.verify_login_successful()
        
        if is_logged_in:
            print("Login successful")
            
            # Logout
            time.sleep(2)
            self.dashboard_page.logout()
            time.sleep(2)
            
            # Verify logout
            current_url = self.driver.current_url
            if "auth/login" in current_url:
                print("Logout successful - Redirected to login page")
                print("TEST PASSED")
                print("-" * 60)
                return True
            else:
                print("Logout failed")
                print("TEST FAILED")
                print("-" * 60)
                return False
        else:
            print("✗ TEST FAILED: Login was not successful")
            print("-" * 60)
            return False


# =============================================================================
# SECTION 5: MAIN EXECUTION
# =============================================================================

def run_demo_tests():
    """
    Run demonstration tests to show framework functionality
    """
    print("\n" + "="*60)
    print("DAY 18 - SELENIUM POM FRAMEWORK DEMONSTRATION")
    print("="*60)
    print("\nThis framework demonstrates:")
    print("1. Page Object Model (POM) implementation")
    print("2. Separated page classes, test scripts, and configuration")
    print("3. Reusable methods (click, input, select, wait)")
    print("4. Multiple test cases")
    print("="*60)
    
    test = TestOrangeHRMLogin()
    
    try:
        # Test 1: Valid Login
        test.setup()
        test.test_valid_login()
        test.teardown()
        
        # Test 2: Login and Logout
        print("\n" + "="*60)
        print("STARTING NEW TEST")
        print("="*60)
        test.setup()
        test.test_login_and_logout()
        test.teardown()
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        if test.driver:
            test.teardown()
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETED")
    print("="*60)
    print("\nFramework Features Demonstrated:")
    print("   - Page Object Model architecture")
    print("   - Reusable click() method in BasePage")
    print("   - Reusable input_text() method in BasePage")
    print("   - Reusable select methods in BasePage")
    print("   - Separation of page classes and test logic")
    print("   - Proper setup/teardown")
    print("\nThis single file contains the complete framework!")
    print("="*60 + "\n")


# =============================================================================
# RUN THE DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("""
    ===================================================================
    DAY 18 - SELENIUM AUTOMATION FRAMEWORK (POM)
    Wipro Pre-Skilling Tech Academy Submission
    
    Contains:
    - Question 7 - Complete POM Framework
    - Lab 11 - Page Object Model Implementation
    - Reusable Methods: click, input, select, wait
    - Multiple Test Cases
    ===================================================================
    """)
    
    run_demo_tests()
