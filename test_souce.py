from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


class Test_sauce:
    def test_invalid_login(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        sleep(2)
        user_name_input = driver.find_element(By.ID, "user-name")
        password_input = driver.find_element(By.ID, "password")
        sleep(2)
        user_name_input.send_keys("1")
        password_input.send_keys("1")

        login_btn = driver.find_element(By.ID, "login-button")
        login_btn.click()

        error_message = driver.find_element(By.XPATH, "//*[@id='login_button_container']/div/form/div[3]/h3")
        test_result = error_message.text == "Epic sadface: Username and password do not match any user in this service"
        print(f"Test Sonucu: {test_result}")
        sleep(20)


testClass = Test_sauce()
testClass.test_invalid_login()
