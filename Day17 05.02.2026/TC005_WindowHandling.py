from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()
driver.get("https://letcode.in/window")
time.sleep(5)
driver.find_element(By.ID, "multi").click()
window_handles = driver.window_handles
for handle in window_handles:
    driver.switch_to.window(handle)
    time.sleep(2)
    print(driver.title)

