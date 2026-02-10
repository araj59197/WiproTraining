from selenium import webdriver

GRIDURL="http://192.168.1.9:4444/wd/hub"

def getdriver(browser):
    if browser=="chrome":
        options = webdriver.ChromeOptions()
        # Anti-detection options to avoid Google CAPTCHA
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
    elif browser=="edge":
        options = webdriver.EdgeOptions()
        # Anti-detection options to avoid edge CAPTCHA
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
    else:
        raise ValueError("Browser not supported")
    
    driver = webdriver.Remote(
        command_executor=GRIDURL,
        options=options
    )
    driver.maximize_window()
    return driver


    