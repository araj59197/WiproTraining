from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
def main():
    driver = webdriver.Chrome()
    vars = {}

    try:
        driver.get("https://tutorialsninja.com/demo/")
        WebDriverWait(driver, 30).until(lambda d: d.title)
        vars["title1"] = driver.title
        print(f"Step 1 - Initial Page Title: {vars['title1']}")

        driver.get("https://tutorialsninja.com/demo/index.php?route=account/register")
        WebDriverWait(driver, 30).until(
            lambda d: "route=account/register" in d.current_url
        )
        WebDriverWait(driver, 30).until(lambda d: d.title)
        vars["title2"] = driver.title
        print(f"Step 2 - Second Page Title: {vars['title2']}")

        driver.execute_script("window.history.back();")
        WebDriverWait(driver, 30).until(lambda d: d.title)
        vars["title3"] = driver.title
        print(f"Step 3 - After back() Title: {vars['title3']}")

        driver.execute_script("window.history.forward();")
        WebDriverWait(driver, 30).until(lambda d: d.title)
        vars["title4"] = driver.title
        print(f"Step 4 - After forward() Title: {vars['title4']}")

        driver.execute_script("window.location.reload();")
        WebDriverWait(driver, 30).until(lambda d: d.title)
        vars["title5"] = driver.title
        print(f"Step 5 - After refresh() Title: {vars['title5']}")

        print("========================================")
        print("✓ Browser Navigation Test Completed! Browser will be closed.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
