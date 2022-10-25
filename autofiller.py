from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


def auto_filler(browser):
    browser.find_element(By.CLASS_NAME, 'sc-list-custom-dropdown__button').click()
    browser.find_elements(By.CLASS_NAME, 'sc-list-custom-dropdown__option-wrapper')[1].click()
    sleep(4)
    filters = [a for a in browser.find_elements(By.CLASS_NAME, 'sc-ui-hover-button__text') if
               'Filtros' in a.text]
    filters[0].click()
    sleep(3)
    browser.execute_script("arguments[0].click();", browser.find_element(By.ID, 'ACTIVE'))
    browser.find_elements(By.CLASS_NAME, 'andes-button__content')[1].click()
    sleep(2)
    browser.find_elements(By.CLASS_NAME, 'sc-bulk-tab__name')
