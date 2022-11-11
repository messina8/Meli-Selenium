import pickle
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException, \
    TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def open_driver():
    try:
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=options)
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
    try:
        clear_filters(browser)
    except ElementNotInteractableException:
        sleep(1)
        clear_filters(browser)


def save_cookie(browser):
    with open("cookie", 'wb') as filehandler:
        pickle.dump(browser.get_cookies(), filehandler)


def load_cookie(browser):
    with open("cookie2", 'rb') as cookies_file:
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
    except IndexError:
        browser.find_element(By.ID, 'filter_trigger').click()
        sleep(1.5)
        browser.find_elements(By.CLASS_NAME, 'andes-button--medium andes-button--transparent')
        [a for a in browser.find_elements(By.CLASS_NAME, 'andes-button') if
         a.accessible_name == 'Limpiar filtros'][0].click()


def popup_handler(browser):
    popup = True
    while popup:
        try:
            browser.find_element(By.CLASS_NAME, 'sell-ui-snackbar__message')
        except NoSuchElementException:
            popup = False


def handle_stock(browser, delta, new_price=''):
    first_result = browser.find_elements(By.CLASS_NAME, 'sc-list-item-row')[0]
    stock = first_result.find_element(By.CLASS_NAME, 'sc-list-item-row-description__info')
    state = first_result.find_elements(By.CLASS_NAME, 'sc-list-actionable-cell__title--text')[-1]

    if stock.text == 'Sin Stock' or state.text.lower() == 'inactiva':
        first_result.find_element(By.CLASS_NAME, 'sc-trigger-content__trigger').click()
        sleep(1.2)
        [a for a in first_result.find_elements(By.CLASS_NAME, 'andes-list__item') if
         a.text.lower() in ['reactivar', 'republicar']][0].click()
        sleep(2)
        if 'modificar' in browser.current_url:
            change_stock(browser, delta)
            popup_handler(browser)
            sleep(1)
            if new_price != '':
                edit_price(browser, new_price)
        elif 'listado' in browser.current_url:
            open_publication(browser)
            change_stock(browser, delta, absolute=True)
            popup_handler(browser)
            if new_price != '':
                edit_price(browser, new_price)
        else:
            cant = browser.find_element(By.ID, 'relist-0.item.available_quantity')
            # noinspection PyTypeChecker
            cant.send_keys(Keys.BACKSPACE * 2 + str(delta))
            price_in = browser.find_element(By.ID, 'relist-0.item.price')
            if new_price != '':
                # noinspection PyTypeChecker
                price_in.send_keys(Keys.BACKSPACE * 6 + new_price)
            sleep(.8)
            browser.find_elements(By.CLASS_NAME, 'syi-listing-type')[1].click()
            sleep(.3)
            browser.find_element(By.CLASS_NAME, 'syi-action-button__primary').click()
            sleep(1.8)
            primary_button = browser.find_element(By.CLASS_NAME, 'syi-action-button__primary')
            if '/modificar/' in primary_button.get_attribute('href'):
                primary_button.click()
                edit_tech(browser)
            else:
                browser.back()

    elif stock_to_int(stock.text) + int(delta) <= 0:
        try:
            first_result.find_element(By.CLASS_NAME, 'sc-trigger-content__trigger').click()
            sleep(1)
            [a for a in first_result.find_elements(By.CLASS_NAME, 'andes-list__item') if
             a.text.lower() == 'pausar'][0].click()
            sleep(1)
            [a for a in browser.find_elements(By.CLASS_NAME, 'andes-button__content') if a.text.lower() == 'confirmar'][
                0].click()
        except IndexError:
            first_result.find_element(By.CLASS_NAME, 'sc-trigger-content__trigger').click()
            sleep(1)
            [a for a in first_result.find_elements(By.CLASS_NAME, 'andes-list__item') if
             a.text.lower() == 'modificar'][0].click()
            change_stock(browser, 0, absolute=True)
    else:
        open_publication(browser)
        change_stock(browser, delta)
        popup_handler(browser)


def stock_to_int(string):
    num = ''
    for c in string:
        if c.isdigit():
            num += c
    return int(num)


