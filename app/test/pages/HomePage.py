
from app.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    URL = 'http://127.0.0.1:5000/'

    SEARCH_INPUT = (By.CSS_SELECTOR, '#collapsibleNavbar > form > input')
    SEARCH_BUTTON = (By.CSS_SELECTOR, '#collapsibleNavbar > form > button')

    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, 'button.btn.btn-danger')

    def open_page(self):
        self.open(self.URL)

    def search(self, kw):
        self.typing(*self.SEARCH_INPUT, kw)
        self.click(*self.SEARCH_BUTTON)

    def add_to_cart(self):
        self.click(*self.ADD_TO_CART_BUTTON)




