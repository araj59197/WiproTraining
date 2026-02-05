"""
Question 6 - Handling Alerts and Pop-ups

This script demonstrates:
1. Triggering a JavaScript alert
2. Accepting the alert and printing its message
3. Dismissing a confirmation pop-up
4. Entering text in a prompt alert and accepting it
5. Verifying the result displayed on the page
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Initialize Chrome driver
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Navigate to the alerts practice page
    print("Opening DemoQA Alerts Page...")
    driver.get("https://demoqa.com/alerts")
    time.sleep(2)
    
    # 1. TRIGGER AND ACCEPT SIMPLE ALERT
    print("\n1. Handling Simple Alert...")
    
    # Click button to trigger alert (using JavaScript to avoid ad overlay)
    alert_button = driver.find_element(By.ID, "alertButton")
    driver.execute_script("arguments[0].click();", alert_button)
    time.sleep(1)
    
    # Switch to alert and get message
    alert = driver.switch_to.alert
    alert_message = alert.text
    print(f"   Alert Message: '{alert_message}'")
    
    # Accept the alert
    alert.accept()
    print("   Alert accepted")
    
    time.sleep(2)
    
    # 2. HANDLE DELAYED ALERT (appears after 5 seconds)
    print("\n2. Handling Delayed Alert...")
    
    # Click button to trigger delayed alert (using JavaScript to avoid ad overlay)
    delayed_alert_button = driver.find_element(By.ID, "timerAlertButton")
    driver.execute_script("arguments[0].click();", delayed_alert_button)
    print("   Waiting for delayed alert (5 seconds)...")
    
    # Wait for alert to appear
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    
    # Switch to alert and get message
    delayed_alert = driver.switch_to.alert
    delayed_alert_message = delayed_alert.text
    print(f"   Delayed Alert Message: '{delayed_alert_message}'")
    
    # Accept the alert
    delayed_alert.accept()
    print("   Delayed alert accepted")
    
    time.sleep(2)
    
    # 3. DISMISS CONFIRMATION POP-UP
    print("\n3. Handling Confirmation Pop-up (Dismiss)...")
    
    # Click button to trigger confirmation (using JavaScript to avoid ad overlay)
    confirm_button = driver.find_element(By.ID, "confirmButton")
    driver.execute_script("arguments[0].click();", confirm_button)
    time.sleep(1)
    
    # Switch to confirmation alert
    confirm_alert = driver.switch_to.alert
    confirm_message = confirm_alert.text
    print(f"   Confirmation Message: '{confirm_message}'")
    
    # Dismiss the confirmation (click Cancel)
    confirm_alert.dismiss()
    print("   Confirmation dismissed (Cancel clicked)")
    
    # Verify result
    result = driver.find_element(By.ID, "confirmResult")
    result_text = result.text
    print(f"   Result displayed: '{result_text}'")
    
    time.sleep(2)
    
    # 3b. ACCEPT CONFIRMATION POP-UP
    print("\n3b. Handling Confirmation Pop-up (Accept)...")
    
    # Click button again to trigger confirmation (using JavaScript to avoid ad overlay)
    driver.execute_script("arguments[0].click();", confirm_button)
    time.sleep(1)
    
    # Switch to confirmation alert and accept
    confirm_alert2 = driver.switch_to.alert
    confirm_alert2.accept()
    print("   Confirmation accepted (OK clicked)")
    
    # Verify result
    result2 = driver.find_element(By.ID, "confirmResult")
    result_text2 = result2.text
    print(f"   Result displayed: '{result_text2}'")
    
    time.sleep(2)
    
    # 4. ENTER TEXT IN PROMPT ALERT
    print("\n4. Handling Prompt Alert...")
    
    # Click button to trigger prompt (using JavaScript to avoid ad overlay)
    prompt_button = driver.find_element(By.ID, "promtButton")
    driver.execute_script("arguments[0].click();", prompt_button)
    time.sleep(1)
    
    # Switch to prompt alert
    prompt_alert = driver.switch_to.alert
    prompt_message = prompt_alert.text
    print(f"   Prompt Message: '{prompt_message}'")
    
    # Enter text in prompt
    user_input = "Aditya Raj"
    prompt_alert.send_keys(user_input)
    print(f"   Entered text: '{user_input}'")
    
    # Accept the prompt
    prompt_alert.accept()
    print("   Prompt accepted")
    
    time.sleep(1)
    
    # 5. VERIFY RESULT DISPLAYED ON PAGE
    print("\n5. Verifying Results...")
    
    # Get the result displayed on page
    prompt_result = driver.find_element(By.ID, "promptResult")
    prompt_result_text = prompt_result.text
    print(f"   Final Result: '{prompt_result_text}'")
    
    # Verify the entered text appears in result
    if user_input in prompt_result_text:
        print(f"\nSUCCESS! User input '{user_input}' verified in result!")
    else:
        print(f"\nFAILED! User input not found in result!")
    
    # Summary
    print("\n" + "="*60)
    print("ALERT HANDLING SUMMARY")
    print("="*60)
    print(f"1. Simple Alert: {alert_message}")
    print(f"2. Delayed Alert: {delayed_alert_message}")
    print(f"3. Confirmation (Dismiss): {result_text}")
    print(f"4. Confirmation (Accept): {result_text2}")
    print(f"5. Prompt Alert: {prompt_result_text}")
    print("="*60)
    
    time.sleep(3)
    
except Exception as e:
    print(f"\nError occurred: {e}")
    import traceback
    traceback.print_exc()

finally:
    time.sleep(2)
    driver.quit()
    print("\nBrowser closed\n")
