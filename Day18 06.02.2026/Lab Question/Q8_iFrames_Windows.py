from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
driver.maximize_window()
driver.implicitly_wait(10)

try:
    print("=" * 80)
    print("QUESTION 8: Handling iFrames and Windows")
    print("=" * 80)
    
    print("\n--- Part 1: Working with iFrames ---")
    
    driver.get("https://www.w3schools.com/html/html_iframe.asp")
    print(f"Opened URL: {driver.current_url}")
    print(f"Main Page Title: {driver.title}")
    time.sleep(2)
    
    driver.get("https://www.w3schools.com/html/tryit.asp?filename=tryhtml_iframe")
    print(f"\nNavigated to tryit editor: {driver.current_url}")
    time.sleep(2)
    
    iframe = driver.find_element(By.ID, "iframeResult")
    driver.switch_to.frame(iframe)
    print("Switched to iframe 'iframeResult'")
    
    iframe_body = driver.find_element(By.TAG_NAME, "body")
    print(f"Inside iframe - Body text preview: {iframe_body.text[:100]}...")
    
    print("\n--- Part 2: Switching Back to Main Content ---")
    
    driver.switch_to.default_content()
    print("Switched back to main content")
    print(f"Verified - Current URL: {driver.current_url}")
    
    print("\n--- Part 3: Opening New Window/Tab ---")
    
    parent_window = driver.current_window_handle
    print(f"Parent Window Handle: {parent_window}")
    print(f"Parent Window Title: {driver.title}")
    
    driver.execute_script("window.open('https://www.selenium.dev', '_blank');")
    print("Opened new tab with Selenium website")
    time.sleep(2)
    
    print("\n--- Part 4: Switching Between Windows ---")
    
    all_windows = driver.window_handles
    print(f"\nTotal windows open: {len(all_windows)}")
    
    for index, window in enumerate(all_windows, 1):
        driver.switch_to.window(window)
        print(f"\nWindow {index}:")
        print(f"  Handle: {window}")
        print(f"  Title: {driver.title}")
        print(f"  URL: {driver.current_url}")
        time.sleep(1)
    
    print("\n--- Part 5: Closing Child Window and Returning to Parent ---")
    
    child_window = [window for window in all_windows if window != parent_window][0]
    driver.switch_to.window(child_window)
    print(f"\nClosing child window: {driver.title}")
    driver.close()
    print("Child window closed")
    
    driver.switch_to.window(parent_window)
    print(f"Switched back to parent window")
    print(f"  Parent Window Title: {driver.title}")
    print(f"  Parent Window URL: {driver.current_url}")
    
    remaining_windows = driver.window_handles
    print(f"\nRemaining windows: {len(remaining_windows)}")
    
    print("\n" + "=" * 80)
    print("SCRIPT COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    time.sleep(3)

except Exception as e:
    print(f"\nError occurred: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    print("\nClosing browser...")
    driver.quit()
    print("Browser closed")
