from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium_controller as controller
from time import sleep


def auto_filler(browser):  # cant find a way to make it work.
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
    tabs = [a for a in browser.find_elements(By.CLASS_NAME, 'sc-bulk-tab__name') if a.text == 'Libros']
    tabs[0].click()
    lineas = browser.find_elements(By.CLASS_NAME, 'fixedDataTableRowLayout_main')
    cuadrados = lineas[2].find_elements(By.CLASS_NAME, 'sc-bulk-cell__text')[13:]
    cuadrados2 = lineas[2].find_elements(By.CLASS_NAME, 'sc-bulk-cell')[17:48]
    # combi = list(zip(cuadrados2, cuadrados))
    for h, i in enumerate(cuadrados2[1:]):
        print(h)
        text = cuadrados[h + 1]
        if text.text == '':
            if 'number' in i.get_attribute('class'):
                print('number')
                text.click()
                sleep(.1)
                text.click()
                sleep(.3)
                q = text.find_element(By.CLASS_NAME, 'andes-form-control__field')
                q.send_keys('No disponible' + Keys.ENTER)
            elif 'string' in i.get_attribute('class'):
                print('string')
                text.click()
                sleep(.1)
                print('click')
                text.click()
                print('click')
                sleep(1)
                q = browser.find_element(By.CLASS_NAME, 'sc-bulk-textfield__edition_mode')
                q.send_keys('No disponible' + Keys.ENTER)


def mass_filler(browser):
    print('Starting Mass Filler')
    links = []
    active = True
    browser.get('https://www.mercadolibre.com.ar/publicaciones/listado?filters=ACTIVE&page=1&sort=DEFAULT')
    # browser.find_element(By.ID, 'filter_trigger').click()
    # try:
    #     WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'andes-checkbox__label')))
    #     [a for a in browser.find_elements(By.CLASS_NAME, 'andes-checkbox__label') if a.text == 'Activas'][0].click()
    #     [a for a in browser.find_elements(By.CLASS_NAME, 'andes-button__content') if a.text == 'Aplicar'][0].click()
    # except IndexError:
    #     print('Could not find filters')
    #     return 'Could not find filters'
    while active:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-list-item-row')))
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-list-item-row-quality')))
        for i in browser.find_elements(By.CLASS_NAME, 'sc-list-item-row'):
            try:
                if 'Básica' in i.find_element(By.CLASS_NAME, 'sc-list-item-row-quality').text:
                    link = i.find_element(By.CLASS_NAME, 'sc-list-item-row-description__content').get_attribute('href')
                    links.append(link)
            except NoSuchElementException:
                pass

        for pub in links:
            browser.execute_script(f'''window.open("{pub}","_blank");''')

        sleep(3)
        for tab in browser.window_handles[1:]:
            browser.switch_to.window(tab)
            try:
                controller.edit_tech(browser)
            except NoSuchElementException:
                print(f'Error loading page {browser.current_url}')

        for tab in browser.window_handles[1:]:
            browser.switch_to.window(tab)
            browser.close()

        browser.switch_to.window(browser.window_handles[0])
        browser.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
        sleep(1.5)
        try:
            browser.find_elements(By.CLASS_NAME, 'andes-pagination__button')[-1].click()
            sleep(1)
        except NoSuchElementException:
            active = False
            return 'Mass editing finished'
