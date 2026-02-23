import csv
import os
import subprocess
import re
import undetected_chromedriver as uc
from robot.api.deco import keyword
from selenium import webdriver


class StealthLib:
    def __init__(self):
        self.driver = None
        self._last_url = None
        self._last_browser = "chrome"

    @keyword("Get Csv Data")
    def get_csv_data(self, file_path):
        data = {}
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    data[row[0].strip()] = row[1].strip()
        return data

    def _detect_chrome_version(self):
        """Auto-detect the installed Chrome major version."""
        try:
            # Windows: query registry for Chrome version
            result = subprocess.run(
                ['reg', 'query',
                 r'HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon',
                 '/v', 'version'],
                capture_output=True, text=True, timeout=10
            )
            match = re.search(r'(\d+)\.\d+\.\d+\.\d+', result.stdout)
            if match:
                return int(match.group(1))
        except Exception:
            pass
        # Fallback: let undetected_chromedriver auto-detect
        return None

    @keyword("Open Stealth Browser")
    def open_stealth_browser(self, url, browser="chrome"):
        """
        Open a browser for Robot tests.

        Default is Chrome via undetected_chromedriver.
        Pass browser=edge to use Microsoft Edge.
        """
        browser = str(browser).lower()
        self._last_url = url
        self._last_browser = browser

        if browser == "edge":
            from selenium.webdriver.edge.options import Options as EdgeOptions

            edge_options = EdgeOptions()
            edge_options.add_argument("--start-maximized")
            edge_options.add_argument("--disable-popup-blocking")
            self.driver = webdriver.Edge(options=edge_options)
        else:
            options = uc.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            # Auto-detect Chrome version instead of hardcoding
            chrome_ver = self._detect_chrome_version()
            if chrome_ver:
                self.driver = uc.Chrome(options=options, version_main=chrome_ver)
            else:
                self.driver = uc.Chrome(options=options)

        self.driver.get(url)
        # Register the driver with Robot's SeleniumLibrary
        from robot.libraries.BuiltIn import BuiltIn

        sl = BuiltIn().get_library_instance('SeleniumLibrary')
        sl.register_driver(self.driver, 'stealth_browser')
        return self.driver

    @keyword("Recover Browser If Needed")
    def recover_browser_if_needed(self):
        """Check if the browser session is alive. If not, reopen it."""
        try:
            # Simple check — if this throws, session is dead
            _ = self.driver.title
            return False  # no recovery needed
        except Exception:
            # Session is dead — reopen
            try:
                self.driver.quit()
            except Exception:
                pass
            from robot.libraries.BuiltIn import BuiltIn
            sl = BuiltIn().get_library_instance('SeleniumLibrary')
            # Remove dead driver reference
            try:
                sl.close_all_browsers()
            except Exception:
                pass

            url = self._last_url or "https://demo.nopcommerce.com"
            browser = self._last_browser or "chrome"

            if browser == "edge":
                from selenium.webdriver.edge.options import Options as EdgeOptions
                edge_options = EdgeOptions()
                edge_options.add_argument("--start-maximized")
                edge_options.add_argument("--disable-popup-blocking")
                self.driver = webdriver.Edge(options=edge_options)
            else:
                options = uc.ChromeOptions()
                options.add_argument('--start-maximized')
                options.add_argument('--disable-popup-blocking')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')
                chrome_ver = self._detect_chrome_version()
                if chrome_ver:
                    self.driver = uc.Chrome(options=options, version_main=chrome_ver)
                else:
                    self.driver = uc.Chrome(options=options)

            self.driver.get(url)
            sl.register_driver(self.driver, 'stealth_browser')
            return True  # recovery happened

    @keyword("Close Stealth Browser")
    def close_stealth_browser(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass