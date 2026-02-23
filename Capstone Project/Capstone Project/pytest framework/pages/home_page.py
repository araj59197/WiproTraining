from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class HomePage(BasePage):
    # Locators
    REGISTER_LINK = (By.CLASS_NAME, "ico-register")
    LOGOUT_LINK = (By.CLASS_NAME, "ico-logout")
    WISHLIST_LINK = (By.CLASS_NAME, "ico-wishlist")
    CART_LINK = (By.CLASS_NAME, "ico-cart")
    SEARCH_BOX = (By.ID, "small-searchterms")
    SEARCH_BTN = (By.CSS_SELECTOR, ".search-box-button")
    CURRENCY_DROPDOWN = (By.ID, "customerCurrency")
    HOME_LOGO = (By.XPATH, "//div[@class='header-logo']//img")
    
    # Sort/Display Locators
    SORT_DROPDOWN = (By.ID, "products-orderby")
    SIZE_DROPDOWN = (By.ID, "products-pagesize")
    
    # Footer Links
    LINK_SITEMAP = (By.LINK_TEXT, "Sitemap")
    LINK_SHIPPING = (By.LINK_TEXT, "Shipping & returns")
    LINK_PRIVACY = (By.LINK_TEXT, "Privacy notice")
    LINK_ABOUT = (By.LINK_TEXT, "About us")
    LINK_CONTACT = (By.LINK_TEXT, "Contact us")

    def nav_to_home(self):
        if self.is_visible(self.HOME_LOGO):
            self.click_element(self.HOME_LOGO)
        else:
            self.driver.get("https://demo.nopcommerce.com/")

    def nav_to_register(self):
        self.click_element(self.REGISTER_LINK)

    def nav_to_cart(self):
        self.click_element(self.CART_LINK)

    def nav_to_wishlist(self):
        # Wait for the link to be clickable (handles notification bar overlap)
        self.wait.until(EC.element_to_be_clickable(self.WISHLIST_LINK)).click()

    def logout(self):
        if self.is_visible(self.LOGOUT_LINK):
            self.click_element(self.LOGOUT_LINK)

    def search_for_product(self, query):
        # Ensure search box is interactable
        box = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BOX))
        box.clear()
        time.sleep(0.2)
        box.send_keys(query)
        self.click_element(self.SEARCH_BTN)

    def switch_currency(self, currency_name):
        self.select_dropdown_by_text(self.CURRENCY_DROPDOWN, currency_name)

    def sort_products(self, sort_text):
        self.select_dropdown_by_text(self.SORT_DROPDOWN, sort_text)
        
    def change_display_size(self, size_text):
        self.select_dropdown_by_text(self.SIZE_DROPDOWN, size_text)