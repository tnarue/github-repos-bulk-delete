from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from time import sleep
import time



def browser_start():
    chrome_options = Options()

    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_argument('--disable-setuid-sandbox')
    capabilities = DesiredCapabilities.CHROME

    user_agent = "Chrome"
    chrome_options.add_argument('user-agent={user_agent}'
                                .format(user_agent=user_agent))
    chrome_prefs = {
        'intl.accept_languages': 'en-US'
    }

    chrome_options.add_experimental_option('prefs', chrome_prefs)
    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              chrome_options=chrome_options)
    return driver


def github_login(driver, username, password):
    driver.get("https://github.com/login")
    unform = driver.find_element_by_xpath("//input[@name='login']")
    unform.send_keys(username)

    unform = driver.find_element_by_xpath("//input[@name='password']")
    unform.send_keys(password)
    time.sleep(5)

    login_button = driver.find_element_by_xpath('//input[@name = "commit"]')
    login_button.click()

    time.sleep(5)
    return driver

def get_totalpage(driver):
    try:
        total_page = int(
            driver.find_element_by_xpath('//div[@class = "pagination"]/em[1]').get_attribute("data-total-pages"))
        return total_page

    except NoSuchElementException:
        return 1


def get_pageurl(username, page):
    baseurl = "https://github.com/"
    repotab = "tab=repositories"
    if page > 1:
        page_text = "page=" + str(page)
        page_url = baseurl + username + "?" + page_text + "&" + repotab
        return page_url
    else:
        page_url = baseurl + username + "?" + repotab
        return page_url

def check_deletebutton(delete_button):
    if delete_button.text == "Delete this repository":
        return 1
    else:
        return 0