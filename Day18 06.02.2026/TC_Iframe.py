from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions
driver=webdriver.Firefox()
driver.implicitly_wait(10)
wait=WebDriverWait(driver,10)

driver.get("https://letcode.in/frame")
#time.sleep(5)
iframe=driver.find_element(By.TAG_NAME,"iframe")
driver.switch_to.frame(iframe)
driver.find_element(By.NAME,"fname").send_keys("Aditya")
driver.find_element(By.NAME,"lname").send_keys("Raj")
driver.switch_to.default_content()
insight=driver.find_element(By.XPATH,"//p[text()=' Insight ']").is_displayed()


print("insight is displayed",insight)