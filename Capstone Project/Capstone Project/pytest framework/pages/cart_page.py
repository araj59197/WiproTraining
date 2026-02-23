from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    FIRST_GRID_ITEM = (By.CSS_SELECTOR, ".product-item .product-title a")
    ADD_TO_CART_BTN = (By.XPATH, "//button[contains(@class, 'add-to-cart-button')]")
    ADD_TO_WISHLIST_BTN = (By.XPATH, "//button[contains(@class, 'add-to-wishlist-button')]")
    QTY_INPUT = (By.CLASS_NAME, "qty-input")
    UPDATE_CART_BTN = (By.ID, "updatecart")
    REMOVE_BTN = (By.CLASS_NAME, "remove-btn")
    SUBTOTAL = (By.CLASS_NAME, "product-subtotal")
    PAGE_TITLE = (By.TAG_NAME, "h1")

    def select_first_item(self):
        self.wait.until(EC.presence_of_element_located(self.FIRST_GRID_ITEM))
        self.click_element(self.FIRST_GRID_ITEM)

    def add_current_item_to_cart(self):
        self.click_element(self.ADD_TO_CART_BTN)

    def add_current_item_to_wishlist(self):
        self.click_element(self.ADD_TO_WISHLIST_BTN)

    def update_quantity(self, qty):
        self.enter_text(self.QTY_INPUT, qty)
        self.click_element(self.UPDATE_CART_BTN)

    def remove_item(self):
        # Check if remove button exists first
        btns = self.driver.find_elements(*self.REMOVE_BTN)
        if btns:
            self.driver.execute_script("arguments[0].click();", btns[0])

    def has_items(self):
        return len(self.driver.find_elements(*self.SUBTOTAL)) > 0