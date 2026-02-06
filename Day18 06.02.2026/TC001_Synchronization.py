from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
driver = webdriver.Chrome()
# driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)
driver.get("https://opensource-demo.orangehrmlive.com/")


# time.sleep(5)
element = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
driver.find_element(By.NAME, "username").send_keys("Admin")
driver.find_element(By.NAME, "password").send_keys("admin123")
driver.find_element(By.XPATH, "//button[@type='submit']").click()

