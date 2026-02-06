from LoginPagefactory import loginpage_PageFactory
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Firefox()
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
time.sleep(5)

loginobj = loginpage_PageFactory(driver)

loginobj.enterusername("Admin")
loginobj.enterpassword("admin123")

loginobj.clicklogin()
