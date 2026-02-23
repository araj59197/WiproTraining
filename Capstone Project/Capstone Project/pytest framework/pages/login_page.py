import time
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    GENDER_MALE = (By.ID, "gender-male")
    FIRSTNAME = (By.ID, "FirstName")
    LASTNAME = (By.ID, "LastName")
    EMAIL = (By.ID, "Email")
    PASSWORD = (By.ID, "Password")
    CONF_PASSWORD = (By.ID, "ConfirmPassword")
    REGISTER_BTN = (By.ID, "register-button")
    REG_RESULT = (By.CLASS_NAME, "result")
    CONTINUE_BTN = (By.CSS_SELECTOR, "a.register-continue-button")

    def register_new_user(self, fname, lname, pwd):
        self.click_element(self.GENDER_MALE)
        self.enter_text(self.FIRSTNAME, fname)
        self.enter_text(self.LASTNAME, lname)
        
        # Dynamic unique email
        email = f"test_{int(time.time())}@example.com"
        self.enter_text(self.EMAIL, email)
        
        self.enter_text(self.PASSWORD, pwd)
        self.enter_text(self.CONF_PASSWORD, pwd)
        self.click_element(self.REGISTER_BTN)

    def get_registration_result(self):
        return self.get_element_text(self.REG_RESULT)

    def click_continue(self):
        self.click_element(self.CONTINUE_BTN)