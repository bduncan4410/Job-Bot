import yamlValidate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from LinkedInBot import linkedinBot
from diceBot import diceBot


def init_browser():
    browser_options = Options()
    options = ['--disable-blink-features', '--no-sandbox', '--start-maximized', '--disable-extensions',
               '--ignore-certificate-errors-spki-list', '--ignore-ssl-errors', '--disable-blink-features=AutomationControlled']

    for option in options:
        browser_options.add_argument(option)

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=browser_options)

    driver.set_window_position(0, 0)
    driver.maximize_window()

    return driver


if __name__ == '__main__':
    parameters = yamlValidate.validate_yaml()
    browser = init_browser()

    print("")
    print("Welcome to the All in one Job bot. ")
    print("Please type the respect number for the Job Board you would like to use.  ")
    print("1: Linked In")
    print("2: Dice ")
    print("3: Indeed --Coming Soon")
    print("4: ZipRecruiter --Coming Soon")
    print("")

    choice = int(input())
    if choice < 3:
        match choice:
            case 1:
                print("Starting LinkedIn Bot")
                bot = linkedinBot(parameters, browser)
                bot.login()
                bot.security_check()
                bot.start_applying()
            case 2:
                print("Starting Dice Bot")
                bot = diceBot(parameters, browser)
                bot.login()
                bot.security_check()
                bot.start_applying()
            case _:
                print("An invalid option was selected. Application will close now.")







