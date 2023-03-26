from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest
from datetime import date
from pathlib import Path
from selenium.webdriver.common.action_chains import ActionChains


class Test_sauce:
    # calls before test
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        self.folder_path = str(date.today())
        Path(self.folder_path).mkdir(exist_ok=True)

    # calls after test
    def teardown_method(self):
        self.driver.quit()

    def wait_for_element_visible(self, locator, timeout=5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))

    def test_no_name_and_password(self):
        self.wait_for_element_visible((By.ID, "login-button"))
        login_btn = self.driver.find_element(By.ID, "login-button")
        login_btn.click()

        error_message = self.driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")

        screenshot_file_path = str(Path(self.folder_path) / f"test-no-name-password.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_message.text == "Epic sadface: Username is required"

    @pytest.mark.parametrize("username", ["akcanbasri", "user"])
    def test_only_username(self, username):
        self.wait_for_element_visible((By.ID, "user-name"))
        user_name_input = self.driver.find_element(By.ID, "user-name")
        user_name_input.send_keys(username)

        self.wait_for_element_visible((By.ID, "login-button"))
        login_btn = self.driver.find_element(By.ID, "login-button")
        login_btn.click()

        error_message = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3")

        screenshot_file_path = str(Path(self.folder_path) / f"test-only-user-name-{username}.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_message.text == "Epic sadface: Password is required"

    def test_banned_account(self):
        self.wait_for_element_visible((By.ID, "user-name"))
        name_input = self.driver.find_element(By.ID, "user-name")

        self.wait_for_element_visible((By.ID, "password"))
        password_input = self.driver.find_element(By.ID, "password")

        action = ActionChains(self.driver)
        action.send_keys_to_element(name_input, "locked_out_user")
        action.send_keys_to_element(password_input, "secret_sauce")
        action.perform()

        login_btn = self.driver.find_element(By.ID, "login-button")
        login_btn.click()

        error_message = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3")

        screenshot_file_path = str(Path(self.folder_path) / f"test-banned-account.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_message.text == "Epic sadface: Sorry, this user has been locked out."

    @pytest.mark.parametrize("username,password", [("standard_user", "secret_sauce")])
    def test_correct_login(self, username, password):
        self.wait_for_element_visible((By.ID, "user-name"))
        name_input = self.driver.find_element(By.ID, "user-name")
        name_input.send_keys(username)

        self.wait_for_element_visible((By.ID, "password"))
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(password)

        login_btn = self.driver.find_element(By.ID, "login-button")
        login_btn.click()

        url = "https://www.saucedemo.com/inventory.html"

        screenshot_file_path = str(Path(self.folder_path) / f"test-correct-login-{username}-{password}.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == url

    def test_counting_products(self):
        total_product = 6
        self.test_correct_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.CLASS_NAME, "inventory_item"))
        list_product = self.driver.find_elements(By.CLASS_NAME, "inventory_item")

        screenshot_file_path = str(Path(self.folder_path) / f"test-counting-products.png")
        self.driver.save_screenshot(screenshot_file_path)
        assert len(list_product) == total_product

    def test_x_icon(self):
        self.wait_for_element_visible((By.ID, "login-button"))
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        error_button = self.driver.find_element(By.CLASS_NAME, "error-button")
        
        screenshot_file_path = str(Path(self.folder_path) / f"test-error-icon.png")
        self.driver.save_screenshot(screenshot_file_path)
        
        error_icon = len(self.driver.find_elements(By.CLASS_NAME, "error_icon"))
        error_button.click()
        assert error_icon > 0

    # Sorting Z to A.
    def test_order_product_z_to_a(self):
        self.test_correct_login("standard_user", "secret_sauce")

        name_of_product_before = list()
        self.wait_for_element_visible((By.CLASS_NAME, "inventory_item_name"))
        list_product = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        for i in list_product:
            name_of_product_before.append(i.text)
        name_of_product_before.sort(reverse=True)

        self.wait_for_element_visible((By.CLASS_NAME, "product_sort_container"))
        order_opt = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
        order_opt.click()

        self.wait_for_element_visible((By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/span/select/option[2]"))
        z_to_a = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/span/select/option[2]")
        z_to_a.click()

        name_of_product_after = list()
        self.wait_for_element_visible((By.CLASS_NAME, "inventory_item_name"))
        list_product = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        for i in list_product:
            name_of_product_after.append(i.text)

        screenshot_file_path = str(Path(self.folder_path) / f"test-sorting-z-to-a.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert name_of_product_before == name_of_product_after

    # To quit from your account
    def test_logout(self):
        self.test_correct_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.ID, "react-burger-menu-btn"))
        menubar = self.driver.find_element(By.ID, "react-burger-menu-btn")
        menubar.click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-logout.png")
        self.driver.save_screenshot(screenshot_file_path)

        self.wait_for_element_visible((By.ID, "logout_sidebar_link"))
        logout_btn = self.driver.find_element(By.ID, "logout_sidebar_link")
        logout_btn.click()

        assert self.driver.current_url == "https://www.saucedemo.com/"
        
    # Adding cart
    def test_add_cart(self):
        self.test_correct_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.ID, "add-to-cart-sauce-labs-backpack"))
        add_cart_btn = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_cart_btn.click()

        see_cart = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        see_cart.click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-add-cart-to-a.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == "https://www.saucedemo.com/cart.html"
