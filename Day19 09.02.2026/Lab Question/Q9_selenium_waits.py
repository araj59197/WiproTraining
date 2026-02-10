"""
Question 9 – Selenium Waits

This script demonstrates:
1. Implicit Wait
2. Explicit Wait for an element to become clickable
3. Fluent Wait with a polling interval
4. Prints a message when the element is available for interaction
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


def setup_driver():
    """Initialize Chrome WebDriver with options"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    return driver


# ============================================
# 1. IMPLICIT WAIT DEMONSTRATION
# ============================================
def demonstrate_implicit_wait():
    """
    Implicit Wait:
    - Sets a default waiting time for the entire WebDriver instance
    - WebDriver will wait for the specified time before throwing NoSuchElementException
    - Applied globally to all find_element calls
    """
    print("\n" + "=" * 60)
    print("1. IMPLICIT WAIT DEMONSTRATION")
    print("=" * 60)
    time.sleep(2)

    driver = setup_driver()

    try:
        # Set implicit wait to 10 seconds
        driver.implicitly_wait(10)
        print("Implicit wait set to 10 seconds")

        # Navigate to a test page
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        print("Navigated to the test page")

        # Click button to add an element dynamically
        add_button = driver.find_element(By.ID, "adder")
        add_button.click()
        print("Clicked 'Add a box!' button")

        # Implicit wait will automatically wait for the element to appear
        start_time = time.time()
        dynamic_element = driver.find_element(By.ID, "box0")
        end_time = time.time()

        print(f"Element found after {end_time - start_time:.2f} seconds")
        print(f"MESSAGE: Element with ID 'box0' is NOW AVAILABLE for interaction!")
        print(f"Element text/class: {dynamic_element.get_attribute('class')}")
        time.sleep(3)

    except NoSuchElementException as e:
        print(f"Element not found within implicit wait time: {e}")
    finally:
        driver.quit()
        print("Browser closed")

def demonstrate_explicit_wait():
    """
    Explicit Wait:
    - Waits for a specific condition to be met before proceeding
    - More flexible and precise than implicit wait
    - Can wait for various conditions like clickable, visible, present, etc.
    """
    print("\n" + "=" * 60)
    print("2. EXPLICIT WAIT DEMONSTRATION (Element Clickable)")
    print("=" * 60)
    time.sleep(2)

    driver = setup_driver()

    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        print("Navigated to the test page")

        # Click to reveal a hidden element
        reveal_button = driver.find_element(By.ID, "reveal")
        reveal_button.click()
        print("Clicked 'Reveal a new input' button")

        # Create explicit wait with 10 second timeout
        wait = WebDriverWait(driver, 10)

        # Wait explicitly for element to become clickable
        start_time = time.time()
        revealed_input = wait.until(EC.element_to_be_clickable((By.ID, "revealed")))
        end_time = time.time()

        print(f"Explicit wait completed in {end_time - start_time:.2f} seconds")
        print(f"MESSAGE: Element with ID 'revealed' is NOW CLICKABLE!")

        # Interact with the element
        revealed_input.send_keys("Hello Selenium!")
        print("Successfully typed text into the revealed input field")
        time.sleep(3)

    except TimeoutException:
        print("Timeout: Element did not become clickable within 10 seconds")
    finally:
        driver.quit()
        print("Browser closed")

def demonstrate_fluent_wait():
    """
    Fluent Wait:
    - Similar to explicit wait but with more control
    - Allows setting polling interval (how often to check the condition)
    - Can ignore specific exceptions during waiting
    - Maximum flexibility in wait configuration
    """
    print("\n" + "=" * 60)
    print("3. FLUENT WAIT DEMONSTRATION (With Polling Interval)")
    print("=" * 60)
    time.sleep(2)

    driver = setup_driver()

    try:
        driver.get("https://www.selenium.dev/selenium/web/dynamic.html")
        print("Navigated to the test page")

        # Click button to add element with delay
        add_button = driver.find_element(By.ID, "adder")
        add_button.click()
        print("Clicked 'Add a box!' button")


        fluent_wait = WebDriverWait(
            driver,
            timeout=15,
            poll_frequency=0.5,  # Check every 500 milliseconds
            ignored_exceptions=[NoSuchElementException],
        )

        print("Fluent wait configured:")
        print("  - Timeout: 15 seconds")
        print("  - Polling interval: 500 milliseconds")
        print("  - Ignoring: NoSuchElementException")

        # Wait for element with fluent wait
        start_time = time.time()
        poll_count = [0]  # Use list to track polls in nested function

        def element_found(driver):
            poll_count[0] += 1
            try:
                element = driver.find_element(By.ID, "box0")
                print(f"  Poll #{poll_count[0]}: Element found!")
                return element
            except NoSuchElementException:
                print(f"  Poll #{poll_count[0]}: Element not yet available...")
                return False

        dynamic_element = fluent_wait.until(element_found)
        end_time = time.time()

        print(f"\nFluent wait completed in {end_time - start_time:.2f} seconds")
        print(f"Total polling attempts: {poll_count[0]}")
        print(f"MESSAGE: Element with ID 'box0' is NOW AVAILABLE for interaction!")
        print(f"Element class: {dynamic_element.get_attribute('class')}")

        # Interact with the element
        dynamic_element.click()
        print("Successfully clicked the dynamic element")
        time.sleep(3)

    except TimeoutException:
        print("Timeout: Element did not appear within 15 seconds")
    finally:
        driver.quit()
        print("Browser closed")


# ============================================
# COMPARISON OF ALL WAIT TYPES
# ============================================
def print_wait_comparison():
    """Print a comparison table of different wait types"""
    print("\n" + "=" * 60)
    print("COMPARISON OF SELENIUM WAITS")
    print("=" * 60)

    comparison = """
    Implicit Wait:
      - Global setting for entire driver
      - Applies to all find_element calls
      - Cannot specify conditions
      - Simple to implement

    Explicit Wait:
      - Waits for specific condition
      - Applied to specific elements
      - Multiple built-in conditions available
      - More precise control

    Fluent Wait:
      - Custom polling interval
      - Ignore specific exceptions
      - Maximum flexibility
      - Best for complex scenarios
    """
    print(comparison)
    time.sleep(3)

if __name__ == "__main__":
    print("\n" + "*" * 60)
    print("SELENIUM WAITS DEMONSTRATION")
    print("*" * 60)

    # Print comparison first
    print_wait_comparison()

    # Run all demonstrations
    try:
        # 1. Implicit Wait
        demonstrate_implicit_wait()

        # 2. Explicit Wait (Element Clickable)
        demonstrate_explicit_wait()

        # 3. Fluent Wait with Polling
        demonstrate_fluent_wait()

    except Exception as e:
        print(f"\nAn error occurred: {e}")

    print("\n" + "*" * 60)
    print("ALL DEMONSTRATIONS COMPLETED")
    print("*" * 60)
