from app.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class CartPage(BasePage):
    URL = 'http://127.0.0.1:5000/cart'

    COUPON_DROPDOWN = (By.CSS_SELECTOR, '#select-coupon')
    DISCOUNT = (By.CSS_SELECTOR,'.discount-value')
    FINAL_PRICE = (By.CSS_SELECTOR,'.final-price')
    ORDER_BUTTON = (By.CSS_SELECTOR, 'button.btn.btn-success')

    def open_page(self):
        self.open(self.URL)

    def apply_coupon(self,coupon):
        self.select_dropdown_by_value(*self.COUPON_DROPDOWN,coupon)

    def discount_coupon(self):
        return self.find(*self.DISCOUNT).text

    def final_price(self):
        return self.find(*self.FINAL_PRICE).text

    def order(self):
        self.click(*self.ORDER_BUTTON)

