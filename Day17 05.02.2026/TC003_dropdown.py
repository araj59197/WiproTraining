from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


driver = webdriver.Firefox()
driver.get("https://www.tutorialsninja.com/demo/")

driver.find_element(By.LINK_TEXT, "Desktops").click()
driver.find_element(By.LINK_TEXT, "Mac (1)").click()

dropdown = Select(driver.find_element(By.ID, "input-sort"))

options = dropdown.options
print("Available dropdown options:")
for option in options:
    print(f"  - {option.text}")

print("\nSelecting option at index 4...")
dropdown.select_by_index(4)

dropdown_after = Select(driver.find_element(By.ID, "input-sort"))
print(f"Selected option: {dropdown_after.first_selected_option.text}")

driver.quit()

