import time
import random
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)
driver.maximize_window()

# open the webpage
driver.get("https://www.beenverified.com/app/login")
time.sleep(5)

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='login-email']")))
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='login-password']")))

# enter username and password
username.clear()
username.send_keys('salvep@salvesoft.com')
password.clear()
password.send_keys('Salve123_!')
time.sleep(5)

# target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
# We are logged in!
time.sleep(15)

# open new window with execute_script()
driver.execute_script("window.open('');")
time.sleep(5)
# switch to new window with switch_to.window()
driver.switch_to.window(driver.window_handles[1])
time.sleep(5)

# List of urls of leads
list_of_links = [
    'https://www.beenverified.com/app/report/person?bvid=N_MDU0OTkyOTQ3ODY2&name=REBECCA%20S%20DUBICK&permalink=5d1deb1c31e6032448bb0442225758c8c7edbd057a085f48b698a3',
    'https://www.beenverified.com/app/report/person?bvid=N_MDAwNjY0NzYzNzE5&permalink=a2108844a258baf40efefa305ecda9bb07241a36cd4a65129bb58c']

# creating empty array
data_contact = []
data_email = []
data_name = []


def short_time():
    return random.randint(1, 3)


def long_time():
    return random.randint(5, 11)


# function to check the document is loaded ?
#  wrap , onCanvas are the id's if the page_is_loading get fails
def page_is_loading(driver_tool):
    while True:
        x = driver_tool.execute_script("return document.readyState")
        if x == "complete":
            return True
        else:
            yield False


def search(f_name, m_name, l_name, city_name, state_name, driver_search):
    search_people = driver_search.find_element_by_xpath("(//a[@id='peopleTab'])")
    search_people.click()

    time.sleep(short_time())

    first_name = WebDriverWait(driver_search, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='fn']")))
    m_i = WebDriverWait(driver_search, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='mn']")))
    last_name = WebDriverWait(driver_search, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='ln']")))
    city = WebDriverWait(driver_search, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='city']")))
    state = Select(driver_search.find_element_by_name('state'))

    first_name.send_keys(f_name)
    m_i.send_keys(m_name)
    last_name.send_keys(l_name)
    city.send_keys(city_name)
    if state_name == '':
        state.select_by_value(state_name)

    search_people = WebDriverWait(driver_search, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    search_people.click()

    while not page_is_loading(driver_search):
        continue

    time.sleep(long_time())

    driver_search.execute_script("window.scrollBy(0, arguments[0]);", 1000)
    count_res = driver_search.find_elements_by_xpath("(//a[@class='panel automation-person-result-data-card'])")

    if len(count_res) > 0:
        return True
    else:
        return False


driver.find_element_by_xpath("(//h3[@class='person-name'])").click()


def render_result(driver_search):
    driver_search.execute_script("window.history.go(-1)")
    return driver_search.find_elements_by_xpath("(//a[@class='panel automation-person-result-data-card'])")


search('Robert', '', 'Rohdie', '', 'CA', driver)
render_result(driver)
# time.sleep(10)
for link in list_of_links:

    driver.get(link)
    time.sleep(5)
    while not page_is_loading(driver):
        continue

    data_lead_name = driver.find_element_by_xpath("(//h1[@class='report-header__title'])").text
    driver.execute_script("window.scrollBy(0, arguments[0]);", 1000)
    data_lead = driver.find_elements_by_xpath("(//a[@class='ember-view title_link'])")

    individual_phone = []
    individual_email = []

    for i in data_lead:
        if any(c.isalpha() for c in i.text):
            if '@' in i.text:
                individual_email.append(i.text)
                # print(i.text)
        else:
            individual_phone.append(i.text)
            # print(i.text)

    data_name.append(data_lead_name)
    data_contact.append(individual_phone)
    data_email.append(individual_email)

# driver.quit()

dummy_tup = tuple(zip(data_name, data_contact, data_email))
pre_dataFrame = pd.DataFrame(dummy_tup,
                             columns=['data_name', 'data_contact', 'data_email'])

pre_dataFrame['data_contact'] = pre_dataFrame['data_contact'].astype(str).str.replace(r'\[|\]|', '')
pre_dataFrame['data_email'] = pre_dataFrame['data_email'].astype(str).str.replace(r'\[|\]|', '')