def open_publication(browser):
    first_result = browser.find_elements(By.CLASS_NAME, 'sc-list-item-row')[0]
    edit_price_button = first_result.find_element(By.CLASS_NAME, 'sc-list-item-row-description__title')
    edit_price_button.click()
    sleep(1)


def find_publication(browser, search):
    search_bar = browser.find_element(By.CLASS_NAME, 'andes-form-control__field')
    search_button = browser.find_element(By.CLASS_NAME, 'sc-hover-button__icon')
    search_bar.clear()
    search_bar.send_keys(Keys.BACKSPACE * 35 + search)
    search_button.click()
    print(f'searching for {search}')
    sleep(2.5)
    print(f'{len(browser.find_elements(By.CLASS_NAME, "sc-list-item-row"))} results')


def edit_price(browser, updated_price):
    price_view = browser.find_element(By.ID, 'prices_header_container')
    sleep(.2)
    price_view.click()
    edits = WebDriverWait(browser, 2).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'andes-form-control__control')))
    price_to_edit = edits[3].find_element(By.CLASS_NAME, 'andes-form-control__field')
    price_to_edit.send_keys(Keys.BACKSPACE * 6 + updated_price)
    confirm = browser.find_elements(By.CLASS_NAME, 'andes-button__content')[2]
    confirm.click()
    try:
        popup = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'andes-modal-dialog__wrapper')))
        popup.find_elements(By.CLASS_NAME, 'andes-button__content')[0].click()
    except TimeoutException:
        pass
    sleep(3)
    popup_handler(browser)


def edit_tech(browser):
    tech_view = browser.find_element(By.ID, 'technical_specifications_header_container')
    tech_view.click()
    input_list = browser.find_elements(By.CLASS_NAME, 'modify-ui-attribute-template-with-hint')
    for i in input_list:
        if 'string' in i.get_attribute('class'):
            v = i.find_element(By.CLASS_NAME, 'andes-form-control__field')
            if v.get_attribute('value') == '':
                v.send_keys('No disponible')
                sleep(.3)
        elif 'number' in i.get_attribute('class'):
            v = i.find_element(By.CLASS_NAME, 'andes-form-control__field')
            if v.get_attribute('value') == '':
                v.send_keys('0')
                sleep(.3)
        elif 'multivalue' in i.get_attribute('class'):
            v = i.find_element(By.CLASS_NAME, 'andes-form-control__field')
            if v.get_attribute('value').lower() == 'no aplica':
                pass
            else:
                v = i.find_elements(By.CLASS_NAME, 'andes-tag')
                if len(v) == 0:
                    i.find_element(By.CLASS_NAME, 'andes-form-control__field').send_keys('No disponible' + Keys.ENTER)
                    sleep(.3)
                else:
                    pass

        elif 'boolean' in i.get_attribute('class'):
            checked = [a for a in i.find_elements(By.CLASS_NAME, 'sell-ui-switch__input') if
                       a.get_attribute('checked')]
            if len(checked) == 0:
                i.find_elements(By.CLASS_NAME, 'sell-ui-switch__option')[1].click()
                sleep(.3)

        elif 'list' in i.get_attribute('class'):
            v = i.find_element(By.CLASS_NAME, 'andes-dropdown__trigger')
            if 'elegir' in v.get_attribute('aria-label').lower():
                i.click()
                i.find_elements(By.CLASS_NAME, 'andes-list__item-text')[3].click()
                sleep(.3)
        else:
            print('Error, input type new or unrecognized')

    try:
        browser.find_elements(By.CLASS_NAME, 'andes-button__content')[2].click()
        print('Form submitted correctly')
        sleep(1.2)
    except ElementClickInterceptedException:
        print('Form not submitted')


def change_stock(browser, delta, absolute=False):
    stock = WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.ID, 'quantity')))
    new_stock = int(stock.get_attribute('value')) + int(delta)
    if absolute:
        stock.send_keys(Keys.BACKSPACE * 5 + delta)
    else:
        # noinspection PyTypeChecker
        stock.send_keys(Keys.BACKSPACE * 5 + str(new_stock))
    browser.find_elements(By.CLASS_NAME, 'andes-button__content')[0].click()
    sleep(3)
    popup = True
    while popup:
        try:
            browser.find_element(By.CLASS_NAME, 'sell-ui-snackbar__message')
        except NoSuchElementException:
            popup = False
