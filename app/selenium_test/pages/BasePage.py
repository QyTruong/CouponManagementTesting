class BasePage:
    def __init__(self,driver):
        self.driver = driver

    def open(self,url):
        self.driver.get(url)

    def find(self, by, value):
        return  self.driver.find_element(by,value)

    def finds(self, by, value):
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        self.find(by, value).click()

    def typing(self,by, value, text):
        e = self.find(by, value)
        e.send_keys(text)

    def select_dropdown_by_value(self, by, value, option_value):
        from selenium.webdriver.support.ui import Select
        e = self.find(by, value)
        Select(e).select_by_value(option_value)

    def select(self, by, value, option_value):
        e = self.find(by,value)

