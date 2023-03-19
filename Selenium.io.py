from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome()
driver.get("https://www.google.com.tr/?hl=tr")
driver.maximize_window()

input = driver.find_element(By.NAME, "q")
input.send_keys("kodlamaio")

serch_button = driver.find_element(By.NAME, "btnK")
sleep(2)
serch_button.click()
sleep(2)
first_result = driver.find_element(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/a')
sleep(2)
first_result.click()

list_couse = driver.find_elements(By.CLASS_NAME, "course-listing")
print(f"Total courses: {len(list_couse)}")
while True:
    continue

# fullXpath
# /html/body/div[7]/div/div[11]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/a

# Xpath
# //*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/a
