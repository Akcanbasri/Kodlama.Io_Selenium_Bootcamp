# libraries which will we need
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest
from datetime import date
from pathlib import Path
from selenium.webdriver.common.action_chains import ActionChains
from Homework_6.Constants import constants
from selenium.webdriver.support.ui import Select
from time import sleep


# Class name
class Test_sauce:
    # calls before test
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(constants.URL)
        self.folder_path = str(date.today())
        Path(self.folder_path).mkdir(exist_ok=True)

    # calls after test
    def teardown_method(self):
        self.driver.quit()

    # wait method for all tests
    def wait_for_element_visible(self, locator, timeout=5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))

    # testing about site's about page
    def test_about(self):
        self.test_valid_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.ID, constants.menu_btn_id))
        menu_btn = self.driver.find_element(By.ID, constants.menu_btn_id)
        menu_btn.click()

        self.wait_for_element_visible((By.ID, constants.about_btn_id))
        self.driver.find_element(By.ID, constants.about_btn_id).click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-about-page.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.saucelab_about_url

    # testing about banned account
    @pytest.mark.parametrize("username,password", [("locked_out_user", "secret_sauce")])
    def test_banned_account(self, username, password):
        self.wait_for_element_visible((By.ID, constants.user_id))
        name_input = self.driver.find_element(By.ID, constants.user_id)

        self.wait_for_element_visible((By.ID, constants.password_id))
        password_input = self.driver.find_element(By.ID, constants.password_id)

        action = ActionChains(self.driver)
        action.send_keys_to_element(name_input, username)
        action.send_keys_to_element(password_input, password)
        action.perform()

        login_btn = self.driver.find_element(By.ID, constants.login_id)
        login_btn.click()

        self.wait_for_element_visible((By.XPATH, constants.error_msg_box_full_path))
        error_msg = self.driver.find_element(By.XPATH, constants.error_msg_box_full_path)

        screenshot_file_path = str(Path(self.folder_path) / f"test-banned-account-{username}-{password}.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_msg.text == constants.banned_account_message

    # testing about invalid login
    @pytest.mark.parametrize("username,password", [("1", "1"), ("kodlama.io", "123")])
    def test_invalid_login(self, username, password):
        self.wait_for_element_visible((By.ID, constants.user_id))
        name_input = self.driver.find_element(By.ID, constants.user_id)

        self.wait_for_element_visible((By.ID, constants.password_id))
        password_input = self.driver.find_element(By.ID, constants.password_id)

        action = ActionChains(self.driver)
        action.send_keys_to_element(name_input, username)
        action.send_keys_to_element(password_input, password)
        action.perform()

        login_btn = self.driver.find_element(By.ID, constants.login_id)
        login_btn.click()

        self.wait_for_element_visible((By.XPATH, constants.error_msg_box_full_path))
        error_msg = self.driver.find_element(By.XPATH, constants.error_msg_box_full_path)

        screenshot_file_path = str(Path(self.folder_path) / f"test-invalid-login-{username}-{password}.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_msg.text == constants.unmatched_username_password_text

    # testing about login pace only click to login button
    def test_just_click_login(self):
        self.wait_for_element_visible((By.ID, constants.login_id))
        login_btn = self.driver.find_element(By.ID, constants.login_id)
        login_btn.click()

        self.wait_for_element_visible((By.XPATH, constants.error_msg_box_full_path))
        error_msg = self.driver.find_element(By.XPATH, constants.error_msg_box_full_path)

        screenshot_file_path = str(Path(self.folder_path) / f"test-only-click-login.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_msg.text == constants.just_clik_message

    # testing about login with valid information
    @pytest.mark.parametrize("username,password", [("standard_user", "secret_sauce")])
    def test_valid_login(self, username, password):
        self.wait_for_element_visible((By.ID, constants.user_id))
        username_input = self.driver.find_element(By.ID, constants.user_id)
        username_input.click()
        username_input.send_keys(username)

        self.wait_for_element_visible((By.ID, constants.password_id))
        password_input = self.driver.find_element(By.ID, constants.password_id)
        password_input.click()
        password_input.send_keys(password)
        self.wait_for_element_visible((By.ID, constants.login_id))
        self.driver.find_element(By.ID, constants.login_id).click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-valid-login-{username}-{password}.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.product_list_url

    # testing about logout
    def test_logout(self):
        self.test_valid_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.ID, constants.menu_btn_id))
        menu_btn = self.driver.find_element(By.ID, constants.menu_btn_id)
        menu_btn.click()

        self.wait_for_element_visible((By.ID, constants.logout_btn_id))
        logout_btn = self.driver.find_element(By.ID, constants.logout_btn_id)

        screenshot_file_path = str(Path(self.folder_path) / f"test-logout.png")
        self.driver.save_screenshot(screenshot_file_path)

        logout_btn.click()

        assert self.driver.current_url == constants.URL

    # Testing for login only using username
    @pytest.mark.parametrize("username", [("1"), ("kodlama.io")])
    def test_only_username(self, username):
        self.wait_for_element_visible((By.ID, constants.user_id))
        username_input = self.driver.find_element(By.ID, constants.user_id)
        username_input.click()
        username_input.send_keys(username)

        self.wait_for_element_visible((By.ID, constants.login_id))
        self.driver.find_element(By.ID, constants.login_id).click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-only-username-{username}.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.find_element(By.XPATH,
                                        "//h3[contains(.,\'Epic sadface: Password is required\')]"
                                        "").text == constants.only_username_message

    # Testing about problem user
    @pytest.mark.parametrize("username,password", [("problem_user", "secret_sauce")])
    def test_problem_user(self, username, password):
        self.wait_for_element_visible((By.ID, constants.user_id))
        username_input = self.driver.find_element(By.ID, constants.user_id)
        username_input.click()
        username_input.send_keys(username)

        self.wait_for_element_visible((By.ID, constants.password_id))
        password_input = self.driver.find_element(By.ID, constants.password_id)
        password_input.click()
        password_input.send_keys(password)

        self.wait_for_element_visible((By.ID, constants.login_id))
        self.driver.find_element(By.ID, constants.login_id).click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-problem-user-{username}-{password}.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.product_list_url

    # testing for total product
    def test_counting_products(self):
        total_product = 6
        self.test_valid_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.CLASS_NAME, constants.item_class_name))
        list_product = self.driver.find_elements(By.CLASS_NAME, constants.item_class_name)

        screenshot_file_path = str(Path(self.folder_path) / f"test-counting-products.png")
        self.driver.save_screenshot(screenshot_file_path)

        screenshot_file_path = str(Path(self.folder_path) / f"test-counting-products-a.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert len(list_product) == total_product

    # Testing for 'x' icon for invalid logins
    def test_x_icon(self):
        self.wait_for_element_visible((By.ID, constants.login_id))
        login_button = self.driver.find_element(By.ID, constants.login_id)
        login_button.click()
        error_button = self.driver.find_element(By.CLASS_NAME, constants.error_btn_id)

        screenshot_file_path = str(Path(self.folder_path) / f"test-error-icon.png")
        self.driver.save_screenshot(screenshot_file_path)

        error_icon = len(self.driver.find_elements(By.CLASS_NAME, constants.error_icon_class_name))
        error_button.click()

        assert error_icon > 0

    # test for sorting products from z to a
    def test_sort_product_z_to_a(self):
        self.test_valid_login("standard_user", "secret_sauce")
        name_of_product_before = list()

        self.wait_for_element_visible((By.CLASS_NAME, constants.item_class_name))
        list_product = self.driver.find_elements(By.CLASS_NAME, constants.item_class_name)
        for i in list_product:
            name_of_product_before.append(i.text)
        name_of_product_before.sort(reverse=True)

        self.wait_for_element_visible((By.CLASS_NAME, constants.order_menu_class_name))
        order_opt = self.driver.find_element(By.CLASS_NAME, constants.order_menu_class_name)
        order_opt.click()

        self.wait_for_element_visible((By.XPATH, constants.sorting_z_to_a_full_path))
        z_to_a = self.driver.find_element(By.XPATH, constants.sorting_z_to_a_full_path)
        z_to_a.click()

        name_of_product_after = list()
        self.wait_for_element_visible((By.CLASS_NAME, constants.item_class_name))
        list_product = self.driver.find_elements(By.CLASS_NAME, constants.item_class_name)
        for i in list_product:
            name_of_product_after.append(i.text)

        screenshot_file_path = str(Path(self.folder_path) / f"test-sorting-z-to-a.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert name_of_product_before == name_of_product_after

    # test for adding products to cart
    def test_add_cart(self):
        self.test_valid_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.ID, constants.add_cart_btn_id))
        add_cart_btn = self.driver.find_element(By.ID, constants.add_cart_btn_id)
        add_cart_btn.click()

        see_cart = self.driver.find_element(By.CLASS_NAME, constants.see_cart_id)
        see_cart.click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-add-cart-to-a.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.cart_url

    # testing for twitter link
    def test_go_twitter(self):
        self.test_valid_login("standard_user", "secret_sauce")
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

        self.wait_for_element_visible((By.XPATH, constants.twitter_btn_full_path))
        twitter_btn = self.driver.find_element(By.XPATH, constants.twitter_btn_full_path)
        twitter_btn.click()

        self.driver.switch_to.window(self.driver.window_handles[1])

        screenshot_file_path = str(Path(self.folder_path) / f"test-go-to-twitter.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.twitter_url

    # testing for facebook link
    def test_go_facebook(self):
        self.test_valid_login("standard_user", "secret_sauce")
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

        self.wait_for_element_visible((By.XPATH, constants.facebook_btn_full_path))
        facebook_btn = self.driver.find_element(By.XPATH, constants.facebook_btn_full_path)
        facebook_btn.click()

        self.driver.switch_to.window(self.driver.window_handles[1])

        screenshot_file_path = str(Path(self.folder_path) / f"test-go-to-facebook.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.facebook_url

    # testing for linkedin link
    def test_go_linkedin(self):
        self.test_valid_login("standard_user", "secret_sauce")
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

        self.wait_for_element_visible((By.XPATH, constants.linkedin_btn_full_path))
        linkedin_btn = self.driver.find_element(By.XPATH, constants.linkedin_btn_full_path)
        linkedin_btn.click()

        self.driver.switch_to.window(self.driver.window_handles[1])

        screenshot_file_path = str(Path(self.folder_path) / f"test-go-to-linkedin.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.linkedin_url

    # testing to reset cart
    def test_reset_app_state(self):
        self.test_valid_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.ID, constants.add_cart_btn_id))
        add_btn_to_cart = self.driver.find_element(By.XPATH,
                                                   constants.add_cart_full_path)
        add_btn_to_cart.click()

        self.wait_for_element_visible((By.ID, constants.menu_btn_id))
        menu_btn = self.driver.find_element(By.ID, constants.menu_btn_id)
        menu_btn.click()

        self.wait_for_element_visible((By.ID, constants.reset_btn_id))
        reset_btn = self.driver.find_element(By.ID, constants.reset_btn_id)

        screenshot_file_path = str(Path(self.folder_path) / f"test-reset-cart.png")
        self.driver.save_screenshot(screenshot_file_path)
        reset_btn.click()

        cart_after = self.driver.find_element(By.XPATH, constants.product_number_in_cart_full_path)

        assert cart_after.text == ""

    # testing for cart link
    def test_go_to_cart(self):
        self.test_valid_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.XPATH, constants.product_number_in_cart_full_path))
        cart_btn = self.driver.find_element(By.XPATH, constants.product_number_in_cart_full_path)
        cart_btn.click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-go-to-cart.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.cart_url

    # testing continue button while in cart
    def test_cont_shopping(self):
        self.test_go_to_cart()

        self.wait_for_element_visible((By.ID, constants.continue_btn_id))
        cont_btn = self.driver.find_element(By.ID, constants.continue_btn_id)

        screenshot_file_path = str(Path(self.folder_path) / f"test-continues-shopping.png")
        self.driver.save_screenshot(screenshot_file_path)

        cont_btn.click()

        assert self.driver.current_url == constants.product_list_url

    # Testing for checkout
    def test_checkout(self):
        self.test_go_to_cart()

        self.wait_for_element_visible((By.ID, constants.checkout_btn_id))
        check_btn = self.driver.find_element(By.ID, constants.checkout_btn_id)
        check_btn.click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-checkout-first-step.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.checkout_step_one_url

    # testing for checkout complete
    @pytest.mark.parametrize("first_name_in,last_name_in,zip_code_in", [("Kodlama,io", "Akcan", "42080")])
    def test_checkout_complete(self, first_name_in, last_name_in, zip_code_in):
        self.test_checkout()

        self.wait_for_element_visible((By.ID, constants.checkout_first_name_id))
        first_name = self.driver.find_element(By.ID, constants.checkout_first_name_id)
        first_name.send_keys(first_name_in)

        self.wait_for_element_visible((By.ID, constants.checkout_last_name_id))
        last_name = self.driver.find_element(By.ID, constants.checkout_last_name_id)
        last_name.click()
        last_name.send_keys(last_name_in)

        self.wait_for_element_visible((By.ID, constants.checkout_zipcode_id))
        zip_code = self.driver.find_element(By.ID, constants.checkout_zipcode_id)
        zip_code.click()
        zip_code.send_keys(zip_code_in)

        self.wait_for_element_visible((By.ID, constants.checkout_continue_btn_id))
        cont_btn2 = self.driver.find_element(By.ID, constants.checkout_continue_btn_id)
        cont_btn2.click()

        self.wait_for_element_visible((By.ID, constants.checkout_finih_btn_id))
        finish = self.driver.find_element(By.ID, constants.checkout_finih_btn_id)
        finish.click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-checkout-completed.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.checkout_finished_url

    # testing for back home button while in checkout
    def test_back_home(self):
        self.test_checkout_complete("Kodlama,io", "Akcan", "42080")
        self.wait_for_element_visible((By.ID, constants.checkout_back_home_btn_id))
        self.driver.find_element(By.ID, constants.checkout_back_home_btn_id).click()

        screenshot_file_path = str(Path(self.folder_path) / f"test-back-home.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert self.driver.current_url == constants.product_list_url

    # test checkout for empty continue
    def test_checkout_empty_continue(self):
        self.test_checkout()

        self.wait_for_element_visible((By.ID, constants.checkout_continue_btn_id))
        cont_btn2 = self.driver.find_element(By.ID, constants.checkout_continue_btn_id)
        cont_btn2.click()

        self.wait_for_element_visible((By.XPATH, constants.continue_error_messge_path))
        error_message = self.driver.find_element(By.XPATH, constants.continue_error_messge_path)

        screenshot_file_path = str(Path(self.folder_path) / f"test-empty-continue-click.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_message.text == "Error: First Name is required"

    # test checkout only first name for continue
    @pytest.mark.parametrize("first_name_in", ["Kodlama,io"])
    def test_checkout_only_first_name(self, first_name_in, ):
        self.test_checkout()

        self.wait_for_element_visible((By.ID, constants.checkout_first_name_id))
        first_name = self.driver.find_element(By.ID, constants.checkout_first_name_id)
        first_name.send_keys(first_name_in)

        self.wait_for_element_visible((By.ID, constants.checkout_continue_btn_id))
        cont_btn2 = self.driver.find_element(By.ID, constants.checkout_continue_btn_id)
        cont_btn2.click()

        self.wait_for_element_visible((By.XPATH, constants.continue_error_messge_path))
        error_message = self.driver.find_element(By.XPATH, constants.continue_error_messge_path)

        screenshot_file_path = str(Path(self.folder_path) / f"test-continuie-first name.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_message.text == "Error: Last Name is required"

    # test checkout firstname and lastname for continue
    @pytest.mark.parametrize("first_name_in,last_name_in", [("Kodlama,io", "Akcan")])
    def test_checkout_first_last_names(self, first_name_in, last_name_in):
        self.test_checkout()

        self.wait_for_element_visible((By.ID, constants.checkout_first_name_id))
        first_name = self.driver.find_element(By.ID, constants.checkout_first_name_id)
        first_name.send_keys(first_name_in)

        self.wait_for_element_visible((By.ID, constants.checkout_last_name_id))
        last_name = self.driver.find_element(By.ID, constants.checkout_last_name_id)
        last_name.click()
        last_name.send_keys(last_name_in)

        self.wait_for_element_visible((By.ID, constants.checkout_continue_btn_id))
        cont_btn2 = self.driver.find_element(By.ID, constants.checkout_continue_btn_id)
        cont_btn2.click()

        self.wait_for_element_visible((By.XPATH, constants.continue_error_messge_path))
        error_message = self.driver.find_element(By.XPATH, constants.continue_error_messge_path)

        screenshot_file_path = str(Path(self.folder_path) / f"test-continuie-first and last name.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_message.text == "Error: Postal Code is required"

    # test checkout firstname, zip code for continue
    @pytest.mark.parametrize("first_name_in,zip_code_in", [("Kodlama,io", "42080")])
    def test_checkout_firstname_zip(self, first_name_in, zip_code_in):
        self.test_checkout()

        self.wait_for_element_visible((By.ID, constants.checkout_first_name_id))
        first_name = self.driver.find_element(By.ID, constants.checkout_first_name_id)
        first_name.send_keys(first_name_in)

        self.wait_for_element_visible((By.ID, constants.checkout_zipcode_id))
        zip_code = self.driver.find_element(By.ID, constants.checkout_zipcode_id)
        zip_code.click()
        zip_code.send_keys(zip_code_in)

        self.wait_for_element_visible((By.ID, constants.checkout_continue_btn_id))
        cont_btn2 = self.driver.find_element(By.ID, constants.checkout_continue_btn_id)
        cont_btn2.click()

        self.wait_for_element_visible((By.XPATH, constants.continue_error_messge_path))
        error_message = self.driver.find_element(By.XPATH, constants.continue_error_messge_path)

        screenshot_file_path = str(Path(self.folder_path) / f"test-continuie-firtsname-zip-code.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_message.text == "Error: Last Name is required"

    # test checkout lastname, zip code for continue
    @pytest.mark.parametrize("last_name_in,zip_code_in", [("Akcan", "42080")])
    def test_checkout_lastname_zip(self, last_name_in, zip_code_in):
        self.test_checkout()

        self.wait_for_element_visible((By.ID, constants.checkout_last_name_id))
        last_name = self.driver.find_element(By.ID, constants.checkout_last_name_id)
        last_name.click()
        last_name.send_keys(last_name_in)

        self.wait_for_element_visible((By.ID, constants.checkout_zipcode_id))
        zip_code = self.driver.find_element(By.ID, constants.checkout_zipcode_id)
        zip_code.click()
        zip_code.send_keys(zip_code_in)

        self.wait_for_element_visible((By.ID, constants.checkout_continue_btn_id))
        cont_btn2 = self.driver.find_element(By.ID, constants.checkout_continue_btn_id)
        cont_btn2.click()

        self.wait_for_element_visible((By.XPATH, constants.continue_error_messge_path))
        error_message = self.driver.find_element(By.XPATH, constants.continue_error_messge_path)

        screenshot_file_path = str(Path(self.folder_path) / f"test-continuie-lastname-zip-code.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert error_message.text == "Error: First Name is required"
    # test for sorting product from low to high
    def test_lohi_filter(self):
        self.test_valid_login("standard_user", "secret_sauce")
        self.wait_for_element_visible((By.CLASS_NAME, constants.sort_btn_id))
        dropdown = self.driver.find_element(By.CLASS_NAME, constants.sort_btn_id)

        select = Select(dropdown)

        select.select_by_value("lohi")

        self.wait_for_element_visible((By.CLASS_NAME, "inventory_item_name"))
        item_name = self.driver.find_element(By.CLASS_NAME, "inventory_item_name")

        screenshot_file_path = str(Path(self.folder_path) / f"test-sorting-low-to-high.png")
        self.driver.save_screenshot(screenshot_file_path)

        assert item_name.text == "Sauce Labs Onesie"

    # test for sorting product from high to low
    def test_hilo_filter(self):
        self.test_valid_login("standard_user", "secret_sauce")

        self.wait_for_element_visible((By.CLASS_NAME, constants.sort_btn_id))
        dropdown = self.driver.find_element(By.CLASS_NAME, constants.sort_btn_id)

        select = Select(dropdown)

        select.select_by_value("hilo")

        self.wait_for_element_visible((By.CLASS_NAME, "inventory_item_name"))
        item_name = self.driver.find_element(By.CLASS_NAME, "inventory_item_name")

        screenshot_file_path = str(Path(self.folder_path) / f"test-sorting-high to low.png")
        self.driver.save_screenshot(screenshot_file_path)
        assert item_name.text == "Sauce Labs Fleece Jacket"
