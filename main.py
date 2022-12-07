import yamlValidate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from LinkedInBot import linkedinBot
from diceBot import diceBot
import os
from tkinter import *

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

    # constants
    WINDOWBG = "#17202A"
    BG = '#154360'
    FG = '#FDFEFE'

    window = Tk()
    window.title("Job Bot")
    window.config(bg=WINDOWBG)
    window.resizable(0, 0)

    # labels
    title = Label(text="Welcome to the All in one Job bot.", 
                  bg=WINDOWBG, 
                  fg=FG, 
                  font=('Arial', 24, 'bold'),
                  pady=5)
    title.grid(row=0,column=0, columnspan=2)

    subtitle = Label(text="""Please select an option below.""",
                     bg=WINDOWBG,
                     fg=FG,
                     font=('Arial', 18),
                     pady=5)
    subtitle.grid(row=1,column=0, columnspan=2)

    statusText = ''

    # functions
    def start_Linkedin_Bot():
        statusLabel.config(text='Starting Linkedin Bot')
        bot = linkedinBot(parameters, browser)
        bot.login()
        bot.security_check()
        bot.start_applying()

    def start_Dice_Bot():
        statusLabel.config(text='Starting Dice Bot')
        bot = diceBot(parameters, browser)
        bot.login()
        bot.security_check()
        bot.start_applying()
    
    def start_Indeed_Bot():
        statusLabel.config(text='Coming soon')
    
    def start_ZipRecruiter_Bot():
        statusLabel.config(text='Coming soon')
    
    def open_Readme():
        os.system('cmd /c notepad.exe README.md')

    def open_Config():
        os.system('cmd /c notepad.exe config.yaml')
    
    # buttons
    linkedin_Button = Button(text="Linked In", 
                            bd=0, 
                            bg=BG, 
                            fg=FG,
                            pady=10,
                            width=10,
                            font=('Arial', 12, 'bold'),
                            command=lambda: start_Linkedin_Bot())
    linkedin_Button.grid(row=2, column=0)

    dice_Button = Button(text="Dice", 
                            bd=0, 
                            bg=BG, 
                            fg=FG,
                            pady=10,
                            width=10,
                            font=('Arial', 12, 'bold'),
                            command=lambda: start_Dice_Bot())
    dice_Button.grid(row=2, column=1)

    indeed_Button = Button(text="Indeed", 
                            bd=0, 
                            bg=BG, 
                            fg=FG,
                            pady=10,
                            width=10,
                            font=('Arial', 12, 'bold'),
                            command=lambda: start_Indeed_Bot())
    indeed_Button.grid(row=3, column=0)

    zipRecruiter_Button = Button(text="ZipRecruiter", 
                            bd=0, 
                            bg=BG, 
                            fg=FG,
                            pady=10,
                            width=10,
                            font=('Arial', 12, 'bold'),
                            command=lambda: start_ZipRecruiter_Bot())
    zipRecruiter_Button.grid(row=3, column=1)

    statusLabel = Label(text=statusText,
                        bg=WINDOWBG,
                        fg=FG,
                        pady=10,
                        font=('arial', 18))
    statusLabel.grid(row=4, column=0, columnspan=2)

    config_Button = Button(text="Config", 
                            bd=0,
                            bg=BG, 
                            fg=FG,
                            pady=10,
                            width=10,
                            font=('Arial', 12, 'bold'),
                            command=lambda: open_Config())
    config_Button.grid(row=5, column=0)

    help_Button = Button(text="Help", 
                            bd=0, 
                            bg=BG, 
                            fg=FG,
                            pady=10,
                            width=10,
                            font=('Arial', 12, 'bold'),
                            command=lambda: open_Readme())
    help_Button.grid(row=5, column=1)

    exit_Button = Button(text="Exit", 
                            bd=0, 
                            bg=BG, 
                            fg=FG,
                            pady=10,
                            width=10,
                            font=('Arial', 12, 'bold'))
    exit_Button.grid(row=6, column=0, columnspan=2)

    window.mainloop()
