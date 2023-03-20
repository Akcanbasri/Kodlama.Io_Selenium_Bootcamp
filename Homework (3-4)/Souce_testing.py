from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


# Main class for testing
class Test_sauce:
    # No name and password input
    @staticmethod
    def no_name_password():
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        login_btn = driver.find_element(By.ID, "login-button")
        login_btn.click()
        error_message = driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        test_result = error_message.text == "Epic sadface: Username is required"
        print(f"No input and password: {test_result}")
        driver.quit()

    # Only username input included
    @staticmethod
    def only_username():
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        name_input = driver.find_element(By.ID, "user-name")
        name_input.send_keys("1")
        login_btn = driver.find_element(By.ID, "login-button")
        login_btn.click()
        error_message = driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        test_message = error_message.text == "Epic sadface: Password is required"
        print(f"Only user name: {test_message}")
        driver.quit()

    # Login for banned account
    @staticmethod
    def banned_account():
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        name_input = driver.find_element(By.ID, "user-name")
        name_input.send_keys("locked_out_user")
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("secret_sauce")
        login_btn = driver.find_element(By.ID, "login-button")
        login_btn.click()
        error_message = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/form/div[3]/h3")
        test_message = error_message.text == "Epic sadface: Sorry, this user has been locked out."
        print(f"Banned Account: {test_message}")
        driver.quit()

    # Login for correct with infos
    @staticmethod
    def correct_login():
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        name_input = driver.find_element(By.ID, "user-name")
        name_input.send_keys("standard_user")
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("secret_sauce")
        login_btn = driver.find_element(By.ID, "login-button")
        login_btn.click()
        driver.get("https://www.saucedemo.com/inventory.html")
        assert "inventory.html" in driver.current_url, "Login unsuccessful or incorrect page loaded after login"
        driver.quit()
        return True

    # After login, counting products
    @staticmethod
    def counting_products():
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        sleep(2)
        name_input = driver.find_element(By.ID, "user-name")
        name_input.send_keys("standard_user")
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("secret_sauce")
        login_btn = driver.find_element(By.ID, "login-button")
        login_btn.click()
        driver.get("https://www.saucedemo.com/inventory.html")
        list_product = driver.find_elements(By.CLASS_NAME, "inventory_item")
        print(f"Total products: {len(list_product)}")
        driver.quit()

    # Testing empy inputs with red x buttons
    @staticmethod
    def test_empty_input_write_x():
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        login_btn = driver.find_element(By.ID, "login-button")
        login_btn.click()
        error = driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        if error.text != "Epic sadface: Username is required":
            return f"Test Result: {False}"
        x_icon_active = driver.find_elements(By.XPATH, "//div/*[@data-icon='times-circle']")
        if len(x_icon_active) == 0:
            return f"Test Result: {False}"
        error_exit_btn = driver.find_element(By.XPATH,
                                             "/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3/button")
        error_exit_btn.click()
        x_icon_passive = driver.find_elements(By.XPATH, "//div/*[@data-icon='times-circle']")
        if len(x_icon_passive) == 0:
            return f"Test Result: {True}"
        else:
            return f"Test Result: {False}"


# Main function for testing
def main():
    # Creating test class for testing
    test_sauce = Test_sauce()

    # Calling functions for testing / (Call functions one by one please)
    test_sauce.no_name_password()
#    test_sauce.only_username()
#    test_sauce.banned_account()
#    print(f"Correct Login: {test_sauce.correct_login()}")
#    test_sauce.counting_products()
#    print(test_sauce.test_empty_input_write_x())


# Calling main function
if __name__ == "__main__":
    main()
