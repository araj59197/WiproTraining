from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
driver = webdriver.Firefox()
driver.get("https://amazon.in")
# driver.execute_script("alert('Hello World')")
time.sleep(5)
driver.execute_script("window.scrollBy(0, 1000)")
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")