from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

from Constants import global_constants


class test_sauce:
    def test_invalid_login(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(global_constants.URL)
        WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.ID, "user-name")))
        user_name_input = driver.find_element(By.ID, "user-name")
        password_input = driver.find_element(By.ID, "password")
        user_name_input.send_keys("1")
        password_input.send_keys("1")
        login_btn = driver.find_element(By.ID, "login-button")
        login_btn.click()
        error_message = driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        test_result = error_message.text == "Epic sadface: Username and password do not match any user in this service"
        print(f"Test result: {test_result}")

    def test_valid_login(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(global_constants.URL)
        WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.ID, "user-name")))
        user_name_input = driver.find_element(By.ID, "user-name")
        password_input = driver.find_element(By.ID, "password")

        actions = ActionChains(driver)
        actions.send_keys_to_element(user_name_input, "standard_user")
        actions.send_keys_to_element(password_input, "secret_sauce")
        actions.perform()

        # user_name_input.send_keys("standard_user")
        # password_input.send_keys("secret_sauce")
        login_btn = driver.find_element(By.ID, "login-button")
        login_btn.click()

        driver.execute_script("window.scrollTo(0,250)")


testClass = test_sauce()
testClass.test_invalid_login()
testClass.test_valid_login()
