import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # Allow tests to override the explicit wait via attribute on driver.
        timeout = getattr(self.driver, "_explicit_wait", 10)
        self.wait = WebDriverWait(self.driver, timeout)

    def open_url(self, url):
        self.driver.get(url)

    def click_element(self, locator):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
        except Exception:
            # Fallback: wait for presence, then JS-click (helps with overlays)
            try:
                element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(locator))
            except Exception:
                element = self.driver.find_element(*locator)
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            except Exception:
                pass
            self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, locator, text):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
        except Exception:
            try:
                element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(locator))
            except Exception:
                element = self.driver.find_element(*locator)
            self.driver.execute_script(f"arguments[0].value = '{text}';", element)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", element)

    def get_element_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def capture_screenshot(self, name):
        timestamp = int(time.time())
        base_dir = os.path.join(os.getcwd(), "screenshots", "Pytest screenshots")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        filename = f"{name}_{timestamp}.png"
        full_path = os.path.join(base_dir, filename)
        time.sleep(0.5) 
        self.driver.save_screenshot(full_path)
        return full_path

    def select_dropdown_by_text(self, locator, visible_text: str):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
        except Exception:
            # Be less strict for browsers that report visibility/clickability differently.
            element = WebDriverWait(self.driver, getattr(self.driver, "_explicit_wait", 10)).until(
                EC.presence_of_element_located(locator)
            )

        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        except Exception:
            pass

        try:
            Select(element).select_by_visible_text(visible_text)
            return
        except Exception:
            # Fallback: set value via JS and dispatch change.
            self.driver.execute_script(
                """
                const select = arguments[0];
                const text = (arguments[1] || '').trim();
                const opts = Array.from(select.options || []);
                const opt = opts.find(o => (o.textContent || '').trim() === text);
                if (!opt) { throw new Error('Option not found: ' + text); }
                select.value = opt.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                """,
                element,
                visible_text,
            )