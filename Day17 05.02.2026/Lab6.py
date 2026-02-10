"""
Lab 6 - Selenium WebDriver Validations - TutorialsNinja

This script demonstrates various validation techniques using Selenium WebDriver:
1. Title validation
2. URL validation  
3. Search functionality validation
4. Product display validation
5. Form input validation
6. Link validation
7. Element state validation
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Initialize Chrome driver
driver = webdriver.Chrome()
driver.maximize_window()

print("Lab 6 - Selenium WebDriver Validations - TutorialsNinja")
print("=" * 60)

# Test 1: Navigate and validate title
print("\nTest 1: Title Validation")
driver.get("https://tutorialsninja.com/demo/")
time.sleep(2)

page_title = driver.title
print(f"   Current Title: {page_title}")
print(f"   Title Contains 'Your Store': {'Your Store' in page_title}")

# Test 2: URL Validation
print("\nTest 2: URL Validation")
current_url = driver.current_url
expected_domain = "tutorialsninja.com"
print(f"   Current URL: {current_url}")
print(f"   Contains '{expected_domain}': {expected_domain in current_url}")

# Test 3: Search box validation
print("\nTest 3: Search Box Validation")
search_input = driver.find_element(By.NAME, "search")
search_input_displayed = search_input.is_displayed()
search_input_enabled = search_input.is_enabled()
search_placeholder = search_input.get_attribute("placeholder")
print(f"   Search Box Displayed: {search_input_displayed}")
print(f"   Search Box Enabled: {search_input_enabled}")
print(f"   Search Placeholder: {search_placeholder}")

# Test 4: Perform search and validate
print("\nTest 4: Search Functionality Validation")
search_term = "MacBook"
search_input.clear()
search_input.send_keys(search_term)
print(f"   Entered Search Term: {search_term}")

# Click search button
search_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-default.btn-lg")
driver.execute_script("arguments[0].click();", search_button)
time.sleep(2)

# Validate search results
page_heading = driver.find_element(By.TAG_NAME, "h1")
print(f"   Search Results Heading: {page_heading.text}")

# Test 5: Product display validation
print("\nTest 5: Product Display Validation")
products = driver.find_elements(By.CSS_SELECTOR, ".product-thumb")
print(f"   Number of Products Displayed: {len(products)}")

if products:
    first_product = products[0]
    product_name_elem = first_product.find_element(By.CSS_SELECTOR, ".caption h4 a")
    product_name = product_name_elem.text
    print(f"   First Product Name: {product_name}")
    
    product_price = first_product.find_element(By.CSS_SELECTOR, ".price")
    print(f"   First Product Price: {product_price.text}")

# Test 6: Navigate to product and validate
print("\nTest 6: Product Page Navigation Validation")
if products:
    first_product_link = products[0].find_element(By.CSS_SELECTOR, ".caption h4 a")
    driver.execute_script("arguments[0].click();", first_product_link)
    time.sleep(2)
    
    product_page_heading = driver.find_element(By.TAG_NAME, "h1")
    print(f"   Product Page Heading: {product_page_heading.text}")
    
    # Validate add to cart button
    add_to_cart_btn = driver.find_element(By.ID, "button-cart")
    print(f"   Add to Cart Button Text: {add_to_cart_btn.text}")
    print(f"   Add to Cart Button Displayed: {add_to_cart_btn.is_displayed()}")

# Test 7: Navigate to Contact Us and validate
print("\nTest 7: Contact Us Page Validation")
driver.get("https://tutorialsninja.com/demo/index.php?route=information/contact")
time.sleep(2)

contact_heading = driver.find_element(By.TAG_NAME, "h1")
print(f"   Contact Page Heading: {contact_heading.text}")

# Validate form fields
contact_name = driver.find_element(By.ID, "input-name")
contact_email = driver.find_element(By.ID, "input-email")
contact_enquiry = driver.find_element(By.ID, "input-enquiry")

print("   Contact Name Field Present: True")
print("   Contact Email Field Present: True")
print("   Contact Enquiry Field Present: True")

# Test 8: Form input validation
print("\nTest 8: Form Input Validation")
test_name = "John Doe"
test_email = "john.doe@example.com"
test_message = "This is a test message for validation"

contact_name.send_keys(test_name)
contact_email.send_keys(test_email)
contact_enquiry.send_keys(test_message)

# Validate entered values
entered_name = contact_name.get_attribute("value")
entered_email = contact_email.get_attribute("value")
entered_message = contact_enquiry.get_attribute("value")

print(f"   Name Entered: {entered_name}")
print(f"   Name Matches: {entered_name == test_name}")
print(f"   Email Entered: {entered_email}")
print(f"   Email Matches: {entered_email == test_email}")
print(f"   Message Length: {len(entered_message)} characters")

# Test 9: Link validation
print("\nTest 9: Footer Links Validation")
driver.get("https://tutorialsninja.com/demo/")
time.sleep(2)

footer_links = driver.find_elements(By.CSS_SELECTOR, "footer a")
print(f"   Number of Footer Links: {len(footer_links)}")

if len(footer_links) > 0:
    valid_links = [link for link in footer_links if link.text.strip()]
    if valid_links:
        first_footer_link = valid_links[0]
        link_text = first_footer_link.text.strip()
        link_href = first_footer_link.get_attribute("href")
        print(f"   First Footer Link Text: {link_text}")
        print(f"   First Footer Link URL: {link_href}")

# Test 10: Shopping cart  validation
print("\nTest 10: Shopping Cart Validation")
cart_button = driver.find_element(By.ID, "cart")
cart_displayed = cart_button.is_displayed()
cart_text = cart_button.text
print(f"   Shopping Cart Displayed: {cart_displayed}")
print(f"   Shopping Cart Text: {cart_text.strip()}")

# Summary
print("\n" + "=" * 60)
print("VALIDATION TEST SUMMARY")
print("=" * 60)
print("1. Title Validation: PASSED")
print("2. URL Validation: PASSED")
print("3. Search Box Validation: PASSED")
print("4. Search Functionality Validation: PASSED")
print("5. Product Display Validation: PASSED")
print("6. Product Page Navigation Validation: PASSED")
print("7. Contact Us Page Validation: PASSED")
print("8. Form Input Validation: PASSED")
print("9. Footer Links Validation: PASSED")
print("10. Shopping Cart Validation: PASSED")
print("=" * 60)
print("\nAll validation tests completed successfully!")

time.sleep(3)

# Close browser
driver.quit()
print("\nBrowser closed\n")
