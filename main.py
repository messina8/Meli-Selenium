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


def save_cookie():
    with open("cookie", 'wb') as filehandler:
        pickle.dump(browser.get_cookies(), filehandler)


def load_cookie():
    with open("cookie", 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            # print(cookie)
            browser.add_cookie(cookie)
        print('Cookies loaded correctly')


def find_publication(search):
    search_bar = browser.find_element(By.CLASS_NAME, 'andes-form-control__field')
    search_button = browser.find_element(By.CLASS_NAME, 'sc-hover-button__icon')
    search_bar.clear()
    search_bar.send_keys(Keys.BACKSPACE * 35 + search)
    search_button.click()
    print(f'searching for {search_for}')
    sleep(2.5)


def open_publication():
    first_result = browser.find_elements(By.CLASS_NAME, 'sc-list-item-row')[0]
    edit_price_button = first_result.find_element(By.CLASS_NAME, 'sc-list-item-row-description__title')
    edit_price_button.click()
    sleep(1)


def edit_price(updated_price):
    price_view = browser.find_elements(By.CLASS_NAME, 'sell-ui-card-header-icon')[1]
    sleep(.2)
    price_view.click()
    edits = WebDriverWait(browser, 2).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'andes-form-control__control')))
    # edits = browser.find_elements(By.CLASS_NAME, 'andes-form-control__control')
    price_to_edit = edits[3].find_element(By.CLASS_NAME, 'andes-form-control__field')
    price_to_edit.send_keys(Keys.BACKSPACE * 6 + updated_price)
    confirm = browser.find_elements(By.CLASS_NAME, 'andes-button__content')[2]
    confirm.click()
    try:
        popup = WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'andes-modal-dialog__wrapper')))
        # popup = browser.find_element(By.CLASS_NAME, 'andes-modal-dialog__wrapper')
        popup.find_elements(By.CLASS_NAME, 'andes-button__content')[0].click()
    except TimeoutException:
        pass
    sleep(4)


def edit_tech():
    tech_view = browser.find_elements(By.CLASS_NAME, 'sell-ui-card-header-icon')[3]
    tech_view.click()
    input_list = browser.find_elements(By.CLASS_NAME, 'modify-ui-attribute-template-with-hint')
    pending_items = [a for a in input_list if 'Completá' in a.text]
    for i in pending_items:
        if 'string' in i.get_attribute('class'):
            print('string')
            i.find_element(By.CLASS_NAME, 'andes-form-control__field').send_keys('No disponible')

        elif 'number' in i.get_attribute('class'):
            print('number')
            i.find_element(By.CLASS_NAME, 'andes-form-control__field').send_keys('0')

        elif 'multivalue' in i.get_attribute('class'):
            print('multivalue')
            i.find_element(By.CLASS_NAME, 'andes-form-control__field').send_keys('No disponible' + Keys.ENTER)

        elif 'boolean' in i.get_attribute('class'):
            print('bool')
            i.find_elements(By.CLASS_NAME, 'sell-ui-switch__option')[1].click()

        elif 'list' in i.get_attribute('class'):
            print('list')
            i.click()
            i.find_elements(By.CLASS_NAME, 'andes-list__item-text')[3].click()

        else:
            print('Error, input type new or unrecognized')
        sleep(.4)
    sleep(.4)

    try:
        browser.find_elements(By.CLASS_NAME, 'andes-button__content')[2].click()
    except ElementClickInterceptedException:
        print('Form not submitted')
        pass


def change_stock(delta, absolute=False):
    stock = WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.ID, 'quantity')))
    new_stock = int(stock.get_attribute('value')) + int(delta)
    # noinspection PyTypeChecker
    if absolute:
        stock.send_keys(Keys.BACKSPACE * 5 + delta)
    else:
        stock.send_keys(Keys.BACKSPACE * 5 + str(new_stock))
    browser.find_elements(By.CLASS_NAME, 'andes-button__content')[0].click()
    sleep(4)


