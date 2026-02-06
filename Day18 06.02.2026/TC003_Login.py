from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions

from LoginPage import loginpage

driver=webdriver.Firefox()
driver.implicitly_wait(10)
wait=WebDriverWait(driver,10)

driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
#time.sleep(5)
loginobj=loginpage(driver)

# Perform login
loginobj.enterusername("Admin")
loginobj.enterpassword("admin123")
loginobj.clicklogin()

# Wait to see the dashboard after login
time.sleep(5)
driver.quit()
