from app.selenium_test.pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class AdminCouponPage(BasePage):
    URL_LIST = 'http://127.0.0.1:5000/admin/coupon/'
    URL_NEW = 'http://127.0.0.1:5000/admin/coupon/new/'

    CODE_INPUT = (By.ID, 'code')
    VALUE_INPUT = (By.ID, 'value')
    EXPIRY_INPUT = (By.ID, 'expiry_date')

    # APPLY_CALENDAR_BTN = (By.CSS_SELECTOR,
    #                       'body > div:nth-child(16) > div.ranges > div > button.applyBtn.btn.btn-small.btn-sm.btn-success')

    SAVE_BUTTON = (By.CSS_SELECTOR, 'input[value="Save"]')

    DELETE_BUTTON = (By.CSS_SELECTOR, 'form[action="/admin/coupon/delete/"] button')

    def open_new_page(self):
        self.open(self.URL_NEW)

    def open_list_page(self):
        self.open(self.URL_LIST)

    def create_coupon(self, code, value, expiry):
        self.typing(*self.CODE_INPUT, code)
        self.typing(*self.VALUE_INPUT, value)

        self.click(*self.EXPIRY_INPUT)
        expiry_elem = self.find(*self.EXPIRY_INPUT)
        self.driver.execute_script(f"arguments[0].value = '{expiry}';", expiry_elem)
        # self.typing(*self.EXPIRY_INPUT, expiry)

        # self.click(*self.APPLY_CALENDAR_BTN)
        # self.find(*self.EXPIRY_INPUT).send_keys(Keys.ESCAPE)

        # self.click(*self.SAVE_BUTTON)
        save_btn = self.find(*self.SAVE_BUTTON)
        self.driver.execute_script("arguments[0].click();", save_btn)

    def delete_first_coupon(self):
        buttons = self.finds(*self.DELETE_BUTTON)
        if len(buttons) > 0:
            buttons[0].click()
        else:
            raise Exception("không tìm thấy mã giảm giá nào để xóa")