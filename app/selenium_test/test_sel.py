import time

from app.selenium_test.pages.CartPage import CartPage
from app.selenium_test.pages.HomePage import HomePage
from app.selenium_test.pages.LoginPage import LoginPage
from app.selenium_test.pages.RegisterPage import RegisterPage
from app.selenium_test.pages.OrderPage import OrderPage
from app.selenium_test.pages.AdminCouponPage import AdminCouponPage
from app.test.test_base import driver
from selenium.webdriver.common.by import By


def test_search_products(driver):
    home = HomePage(driver=driver)
    kw = 'ao'
    home.open_page()
    home.search(kw)
    # driver.get('http://127.0.0.1:5000/')
    #
    # kw = 'ao'
    # search = driver.find_element(By.CSS_SELECTOR, '#collapsibleNavbar > form > input')
    # search.send_keys(kw)
    # btn = driver.find_element(By.CSS_SELECTOR, '#collapsibleNavbar > form > button')
    # btn.click()

    time.sleep(5)

    results = driver.find_elements(By.CSS_SELECTOR, '.card-title')

    for r in results:

        product_name = r.text.lower().replace('á', 'a')
        assert kw.lower() in product_name


def test_login_success(driver):
    login = LoginPage(driver=driver)
    login.open_page()
    login.login('user1', 'aaaa1111')

    time.sleep(1)

    assert driver.current_url == 'http://127.0.0.1:5000/'
    e = driver.find_element(By.CSS_SELECTOR, '#collapsibleNavbar > ul > span')
    assert 'user1' in e.text


def test_login_from_cart(driver):
    login = LoginPage(driver)
    login.open_page(url='http://127.0.0.1:5000/login?next=/cart')

    login.login('user1', 'aaaa1111')

    time.sleep(2)

    assert driver.current_url == 'http://127.0.0.1:5000/cart'
    e = driver.find_element(By.CSS_SELECTOR, '#collapsibleNavbar > ul > span')
    assert 'user1' in e.text


def test_apply_coupon_success(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user1', 'aaaa1111')

    time.sleep(2)

    home = HomePage(driver=driver)
    home.open_page()
    home.add_to_cart()
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    time.sleep(2)

    cart = CartPage(driver=driver)
    cart.open_page()
    cart.apply_coupon('SALE10')
    time.sleep(2)

    assert '10,000' in cart.discount_coupon()
    assert cart.final_price() != '0 VNĐ'


def test_coupon_limit(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user1', 'aaaa1111')
    time.sleep(2)

    home = HomePage(driver=driver)
    home.open_page()
    home.add_to_cart()
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    time.sleep(2)

    cart = CartPage(driver=driver)
    cart.open_page()
    cart.apply_coupon('SALE20')
    time.sleep(12)

    try:
        alert = driver.switch_to.alert
        err_msg = alert.text
        assert 'quá số lần ' in err_msg.lower()
        alert.accept()
    except:
        assert False, 'Có lỗi nhưng không thấy !'


def test_coupon_expired(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user1', 'aaaa1111')
    time.sleep(2)

    home = HomePage(driver=driver)
    home.open_page()
    home.add_to_cart()
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    time.sleep(2)

    cart = CartPage(driver=driver)
    cart.open_page()
    cart.apply_coupon('SALE15P')
    time.sleep(12)

    try:
        alert = driver.switch_to.alert
        err_msg = alert.text
        assert 'hết hạn' in err_msg.lower()
        alert.accept()
    except:
        assert False, 'Có lỗi nhưng không thấy !!'


def test_remove_coupon(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user1', 'aaaa1111')
    time.sleep(2)

    home = HomePage(driver=driver)
    home.open_page()
    home.add_to_cart()
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    time.sleep(2)

    cart = CartPage(driver=driver)
    cart.open_page()

    cart.apply_coupon('SALE10')
    time.sleep(5)
    assert '10,000' in cart.discount_coupon(), "Chua ap dung ma giam gia"

    cart.apply_coupon('no')
    time.sleep(5)

    assert '0' in cart.discount_coupon(), "Lỗi!"


def test_checkout_order(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user1', 'aaaa1111')
    time.sleep(1)

    home = HomePage(driver=driver)
    home.open_page()
    home.add_to_cart()
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    time.sleep(1)

    cart = CartPage(driver=driver)
    cart.open_page()

    cart.order()
    time.sleep(2)

    alert_confirm = driver.switch_to.alert.accept()
    time.sleep(5)

    alert_success = driver.switch_to.alert
    assert 'thành công' in alert_success.text.lower()
    alert_success.accept()
    time.sleep(5)

    page_text = driver.find_element(By.TAG_NAME, 'body').text
    assert 'không có sản phẩm nào' in page_text.lower()


def test_register_password_mismatch(driver):
    register = RegisterPage(driver=driver)
    register.open_page()
    register.register('Test User', 'testuser_fail', '123456', '654321')
    time.sleep(2)

    error_msg = driver.find_element(By.CSS_SELECTOR, '.alert.alert-danger').text
    assert 'mật khẩu không khớp' in error_msg.lower()


def test_register_success(driver):
    register = RegisterPage(driver=driver)
    register.open_page()

    register.register('Test User', 'testuser_new_6', 'aaaa1212', 'aaaa1212')
    time.sleep(2)

    assert 'login' in driver.current_url


def test_payment_redirect(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('user1', 'aaaa1111')
    time.sleep(2)

    home = HomePage(driver=driver)
    home.open_page()
    home.add_to_cart()
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    time.sleep(2)

    cart = CartPage(driver=driver)
    cart.open_page()
    cart.apply_coupon('SALE30P')
    time.sleep(12)

    cart.order()
    time.sleep(2)
    driver.switch_to.alert.accept()
    time.sleep(5)
    driver.switch_to.alert.accept()
    time.sleep(2)

    order_page = OrderPage(driver=driver)
    order_page.open_page()
    time.sleep(2)

    order_page.pay_first_order()

    time.sleep(8)
    assert 'stripe.com' in driver.current_url

def test_create_coupon(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('admin', '123456')
    time.sleep(2)

    admin_coupon = AdminCouponPage(driver=driver)
    admin_coupon.open_new_page()
    time.sleep(2)

    admin_coupon.create_coupon('SALEMOI2', '98000', '2026-12-31 23:59:59')
    time.sleep(3)

    assert '/admin/coupon/' in driver.current_url


def test_delete_coupon(driver):
    login = LoginPage(driver)
    login.open_page()
    login.login('admin', '123456')
    time.sleep(2)


    admin_coupon = AdminCouponPage(driver=driver)
    admin_coupon.open_list_page()
    time.sleep(2)

    admin_coupon.delete_first_coupon()
    time.sleep(2)

    driver.switch_to.alert.accept()
    time.sleep(3)

    assert '/admin/coupon/' in driver.current_url