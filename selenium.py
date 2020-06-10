from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://projectby.trainings.dlabanalytics.com/msankevi34/")
element = driver.find_element_by_id('zocial-epam-idp').click()

notebook = driver.find_element_by_xpath("//*[@href='/msankevi34/notebooks/Final_Task.ipynb']").click()

button = driver.find_element_by_name('restart the kernel, then re-run the whole notebook (with dialog)').click()

button2 = driver.find_element(By.XPATH, '//button[text()="Restart and Run All Cells"]').click()

print(driver.title)
print(driver.current_url)
# driver.quit()
