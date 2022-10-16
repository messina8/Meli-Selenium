from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
from time import sleep


def test_login():
    login = browser.find_element(By.NAME, 'user_id')
    login.send_keys('tete6762117')
    continuar = browser.find_element(By.CLASS_NAME, 'andes-button__content')
    continuar.click()
    sleep(2)
    password = browser.find_element(By.NAME, 'password')
    password.send_keys('qatest8742')
    ingresar = browser.find_element(By.NAME, 'action')
    ingresar.click()


def save_cookie(browser):
    with open("cookie", 'wb') as filehandler:
        pickle.dump(browser.get_cookies(), filehandler)


def load_cookie(browser):
    with open("cookie", 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            print(cookie)
            browser.add_cookie(cookie)


def edit_price():
    new_price = input('enter new price: ')
    edit_price_button = browser.find_element(By.CLASS_NAME, 'sc-list-actionable-cell__action')
    edit_price_button.click()
    sleep(2)
    edits = browser.find_elements(By.CLASS_NAME, 'andes-form-control__control')
    price_to_edit = edits[3].find_element(By.CLASS_NAME, 'andes-form-control__field')
    price_to_edit.send_keys(Keys.BACKSPACE * 6 + new_price)
    confirm = browser.find_elements(By.CLASS_NAME, 'andes-button__content')[2]
    confirm.click()


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
            sleep(.1)

        elif 'boolean' in i.get_attribute('class'):
            print('bool')
            i.find_elements(By.CLASS_NAME, 'sell-ui-switch__option')[1].click()
        elif 'list' in i.get_attribute('class'):
            print('list')
            i.click()
            i.find_elements(By.CLASS_NAME, 'andes-list__item-text')[3].click()
        else:
            print('Error, input type new o unrecognized')
        sleep(.2)

    y_n = input('Confirm? Y/N')
    browser.find_elements(By.CLASS_NAME, 'andes-button__content')[2].click()


if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get('https://www.mercadolibre.com.ar')
    try:
        load_cookie(browser)
    except FileNotFoundError:
        print('Please log in manually on automated web driver.')
        input('Once that is done press enter on console...')
        save_cookie(browser)

    browser.get('https://www.mercadolibre.com.ar/publicaciones/listado')
    search_bar = browser.find_element(By.CLASS_NAME, 'andes-form-control__field')
    search_button = browser.find_element(By.CLASS_NAME, 'sc-hover-button__icon')
    sleep(1)
    filter_button = browser.find_element(By.CLASS_NAME, 'sc-tags-container__title__text')
    filter_button.click()
    clear_filters = [a for a in browser.find_elements(By.CLASS_NAME, 'andes-button__content') if
                     a.text == 'Limpiar filtros']
    clear_filters[0].click()
    search_for = input('publi ID or Title: ')  # Should be a prompt to ask what to do, edit stock, change price, etc.
    search_bar.send_keys(search_for)
    search_button.click()
    print(f'searching for {search_for}')
    sleep(1.5)
    edit_price()
    sleep(5)
    edit_tech()
