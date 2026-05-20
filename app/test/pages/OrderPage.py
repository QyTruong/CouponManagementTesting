from app.test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By
class OrderPage(BasePage):
    URL = 'http://127.0.0.1:5000/orders'
    PAY_BUTTONS = (By.CSS_SELECTOR, 'td button.btn-primary')
    def open_page(self):
        self.open(self.URL)
    def pay_first_order(self):
        buttons = self.finds(*self.PAY_BUTTONS)
        if len(buttons) > 0:
            buttons[0].click()
        else:
            raise Exception("Không tìm thấy đơn hàng nào cần thanh toán")