def stock_to_int(string):
    num = ''
    for c in string:
        if c.isdigit():
            num += c
    return int(num)


def handle_stock(delta, price=''):
    first_result = browser.find_elements(By.CLASS_NAME, 'sc-list-item-row')[0]
    stock = first_result.find_element(By.CLASS_NAME, 'sc-list-item-row-description__info')
    state = first_result.find_elements(By.CLASS_NAME, 'sc-list-actionable-cell__title--text')[-1]

    if stock.text == 'Sin Stock' or state.text.lower() == 'inactiva':
        first_result.find_element(By.CLASS_NAME, 'sc-trigger-content__trigger').click()
        sleep(1.2)
        [a for a in first_result.find_elements(By.CLASS_NAME, 'andes-list__item') if
         a.text.lower() in ['reactivar', 'republicar']][0].click()
        if 'modificar' in browser.current_url:
            change_stock(delta)
        elif 'listado' in browser.current_url:
            open_publication()
            change_stock(delta, absolute=True)
        else:
            cant = browser.find_element(By.CLASS_NAME, 'syi-quantity__field')
            cant.send_keys(Keys.BACKSPACE * 2 + str(delta))
            sleep(.8)
            browser.find_elements(By.CLASS_NAME, 'syi-listing-type')[1].click()
            sleep(.3)
            # add price if price not ''
            browser.find_element(By.CLASS_NAME, 'syi-action-button__primary').click()
            sleep(1.8)
            #

    elif stock_to_int(stock.text) + int(delta) == 0:
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
            change_stock(0, absolute=True)
    else:
        change_stock(delta)


def open_driver():
    try:
        driver = webdriver.Chrome()
    except WebDriverException:

        option = webdriver.ChromeOptions()
        option.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
        driver = webdriver.Chrome(options=option)
    return driver


def clear_filters():
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


if __name__ == '__main__':
    browser = open_driver()
    browser.get('https://www.mercadolibre.com.ar')
    try:
        load_cookie()
    except FileNotFoundError:
        print('Please log in manually on automated web driver.')
        browser.get('https://www.mercadolibre.com/jms/mla/lgz/msl/login')
        input('Once that is done press enter on console...')
        save_cookie()

    browser.get('https://www.mercadolibre.com.ar/publicaciones/listado')
    clear_filters()
    print('Welcome to AutoMeli with Selenium!')
    while True:
        print("""
Your options are:

1)Change Price
2)Fill Tech Specs
3)Adjust Stock
0)Exit Program

enter the number of choice:""")
        choice = input()
        try:
            if choice == '5':
                auto_filler(browser)
            elif choice in ['1', '2', '3']:
                search_for = input('publi ID or Title: ')
                try:
                    find_publication(search_for)
                except NoSuchElementException:
                    choice = 9
                    print('No results found')
            if choice == '1':
                price = input('New price: ')
                tech = input('edit specs(Y/N)')
                open_publication()
                edit_price(price)
                if tech.lower() == "y":
                    edit_tech()
                browser.back()
            elif choice == '2':
                open_publication()
                edit_tech()
                browser.back()
            elif choice == '3':
                stock_change = input('Enter Stock change: ')
                change_price = input('should we change the price?(Y/N): ')
                if change_price.lower() == "y":
                    price = input('New price: ')
                    tech = input('edit specs(Y/N): ')
                    # change_stock(stock_change)
                    handle_stock(stock_change, price=price)
                    # edit_price(price)
                    if tech == "Y" or tech == "y":
                        edit_tech()
                else:
                    tech = input('edit specs(Y/N): ')
                    handle_stock(stock_change)
                    # change_stock(stock_change)
                    if tech.lower() == "y":
                        edit_tech()
                browser.back()
            elif choice == '0':
                browser.close()
                exit(0)

            else:
                pass

        except NoSuchWindowException:
            browser.get(browser.current_url)
