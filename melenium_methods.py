from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException, \
    TimeoutException, NoSuchWindowException
from autofiller import auto_filler
import pickle
from time import sleep


def open_driver():
    try:
        driver = webdriver.Chrome()
    except WebDriverException:

        option = webdriver.ChromeOptions()
        option.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
        driver = webdriver.Chrome(options=option)
    return driver


def load_meli(browser):
    browser.get('https://www.mercadolibre.com.ar')
    try:
        load_cookie(browser)
    except FileNotFoundError:
        print('Please log in manually on automated web driver.')
        browser.get('https://www.mercadolibre.com/jms/mla/lgz/msl/login')
        input('Once that is done press enter on console...')
        save_cookie(browser)

    browser.get('https://www.mercadolibre.com.ar/publicaciones/listado')
    clear_filters(browser)


def save_cookie(browser):
    with open("cookie", 'wb') as filehandler:
        pickle.dump(browser.get_cookies(), filehandler)


def load_cookie(browser):
    with open("cookie", 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            # print(cookie)
            browser.add_cookie(cookie)
        print('Cookies loaded correctly')


def clear_filters(browser):
    try:
        filter_button = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sc-tags-container__title__text')))
        filter_button.click()
        clear_all = [a for a in browser.find_elements(By.CLASS_NAME, 'andes-button__content') if
                     a.text == 'Limpiar filtros']
        clear_all[0].click()
    except TimeoutException:
        active_filters = browser.find_elements(By.CLASS_NAME, 'andes-tag__close-icon')
        for i in reversed(active_filters):
            i.click()
            sleep(1.5)
