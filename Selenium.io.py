from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.google.com.tr/?hl=tr")
driver.maximize_window()
input = driver.find_element(By.NAME, "q")
print(f"Input: {input}")
while True:
    continue
