from app.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

class RegisterPage(BasePage):
    URL = 'http://127.0.0.1:5000/register'

    NAME_INPUT = (By.ID, 'name')
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    CONFIRM_INPUT = (By.ID, 'confirm')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'form[action="/register"] button[type="submit"]')

    def open_page(self, url=None):
        self.open(url if url else self.URL)

    def register(self, name, username, password, confirm):
        self.typing(*self.NAME_INPUT, name)
        self.typing(*self.USERNAME_INPUT, username)
        self.typing(*self.PASSWORD_INPUT, password)
        self.typing(*self.CONFIRM_INPUT, confirm)
        self.click(*self.SUBMIT_BUTTON)