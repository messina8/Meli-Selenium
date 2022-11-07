from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from autofiller import auto_filler
import selenium_controller as controller

if __name__ == '__main__':
    browser = controller.open_driver()
    controller.load_meli(browser)

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
                    controller.find_publication(browser, search_for)
                except NoSuchElementException or IndexError:
                    choice = 9
                    print('No results found')
            if choice == '1':
                price = input('New price: ')
                tech = input('edit specs(Y/N)')
                controller.open_publication(browser)
                controller.edit_price(browser, price)
                if tech.lower() == "y":
                    controller.edit_tech(browser)
                browser.back()
            elif choice == '2':
                controller.open_publication(browser)
                controller.edit_tech(browser)
                browser.back()
            elif choice == '3':
                stock_change = input('Enter Stock change: ')
                change_price = input('should we change the price?(Y/N): ')
                if change_price.lower() == "y":
                    price = input('New price: ')
                    tech = input('edit specs(Y/N): ')
                    controller.handle_stock(browser, stock_change, new_price=price)
                    if tech == "Y" or tech == "y":
                        try:
                            controller.edit_tech(browser)
                        except NoSuchElementException:
                            pass
                else:
                    tech = input('edit specs(Y/N): ')
                    controller.handle_stock(browser, stock_change)
                    if tech.lower() == "y":
                        controller.edit_tech(browser)
                controller.load_meli(browser)
            elif choice == '0':
                browser.close()
                exit(0)

            else:
                pass

        except NoSuchWindowException:
            # should detect if browser is still open, in case it got closed.
            window_name = browser.window_handles[0]
            browser.switch_to.window(window_name)
            print('Reference to window was lost and recovered')

