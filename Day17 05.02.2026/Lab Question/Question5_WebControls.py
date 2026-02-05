"""
Question 5 - Handling Web Controls

This script demonstrates:
1. Filling text boxes
2. Selecting radio buttons and checkboxes
3. Choosing options from drop-down lists using Select class
4. Submitting the form and verifying confirmation message
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


# Initialize Chrome driver
driver = webdriver.Chrome()
driver.maximize_window()

try:
    print("Opening DemoQA Practice Form...")
    driver.get("https://demoqa.com/automation-practice-form")
    time.sleep(2)
    
    print("\n1. Filling text boxes...")
    
    first_name = driver.find_element(By.ID, "firstName")
    first_name.send_keys("Aditya")
    print("   First Name: Aditya")
    
    last_name = driver.find_element(By.ID, "lastName")
    last_name.send_keys("Raj")
    print("   Last Name: Raj")
    
    email = driver.find_element(By.ID, "userEmail")
    email.send_keys("aditya.raj@example.com")
    print("   Email: aditya.raj@example.com")
    
    mobile = driver.find_element(By.ID, "userNumber")
    mobile.send_keys("9876543210")
    print("   Mobile: 9876543210")
    
    address = driver.find_element(By.ID, "currentAddress")
    address.send_keys("123 Main Street, Mumbai, India")
    print("   Address: 123 Main Street, Mumbai, India")
    
    time.sleep(1)
    
    print("\n2. Selecting radio buttons...")
    
    male_radio = driver.find_element(By.XPATH, "//label[@for='gender-radio-1']")
    male_radio.click()
    print("   Gender: Male selected")
    
    time.sleep(1)
    
    print("\n3. Selecting checkboxes...")
    
    sports_checkbox = driver.find_element(By.XPATH, "//label[@for='hobbies-checkbox-1']")
    sports_checkbox.click()
    print("   Hobby: Sports selected")
    
    reading_checkbox = driver.find_element(By.XPATH, "//label[@for='hobbies-checkbox-2']")
    reading_checkbox.click()
    print("   Hobby: Reading selected")
    
    time.sleep(1)
    
    print("\n4. Selecting from dropdowns...")
    
    dob_input = driver.find_element(By.ID, "dateOfBirthInput")
    dob_input.click()
    time.sleep(1)
    
    month_dropdown = Select(driver.find_element(By.CLASS_NAME, "react-datepicker__month-select"))
    month_dropdown.select_by_visible_text("January")
    print("   Month: January selected")
    
    year_dropdown = Select(driver.find_element(By.CLASS_NAME, "react-datepicker__year-select"))
    year_dropdown.select_by_visible_text("2000")
    print("   Year: 2000 selected")
    
    day = driver.find_element(By.XPATH, "//div[contains(@class, 'react-datepicker__day--015')]")
    day.click()
    print("   Day: 15 selected")
    
    time.sleep(1)

    subject = driver.find_element(By.ID, "subjectsInput")
    subject.send_keys("Maths")
    time.sleep(1)
    subject.send_keys(Keys.ENTER)
    print("   Subject: Maths added")
    
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    state_dropdown = driver.find_element(By.ID, "state")
    state_dropdown.click()
    time.sleep(1)
    state_option = driver.find_element(By.XPATH, "//div[text()='NCR']")
    state_option.click()
    print("   State: NCR selected")
    
    time.sleep(1)
    
    # City
    city_dropdown = driver.find_element(By.ID, "city")
    city_dropdown.click()
    time.sleep(1)
    city_option = driver.find_element(By.XPATH, "//div[text()='Delhi']")
    city_option.click()
    print("   City: Delhi selected")
    
    time.sleep(1)
    
    # 5. SUBMIT THE FORM
    print("\n5. Submitting the form...")
    submit_button = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    time.sleep(1)
    submit_button.click()
    print("   Form submitted")
    
    time.sleep(2)
    
    # 6. VERIFY CONFIRMATION MESSAGE
    print("\n6. Verifying confirmation message...")
    
    # Wait for modal to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "example-modal-sizes-title-lg"))
    )
    
    # Get confirmation message
    confirmation_title = driver.find_element(By.ID, "example-modal-sizes-title-lg")
    confirmation_text = confirmation_title.text
    
    print(f"   Confirmation Message: '{confirmation_text}'")
    
    # Verify the message
    if "Thanks for submitting the form" in confirmation_text:
        print("\nSUCCESS! Form submission confirmed!")
        
        # Display submitted values
        print("\nSubmitted Values:")
        table_rows = driver.find_elements(By.XPATH, "//div[@class='modal-body']//table//tr")
        for row in table_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                print(f"   {cells[0].text}: {cells[1].text}")
    else:
        print("\nFAILED! Confirmation message not found!")
    
    # Keep modal open for viewing
    time.sleep(5)
    
    # Close modal using JavaScript click to avoid ad overlay issues
    close_button = driver.find_element(By.ID, "closeLargeModal")
    driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
    time.sleep(0.5)  # Brief wait after scroll
    driver.execute_script("arguments[0].click();", close_button)
    print("\nModal closed")
    
except Exception as e:
    print(f"\nError occurred: {e}")
    import traceback
    traceback.print_exc()

finally:
    time.sleep(2)
    driver.quit()
    print("\nBrowser closed\n")
