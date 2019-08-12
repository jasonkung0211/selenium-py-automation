import os
from urllib import request
from datetime import datetime
import time
import hashlib
from pyvirtualdisplay import Display
from selenium import webdriver
from load_page import *
from selenium.webdriver.support.wait import WebDriverWait

IGNORE_ERROR_LIST = []


def alert_test(url, timeout, width, high):
    display = Display(visible=True, size=(width, high)).start()
    driver = webdriver.Chrome()
    driver.delete_all_cookies()  # Cleanup cache
    driver.set_page_load_timeout(timeout)
    driver.get(url)
    driver.find_element_by_xpath('//button[text()="Login"]').click()
    time.sleep(1)
    if driver.page_source.find("Please enter an account and password.") == -1:
        print("ERROR: not find message: \"Please enter an account and password.\"")

    driver.find_element_by_id("account").send_keys('ggyy')
    driver.find_element_by_id("password").send_keys('7788')
    driver.find_element_by_xpath('//button[text()="Login"]').click()
    time.sleep(1)
    if driver.page_source.find("Error: Account information or password is incorrect, please re-enter.") == -1:
        print("ERROR: not find message: \"Error: Account information or password is incorrect, please re-enter.\"")

    driver.close()
    driver.quit()
    display.stop()


def logo_test(url, timeout, width, high):
    display = Display(visible=True, size=(width, high)).start()
    driver = webdriver.Chrome()
    driver.delete_all_cookies()  # Cleanup cache
    driver.set_page_load_timeout(timeout)
    driver.get(url)

    images = driver.find_element_by_class_name("login-logo")
    print(images.get_attribute('src'))
    request.urlretrieve(images.get_attribute('src'), "logo.png")

    md5 = hashlib.md5()
    with open('logo.png', 'rb') as f:
        while True:
            data = f.read()
            if not data:
                break
            md5.update(data)
    if md5.hexdigest() != 'ddeda9bdaaa38a7db29e2626bf930842':
        print("ERROR: logo fail.")

    os.remove('./logo.png')

    driver.close()
    driver.quit()
    display.stop()


def account_test(url, timeout, width, high):
    display = Display(visible=True, size=(width, high)).start()
    browser = webdriver.Chrome()
    browser.delete_all_cookies()  # Cleanup cache
    browser.set_page_load_timeout(timeout)
    browser.get(url)

    # --------input account--------
    browser.find_element_by_id("account").send_keys('admin')
    browser.find_element_by_id("password").send_keys('admin')
    with wait_for_page_load(browser):
        browser.find_element_by_xpath('//button[text()="Login"]').click()
    time.sleep(2)
    save_screenshot_filepath = "%s/%s-%s.png" % ('./', datetime.now().strftime('%Y-%m-%d_%H%M%S'), url.rstrip("/").split("/")[-1])
    browser.get_screenshot_as_file(save_screenshot_filepath)

    browser.close()
    browser.quit()
    display.stop()


def load_page_test(url, timeout, width, high):
    max_load_second = timeout
    display = Display(visible=True, size=(width, high)).start()
    driver = webdriver.Chrome()
    driver.delete_all_cookies()  # Cleanup cache
    driver.set_page_load_timeout(timeout)
    print("Open page: %s" % url)
    start_clock = time.clock()
    driver.get(url)
    end_clock = time.clock()
    elapsed_seconds = (end_clock - start_clock) * 1000
    if elapsed_seconds > max_load_second:
        print("ERROR: page load is too slow. It took {:.3f} seconds, more than {:d} seconds.".format(elapsed_seconds, max_load_second))
    else:
        print("Page load took: {:.2f} seconds.".format(elapsed_seconds))

    print('Chrome  title: {}'.format(driver.title))

    all_warnings = driver.get_log('browser')
    critical_errors = []
    for warning in all_warnings:
        if warning['level'] == 'SEVERE':
            has_error = True
            for ignore_err in IGNORE_ERROR_LIST:
                if ignore_err in warning['message']:
                    has_error = False
                    break
            if has_error is True:
                critical_errors.append(warning)

    if len(critical_errors) != 0:
        print("ERROR: severe errors have happened when loading the page. Details:\n\t%s" % "\n\t".join([str(error) for error in critical_errors]))

    save_screenshot_filepath = "%s/%s-%s.png" % ('./', datetime.now().strftime('%Y-%m-%d_%H%M%S'), url.rstrip("/").split("/")[-1])
    driver.get_screenshot_as_file(save_screenshot_filepath)

    driver.close()
    driver.quit()
    display.stop()

    return
