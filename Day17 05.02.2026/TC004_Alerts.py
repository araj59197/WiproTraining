from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
driver = webdriver.Chrome()
driver.get("https://letcode.in/alert")
time.sleep(2)  
driver.find_element(By.ID, "accept").click()
try:
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print(f"Alert text: {alert.text}")
    alert.accept()
    print("Alert Accepted")
except Exception as e:
    print(f"Error handling alert: {e}")
finally:
    time.sleep(1)
    driver.quit()