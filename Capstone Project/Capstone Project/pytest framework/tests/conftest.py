import pytest
import os
import sys
import glob
import time
import configparser
import argparse
import psutil
import re
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

def _first_existing_path(paths):
    for path in paths:
        if path and os.path.exists(path):
            return path
    return None


def _get_file_major_version(exe_path: str | None) -> int | None:
    if not exe_path or not os.path.exists(exe_path):
        return None
    try:
        # PowerShell is reliable for extracting FileVersion on Windows.
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f"(Get-Item '{exe_path}').VersionInfo.ProductVersion",
        ]
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
        m = re.match(r"^(\d+)\.", out)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def _find_cached_driver(cache_root: str, driver_subdir: str, exe_name: str, major: int | None = None) -> str | None:
    r"""Find a cached driver under Selenium Manager cache.

    Example cache_root: %USERPROFILE%\.cache\selenium
    driver_subdir: chromedriver or msedgedriver
    """
    base = os.path.join(cache_root, driver_subdir)
    if not os.path.isdir(base):
        return None

    matches: list[str] = []
    for root, _dirs, files in os.walk(base):
        if exe_name in files:
            exe_path = os.path.join(root, exe_name)
            # Expect version in path like ...\win64\145.0.7632.77\chromedriver.exe
            if major is not None:
                if f"\\{major}." not in exe_path and f"/{major}." not in exe_path:
                    continue
            matches.append(exe_path)

    if not matches:
        return None

    # Prefer most recently modified binary.
    matches.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return matches[0]


def _create_chrome_driver() -> webdriver.Chrome:
    chrome_exe = _first_existing_path(
        [
            os.path.join(os.environ.get("ProgramFiles", ""), "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"),
        ]
    )
    chrome_major = _get_file_major_version(chrome_exe)

    cache_root = os.path.join(os.path.expanduser("~"), ".cache", "selenium")
    chromedriver_path = _find_cached_driver(cache_root, "chromedriver", "chromedriver.exe", major=chrome_major)

    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    if chrome_exe:
        options.binary_location = chrome_exe

    if chromedriver_path:
        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        # As a fallback, allow Selenium Manager to resolve (may require network).
        driver = webdriver.Chrome(options=options)

    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )
    except Exception:
        pass
    return driver


def _create_edge_driver() -> webdriver.Edge:
    edge_exe = _first_existing_path(
        [
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Microsoft", "Edge", "Application", "msedge.exe"),
            os.path.join(os.environ.get("ProgramFiles", ""), "Microsoft", "Edge", "Application", "msedge.exe"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Edge", "Application", "msedge.exe"),
        ]
    )
    edge_major = _get_file_major_version(edge_exe)
    cache_root = os.path.join(os.path.expanduser("~"), ".cache", "selenium")
    msedgedriver_path = _find_cached_driver(cache_root, "msedgedriver", "msedgedriver.exe", major=edge_major)
    edge_options = EdgeOptions()
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-popup-blocking")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option("useAutomationExtension", False)

    if edge_exe:
        edge_options.binary_location = edge_exe

    if msedgedriver_path:
        service = EdgeService(executable_path=msedgedriver_path)
        driver = webdriver.Edge(service=service, options=edge_options)
    else:
        # Fallback: allow Selenium Manager to resolve (may require network).
        driver = webdriver.Edge(options=edge_options)
    try:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )
    except Exception:
        pass
    return driver

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from utilities.data_loader import load_kv_csv

