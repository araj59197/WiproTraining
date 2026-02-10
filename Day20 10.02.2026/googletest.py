import pytest
from driverfactory import getdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("browser",["chrome","edge"])
def test_google(browser):
    driver=getdriver(browser)
    driver.get("https://www.google.com")
    assert "Google" in driver.title
    driver.quit()
    
@pytest.mark.parametrize("browser", ["chrome", "edge"])
def test_google_serach(browser):
    driver = getdriver(browser)
    driver.get("https://www.google.com/")
    serachbox=driver.find_element("name","q")
    serachbox.send_keys("selenium grid")
    serachbox.submit()
    
    # Wait for the page to load and title to change from "Google"
    WebDriverWait(driver, 10).until(
        lambda d: "Google" != d.title
    )
    
    # Verify search was performed (title should contain search-related text)
    assert "selenium" in driver.title.lower() or "Google Search" in driver.title
    driver.quit()