from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
import githubdelete.util as util
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def bulk_delete_all(driver, username, t):
    reposurl = util.get_pageurl(username, 1)
    driver.get(reposurl)
    time.sleep(t)
    total_page = util.get_totalpage(driver)

    i = 0
    for i in range(total_page):
        pageurl = util.get_pageurl(username, i + 1)
        driver.get(pageurl)
        time.sleep(t)

        try:
            elem = driver.find_element_by_xpath('//div[@id = "user-repositories-list"]/ul[1]')
            repo_list = wait(driver, 10).until(lambda driver: elem.find_elements_by_css_selector('h3 > a'))
            for repo in repo_list:
                name = repo.text
                print("repository name: " + name)
                repolink = repo.get_attribute("href")
                reposettingsurl = repolink + "/settings"
                driver.execute_script("window.open('', '__blank');")
                driver.switch_to_window(driver.window_handles[1])
                driver.get(reposettingsurl)
                time.sleep(t)
                delete_button = driver.find_element_by_xpath(
                    '//div[@class = "Box Box--danger"]/ul[1]/li[4]/details[1]/summary[1]')
                if util.check_deletebutton(delete_button):
                    ActionChains(driver).move_to_element(delete_button).click().perform()
                    time.sleep(t)
                    reponame_inputbox = driver.find_element_by_xpath(
                        '//div[@class = "Box Box--danger"]/ul[1]/li[4]/details[1]/details-dialog[1]/div[3]/form[1]/p[1]/input[1]')
                    time.sleep(t)
                    reponame_inputbox.click()
                    time.sleep(t)
                    reponame_inputbox.send_keys(Keys.TAB)
                    reponame_inputbox.send_keys(name)
                    time.sleep(t)
                    confirm_button = driver.find_element_by_xpath(
                        '//div[@class = "Box Box--danger"]/ul[1]/li[4]/details[1]/details-dialog[1]/div[3]/form[1]/button[1]')
                    confirm_button.click()
                    time.sleep(t)
                    driver.close()
                    driver.switch_to_window(driver.window_handles[0])
            else:
                print("This repository is in the exception list.")

            return driver
        except NoSuchElementException:
            print("Error: Element not found")
            return driver


def bulk_delete_with_exception(driver, username, t, repo_exception_list):
    reposurl = util.get_pageurl(username, 1)
    driver.get(reposurl)
    time.sleep(t)
    total_page = util.get_totalpage(driver)

    i = 0
    for i in range(total_page):
        pageurl = util.get_pageurl(username, i + 1)
        driver.get(pageurl)
        time.sleep(t)

        try:
            elem = driver.find_element_by_xpath('//div[@id = "user-repositories-list"]/ul[1]')
            repo_list = wait(driver, 10).until(lambda driver: elem.find_elements_by_css_selector('h3 > a'))
            for repo in repo_list:
                name = repo.text
                print("repository name: " + name)
                if name not in repo_exception_list:
                    repolink = repo.get_attribute("href")
                    reposettingsurl = repolink + "/settings"
                    driver.execute_script("window.open('', '__blank');")
                    driver.switch_to_window(driver.window_handles[1])
                    driver.get(reposettingsurl)
                    time.sleep(t)
                    delete_button = driver.find_element_by_xpath(
                        '//div[@class = "Box Box--danger"]/ul[1]/li[4]/details[1]/summary[1]')
                    if util.check_deletebutton(delete_button):
                        ActionChains(driver).move_to_element(delete_button).click().perform()
                        time.sleep(t)
                        reponame_inputbox = driver.find_element_by_xpath(
                            '//div[@class = "Box Box--danger"]/ul[1]/li[4]/details[1]/details-dialog[1]/div[3]/form[1]/p[1]/input[1]')
                        time.sleep(t)
                        reponame_inputbox.click()
                        time.sleep(t)
                        reponame_inputbox.send_keys(Keys.TAB)
                        reponame_inputbox.send_keys(name)
                        time.sleep(t)
                        confirm_button = driver.find_element_by_xpath(
                            '//div[@class = "Box Box--danger"]/ul[1]/li[4]/details[1]/details-dialog[1]/div[3]/form[1]/button[1]')
                        confirm_button.click()
                        time.sleep(t)
                        driver.close()
                        driver.switch_to_window(driver.window_handles[0])
                else:
                    print("This repository is in exception list.")

            return driver

        except NoSuchElementException:
            print("Error: Element not found")
            return driver


def bulk_delete_by_reponame(driver, username, t, string_contain_list):
    reposurl = util.get_pageurl(username, 1)
    driver.get(reposurl)
    time.sleep(t)
    total_page = util.get_totalpage(driver)

    i = 0
    for i in range(total_page):
        pageurl = util.get_pageurl(username, i + 1)
        driver.get(pageurl)
        time.sleep(t)

        try:
            elem = driver.find_element_by_xpath('//div[@id = "user-repositories-list"]/ul[1]')
            repo_list = wait(driver, 10).until(lambda driver: elem.find_elements_by_css_selector('h3 > a'))
            for repo in repo_list:
                name = repo.text
                print("repository name: " + name)
                if any(text in name for text in string_contain_list):
                    repolink = repo.get_attribute("href")
                    print("repolink: " + repolink)
                    reposettingsurl = repolink + "/settings"
                    driver.execute_script("window.open('', '__blank');")
                    driver.switch_to_window(driver.window_handles[1])
                    driver.get(reposettingsurl)
                    time.sleep(t)
                    delete_button = driver.find_element_by_xpath(
                        '//div[@class = "Box Box--danger"]/ul[1]/li[4]/details[1]/summary[1]')
                    if util.check_deletebutton(delete_button):
                        ActionChains(driver).move_to_element(delete_button).click().perform()
                        time.sleep(t)
                        reponame_inputbox = driver.find_element_by_xpath(
                            '//div[@class = "Box Box--danger"]/ul[1]/li[4]/details[1]/details-dialog[1]/div[3]/form[1]/p[1]/input[1]')
                        time.sleep(t)
                        reponame_inputbox.click()
                        time.sleep(t)
                        reponame_inputbox.send_keys(Keys.TAB)
                        reponame_inputbox.send_keys(name)
                        time.sleep(t)
                        confirm_button = driver.find_element_by_xpath(
                            '//div[@class = "Box Box--danger"]/ul[1]/li[4]/details[1]/details-dialog[1]/div[3]/form[1]/button[1]')
                        confirm_button.click()
                        time.sleep(t)
                        driver.close()
                        driver.switch_to_window(driver.window_handles[0])
                else:
                    print("This repository name does not contains given strings.")

            return driver

        except NoSuchElementException:
            print("Error: Element not found")
            return driver