DATA_DIR = os.path.join(BASE_DIR, "data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)

# ---------------- CONFIG READER ---------------- #

CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.ini")
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# ---------------- CLI OPTIONS ---------------- #

def pytest_addoption(parser):
    try:
        parser.addoption(
            "--browser",
            action="store",
            default=None,
            choices=["chrome", "edge", "both"],
            help="Browser to use: chrome, edge, or both (overrides config.ini)"
        )
    except argparse.ArgumentError:
        pass

# ---------------- TERMINAL LOG FILE ---------------- #

def pytest_configure(config):
    log_file = os.path.join(REPORT_DIR, "pytest_terminal_output.txt")
    with open(log_file, "w") as f:
        f.write(f"PYTEST EXECUTION LOG\nStarted: {time.ctime()}\n====================\n")

# ---------------- DYNAMIC CSV PARAMETRIZATION ---------------- #

def pytest_generate_tests(metafunc):
    if "setup" in metafunc.fixturenames:
        csv_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))
        # Parameterize by CSV *and* (optionally) by browser.
        # - Default: uses config.ini browser (single browser)
        # - --browser=chrome|edge: single browser
        # - --browser=both: runs each CSV on both browsers
        cli_browser = None
        if "--browser" in sys.argv or any(arg.startswith("--browser=") for arg in sys.argv):
            cli_browser = metafunc.config.getoption("--browser")

        cfg_browser = config.get("DEFAULT", "browser", fallback="chrome")
        requested = (cli_browser or cfg_browser or "chrome").strip().lower()

        if requested == "both":
            browsers = ["chrome", "edge"]
        else:
            browsers = [requested]

        params = [(csv_path, browser) for csv_path in csv_files for browser in browsers]
        metafunc.parametrize("setup", params, indirect=True)

# ---------------- FORCE BROWSER TERMINATION ---------------- #

def kill_browser_process(driver):
    try:
        if driver and driver.service and driver.service.process:
            pid = driver.service.process.pid
            driver.quit()
            if psutil.pid_exists(pid):
                proc = psutil.Process(pid)
                for child in proc.children(recursive=True):
                    child.terminate()
                proc.terminate()
    except:
        pass

# ---------------- MAIN FIXTURE ---------------- #

@pytest.fixture(scope="class")
def setup(request):
    if isinstance(request.param, (tuple, list)) and len(request.param) == 2:
        csv_path, browser = request.param
    else:
        csv_path, browser = request.param, None
    test_data = load_kv_csv(csv_path)

    # Determine browser from parametrization, CLI, or config.
    if not browser:
        if "--browser" in sys.argv or any(arg.startswith("--browser=") for arg in sys.argv):
            browser = request.config.getoption("--browser").lower()
        else:
            browser = config.get("DEFAULT", "browser", fallback="chrome").lower()

    if browser == "both":
        # Safety net; should be expanded by pytest_generate_tests.
        browser = "chrome"

    driver = None

    implicit_wait = config.getint("DEFAULT", "implicit_wait", fallback=5)
    explicit_wait = config.getint("DEFAULT", "explicit_wait", fallback=10)
    base_url = config.get("DEFAULT", "base_url", fallback=test_data.get("base_url"))

    def _configure_driver(drv):
        drv.set_page_load_timeout(45)
        drv.implicitly_wait(implicit_wait)
        # Used by BasePage to configure WebDriverWait.
        drv._explicit_wait = explicit_wait

    def _create_driver_for_browser():
        if browser == "edge":
            try:
                return _create_edge_driver()
            except Exception:
                # Fall back to Chrome using cached ChromeDriver.
                return _create_chrome_driver()
        return _create_chrome_driver()

    def _start_new_driver():
        nonlocal driver
        driver = _create_driver_for_browser()
        _configure_driver(driver)
        request.cls.driver = driver
        request.cls.data = test_data
        try:
            driver.get(base_url)
            # Wait out initial Cloudflare check if present
            time.sleep(3)
        except Exception:
            pass
        return driver

    def _restart_driver():
        """Restart the underlying browser session and re-attach to the test class."""
        nonlocal driver
        try:
            kill_browser_process(driver)
        except Exception:
            pass
        return _start_new_driver()

    _start_new_driver()

    # Expose helpers to tests (callable with no args).
    # Must be a staticmethod to avoid Python binding it as an instance method.
    request.cls._restart_driver = staticmethod(_restart_driver)
    request.cls._base_url = base_url
    request.cls._browser = browser

    yield

    kill_browser_process(driver)

# ---------------- LOG PASS/FAIL TO FILE ---------------- #

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    if report.when == "call":
        log_path = os.path.join(REPORT_DIR, "pytest_terminal_output.txt")
        status = "PASS" if report.passed else "FAIL"
        try:
            with open(log_path, "a") as f:
                f.write(f"{status}: {report.nodeid}\n")
        except:
            pass