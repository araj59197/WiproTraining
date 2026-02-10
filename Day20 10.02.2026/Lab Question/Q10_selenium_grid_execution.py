"""
Question 10 - Selenium Grid Execution

This script demonstrates:
1. Connecting to Selenium Grid using RemoteWebDriver
2. Running the same test on multiple browsers
3. Navigating to a website and verifying the page title
4. Printing browser name and platform for each execution
"""

from selenium import webdriver
import time

# Selenium Grid Hub URL
GRID_URL = "http://192.168.1.9:4444/wd/hub"

# Test website URL
TEST_URL = "https://www.google.com"
EXPECTED_TITLE = "Google"

# List of browsers to test
BROWSERS = ["chrome", "edge"]


def run_test_on_browser(browser_name):
    """
    Run the test on a specific browser using Selenium Grid
    
    Args:
        browser_name (str): Name of the browser (chrome, edge, firefox)
    """
    print(f"\n{'='*60}")
    print(f"Starting test on {browser_name.upper()} browser")
    print(f"{'='*60}")
    
    try:
        # Step 1: Set up browser options based on browser type
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            # Anti-detection options to avoid Google CAPTCHA
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
        elif browser_name == "edge":
            options = webdriver.EdgeOptions()
            # Anti-detection options
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
        else:
            print(f"ERROR: Browser {browser_name} is not supported!")
            return
        
        # Step 2: Connect to Selenium Grid using RemoteWebDriver
        print(f"Connecting to Selenium Grid at {GRID_URL}")
        driver = webdriver.Remote(
            command_executor=GRID_URL,
            options=options
        )
        
        # Step 3: Get browser capabilities (platform and browser info)
        capabilities = driver.capabilities
        browser_name_cap = capabilities.get('browserName', 'Unknown')
        browser_version = capabilities.get('browserVersion', 'Unknown')
        platform_name = capabilities.get('platformName', 'Unknown')
        
        # Step 4: Print browser and platform information
        print(f"\nBrowser Information:")
        print(f"   Browser Name: {browser_name_cap}")
        print(f"   Browser Version: {browser_version}")
        print(f"   Platform: {platform_name}")
        
        # Step 5: Maximize window
        driver.maximize_window()
        print(f"\nNavigating to: {TEST_URL}")
        
        # Step 6: Navigate to the website
        driver.get(TEST_URL)
        time.sleep(2)  # Wait for page to load
        
        # Step 7: Get and verify page title
        actual_title = driver.title
        print(f"\nPage Title: {actual_title}")
        
        # Step 8: Verify the title
        if EXPECTED_TITLE in actual_title:
            print(f"TEST PASSED: Title verification successful!")
            print(f"   Expected: '{EXPECTED_TITLE}' found in '{actual_title}'")
        else:
            print(f"TEST FAILED: Title verification failed!")
            print(f"   Expected: '{EXPECTED_TITLE}'")
            print(f"   Actual: '{actual_title}'")
        
        # Step 9: Close the browser
        print(f"\nClosing {browser_name} browser...")
        driver.quit()
        print(f"Test completed successfully on {browser_name.upper()}")
        
    except Exception as e:
        print(f"\nERROR occurred while testing on {browser_name}: {str(e)}")
        print(f"   Make sure Selenium Grid is running at {GRID_URL}")


def main():
    """
    Main function to run tests on all browsers
    """
    print("\n" + "="*60)
    print("SELENIUM GRID EXECUTION TEST")
    print("="*60)
    print(f"Test URL: {TEST_URL}")
    print(f"Expected Title: {EXPECTED_TITLE}")
    print(f"Grid URL: {GRID_URL}")
    print(f"Browsers to test: {', '.join([b.upper() for b in BROWSERS])}")
    print("="*60)
    
    # Run test on each browser
    for browser in BROWSERS:
        run_test_on_browser(browser)
        time.sleep(1)  # Small delay between browser tests
    
    # Final summary
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED!")
    print("="*60)
    print(f"Total browsers tested: {len(BROWSERS)}")
    print("="*60 + "\n")


# Entry point
if __name__ == "__main__":
    main()
